from django.http import HttpResponse

from open_facebook.api import OpenFacebook
from helperFunctions import *
import json

FBOpen = OpenFacebook


def formattedResponse(isError=False, errorMessage=None, data=None):
    '''
    Returns a properly formatted response for our API.
    :param isError: Whether or not there was an error.
    :param errorMessage: A human readable error message.
    :param data: The appropriate data if the response
    '''

    response = {
        'isError': isError,
        'errorMessage': errorMessage,
        'data': data,
    }

    return HttpResponse(json.dumps(response), content_type="application/json")


def loginWithFacebook(request):
    '''
    Required fields:

        accessToken

    '''
    requiredFields = ['accessToken']

    verifiedRequestResponse = verifyRequest(request.POST, requiredFields)
    if verifiedRequestResponse['isMissingFields']:
        errorMessage = verifiedRequestResponse['errorMessage']
        return formattedResponse(isError=True, errorMessage=errorMessage)

    request = request.POST
    accessToken = request['accessToken']

    graph = FBOpen(access_token=accessToken)

    try:
        userInfo = graph.get('me', fields='name, picture, id')
    except:
        errorMessage = 'Bad access token'
        return formattedResponse(isError=True, errorMessage=errorMessage)

    userName = userInfo['name']
    userId = userInfo['id']

    account, isAccountCreated = Account.objects.get_or_create(
        userId=userId,
        name=userName
    )

    if isAccountCreated:
        titles = []
        aboutMe = ''
        jobs = {
            'currentJobsAsEmployee': [],
            'completedJobsAsEmployee': []
        }
        nonprofits = []
        skills = []
        profileImageUrl = userInfo['picture']['data']['url']

        UserProfileImage.objects.create(account=account, url=profileImageUrl)

    else:
        userModel = getUserModel(account)

        titles = userModel['titles']
        aboutMe = userModel['aboutMe']
        jobs = userModel['jobs']
        nonprofits = userModel['nonprofits']
        skills = userModel['skills']
        profileImageUrl = userModel['profileImageUrl']

    loginWithFacebookReturn = {
        'me': {
            'userId': userId,
            'name': userName,
            'titles': titles,
            'aboutMe': aboutMe,
            'jobs': jobs,
            'nonprofits': nonprofits,
            'skills': skills,
            'profileImageUrl': profileImageUrl
        }
    }

    return formattedResponse(data=loginWithFacebookReturn)


def updateProfile(request):
    '''
    Required fields:

        userId
        profile

    '''

    # verify top-level objects
    requiredFields = ['userId', 'profile']
    verifiedRequestResponse = verifyRequest(request.POST, requiredFields)
    if verifiedRequestResponse['isMissingFields']:
        errorMessage = verifiedRequestResponse['errorMessage']
        return formattedResponse(isError=True, errorMessage=errorMessage)

    # verify object nested in profile
    try:
        requiredFields = ['aboutMe', 'titles', 'skills', 'resume']
        verifiedRequestResponse = verifyRequest(json.loads(request.POST[
            'profile']), requiredFields)
        if verifiedRequestResponse['isMissingFields']:
            errorMessage = verifiedRequestResponse['errorMessage']
            return formattedResponse(isError=True, errorMessage=errorMessage)
    except:
        errorMessage = 'profile was not a valid JSON'
        return formattedResponse(isError=True, errorMessage=errorMessage)

    request = request.POST
    userId = request['userId']
    profile = json.loads(request['profile'])

    aboutMe = profile['aboutMe']
    resume = profile['resume']
    titles = profile['titles']
    skills = profile['skills']

    if Account.objects.filter(userId=userId).exists():
        account = Account.objects.get(userId=userId)

        account.aboutMe = aboutMe
        account.resume = resume
        # remove current skills from the new skills list
        # if skill not in the new skills list, delete it
        currentSkills = getUserSkills(account)
        for skillObject in currentSkills:
            skill = str(skillObject.skill)
            if skill in skills:
                skills.remove(skill)
            else:
                skillObject.delete()
        # add the new skills
        for skill in skills:
            UserSkill.objects.create(account=account, skill=skill)

        # remove current titles from the new titles list
        # if title not in the new titles list, delete it
        currentTitles = getUserTitles(account)
        for titleObject in currentTitles:
            title = str(titleObject.title)
            if title in titles:
                titles.remove(title)
            else:
                titleObject.delete()
        # add the new titles
        for title in titles:
            UserTitle.objects.create(account=account, title=title)

        account.save()
    else:
        errorMessage = 'Unknown user'
        return formattedResponse(isError=True, errorMessage=errorMessage)

    updatedProfileModel = {
        'titles': formatTitles(getUserTitles(account)),
        'skills': formatSkills(getUserSkills(account)),
        'aboutMe': str(account.aboutMe),
        'resume': str(account.resume)
    }

    return formattedResponse(data=updatedProfileModel)


def createNonprofit(request):
    '''
    Required fields:

        userId
        nonprofit

    '''

    # verify top-level objects
    requiredFields = ['userId', 'nonprofit']
    verifiedRequestResponse = verifyRequest(request.POST, requiredFields)
    if verifiedRequestResponse['isMissingFields']:
        errorMessage = verifiedRequestResponse['errorMessage']
        return formattedResponse(isError=True, errorMessage=errorMessage)

    # verify nonprofit object
    try:
        requiredFields = ['name', 'mission', 'description', 'website',
                          'address']
        verifiedRequestResponse = verifyRequest(json.loads(request.POST[
            'nonprofit']), requiredFields)
        if verifiedRequestResponse['isMissingFields']:
            errorMessage = verifiedRequestResponse['errorMessage']
            return formattedResponse(isError=True, errorMessage=errorMessage)
    except:
        errorMessage = 'nonprofit was not a valid JSON'
        return formattedResponse(isError=True, errorMessage=errorMessage)

    request = request.POST

    userId = request['userId']
    nonprofit = json.loads(request['nonprofit'])

    if Account.objects.filter(userId=userId).exists():

        newNonprofit, isNewNonprofitCreated = Nonprofit.objects.get_or_create(
            name=nonprofit['name'],
            description=nonprofit['description'],
            mission=nonprofit['mission'],
            website=nonprofit['website'],
            address=nonprofit['address']
        )
        if isNewNonprofitCreated:

            # get user nonprofit models
            account = Account.objects.get(userId=userId)
            userNonprofits = formatNonprofitsForUserModel(getUserNonprofits(
                account))
            newNonprofitModel = getNonprofitModel(newNonprofit)

            # add nonprofit relation
            NonprofitRelation.objects.create(
                nonprofitId=str(newNonprofit.pk),
                userId=userId
            )

        else:
            errorMessage = 'Failed to create nonprofit'
            return formattedResponse(isError=True, errorMessage=errorMessage)
    else:
        errorMessage = 'Unknown user'
        return formattedResponse(isError=True, errorMessage=errorMessage)

    userNonprofitModels = {
        'myNonprofits': userNonprofits,
        'newNonprofit': newNonprofitModel
    }

    return formattedResponse(data=userNonprofitModels)


def postJobAsNonprofit(request):
    '''
    Required fields:
        userId
        nonproftId
        jobToPost
    '''

    # verify top-level objects
    requiredFields = ['userId', 'nonprofitId', 'jobToPost']
    verifiedRequestResponse = verifyRequest(request.POST, requiredFields)
    if verifiedRequestResponse['isMissingFields']:
        errorMessage = verifiedRequestResponse['errorMessage']
        return formattedResponse(isError=True, errorMessage=errorMessage)

    # verify jobToPost object
    try:
        requiredFields = ['name', 'compensation', 'description', 'city',
                          'state', 'titles', 'skills']
        verifiedRequestResponse = verifyRequest(json.loads(request.POST[
            'jobToPost']), requiredFields)
        if verifiedRequestResponse['isMissingFields']:
            errorMessage = verifiedRequestResponse['errorMessage']
            return formattedResponse(isError=True, errorMessage=errorMessage)
    except:
        errorMessage = 'jobToPost was not a valid JSON'
        return formattedResponse(isError=True, errorMessage=errorMessage)

    request = request.POST

    userId = request['userId']
    nonprofitId = request['nonprofitId']
    jobToPost = json.loads(request['jobToPost'])

    if Account.objects.filter(userId=userId).exists():
        if Nonprofit.objects.filter(pk=nonprofitId).exists():
            if NonprofitRelation.objects.filter(userId=userId,
                                                nonprofitId=nonprofitId).exists():
                nonprofit = Nonprofit.objects.get(pk=nonprofitId)

                newPostedJob, isNewPostedJobCreated = PostedJob.objects \
                    .get_or_create(
                    name=jobToPost['name'],
                    compensation=jobToPost['compensation'],
                    description=jobToPost['description'],
                    city=jobToPost['city'],
                    state=jobToPost['state'],
                    nonprofit=nonprofit
                )

                if isNewPostedJobCreated:
                    # add skills
                    for skill in jobToPost['skills']:
                        PostedJobSkill.objects.create(
                            job=newPostedJob,
                            skill=skill
                        )

                    for title in jobToPost['titles']:
                        PostedJobTitle.objects.create(
                            job=newPostedJob,
                            title=title
                        )

                else:
                    errorMessage = 'Failed to post job, job already exists'
                    return formattedResponse(isError=True,
                                             errorMessage=errorMessage)
            else:
                errorMessage = 'User is not an affiliate of the nonprofit'
                return formattedResponse(isError=True,
                                         errorMessage=errorMessage)
        else:
            errorMessage = 'Unknown nonprofit'
            return formattedResponse(isError=True,
                                     errorMessage=errorMessage)
    else:
        errorMessage = 'Unknown user'
        return formattedResponse(isError=True, errorMessage=errorMessage)

    updatedNonprofitPostedJobModel = {
        'nonprofitPostedJobs': formatJobs(
            getNonprofitPostedJobs(nonprofit),
            jobType=POSTED_JOB_TYPE
        ),
        'newPostedJob': formatJob(
            newPostedJob,
            jobType=POSTED_JOB_TYPE
        )
    }

    return formattedResponse(data=updatedNonprofitPostedJobModel)


def applyToJob(request):
    '''
    Required fields:
        userId
        jobId
    '''

    requiredFields = ['userId', 'jobId']
    verifiedRequestResponse = verifyRequest(request.POST, requiredFields)
    if verifiedRequestResponse['isMissingFields']:
        errorMessage = verifiedRequestResponse['errorMessage']
        return formattedResponse(isError=True, errorMessage=errorMessage)

    request = request.POST

    userId = request['userId']
    jobId = request['jobId']

    if Account.objects.filter(userId=userId).exists():
        if PostedJob.objects.filter(pk=jobId).exists():
            applicant = Account.objects.get(userId=userId)
            job = PostedJob.objects.get(pk=jobId)

            newJobApplication, isNewApplication = PostedJobApplication \
                .objects.get_or_create(
                applicant=applicant,
                job=job
            )

            if isNewApplication:
                allJobsAsApplicant = getPostedJobsAsApplicant(applicant)
                formattedJobsAsApplicant = formatJobs(allJobsAsApplicant,
                                                      jobType=POSTED_JOB_TYPE)

                newJobAsApplicant = formatJob(newJobApplication.job,
                                              jobType=POSTED_JOB_TYPE)

            else:
                errorMessage = 'User has already applied to that job'
                return formattedResponse(isError=True,
                                         errorMessage=errorMessage)

        else:
            errorMessage = 'Unknown job'
            return formattedResponse(isError=True, errorMessage=errorMessage)
    else:
        errorMessage = 'Unknown user'
        return formattedResponse(isError=True, errorMessage=errorMessage)

    jobsAsApplicantData = {
        'jobsAsApplicant': formattedJobsAsApplicant,
        'newJobAsApplicant': newJobAsApplicant
    }

    return formattedResponse(data=jobsAsApplicantData)


def acceptApplicant(request):
    '''
    Required fields:
        applicantId
        affiliateId
        nonprofitId
        jobId
    '''

    requiredFields = ['affiliateId', 'applicantId', 'jobId', 'nonprofitId']
    verifiedRequestResponse = verifyRequest(request.POST, requiredFields)
    if verifiedRequestResponse['isMissingFields']:
        errorMessage = verifiedRequestResponse['errorMessage']
        return formattedResponse(isError=True, errorMessage=errorMessage)

    request = request.POST

    applicantId = request['applicantId']
    affiliateId = request['affiliateId']
    nonprofitId = request['nonprofitId']
    jobId = request['jobId']

    if Account.objects.fillter(userId=applicantId).exists():
        if Account.objects.filter(userId=affiliateId).exists():
            if NonprofitRelation.objects.filter(
                    userId=affiliateId,
                    nonprofitId=nonprofitId
            ).exists():
                if PostedJob.objects.filter(pk=jobId).exists():
                    jobToTake = PostedJob.objects.get(pk=jobId)

                    if str(jobToTake.nonprofit.pk) == nonprofitId:
                        nonprofitEmployer = jobToTake.nonprofit
                        userEmployee = Account.objects.get(userId=applicantId)

                        jobName = str(jobToTake.name)
                        jobDescription = str(jobToTake.description)
                        jobCompensation = str(jobToTake.compensation)
                        jobCity = str(jobToTake.city)
                        jobState = str(jobToTake.state)
                        jobTimeCreated = jobToTake.timeCreated

                        newCurrentJob, isNewCurrentJobCreated = CurrentJob \
                            .objects.get_or_create(
                            employee=userEmployee,
                            nonprofit=nonprofitEmployer,
                            name=jobName,
                            description=jobDescription,
                            compensation=jobCompensation,
                            state=jobState,
                            city=jobCity,
                            timeCreated=jobTimeCreated
                        )

                        if isNewCurrentJobCreated:
                            jobToTake.delete()

                            postedJobsModel = formatJobs(
                                getNonprofitPostedJobs(nonprofitEmployer),
                                POSTED_JOB_TYPE
                            )
                            currentJobsModel = formatJobs(
                                getNonprofitCurrentJobs(nonprofitEmployer),
                                CURRENT_JOB_TYPE
                            )
                            newCurrentJobModel = formatJob(
                                newCurrentJob,
                                CURRENT_JOB_TYPE
                            )

                        else:
                            errorMessage = 'Failed to accept applicant'
                            return formattedResponse(isError=True,
                                                     errorMessage=errorMessage)
                    else:
                        errorMessage = 'Job is not associated with the ' \
                                       'provided nonprofit'
                        return formattedResponse(isError=True,
                                                 errorMessage=errorMessage)
                else:
                    errorMessage = 'Unknown job'
                    return formattedResponse(isError=True,
                                             errorMessage=errorMessage)
            else:
                errorMessage = 'The suggested affiliate is not an affiliate of ' \
                               'the nonprofit'
                return formattedResponse(isError=True,
                                         errorMessage=errorMessage)
        else:
            errorMessage = 'Unknown user: affiliate'
            return formattedResponse(isError=True, errorMessage=errorMessage)
    else:
        errorMessage = 'Unknown user: applicant'
        return formattedResponse(isError=True, errorMessage=errorMessage)

    updatedNonprofitJobModels = {
        'postedJobs': postedJobsModel,
        'currentJobs': currentJobsModel,
        'newCurrentJob': newCurrentJobModel
    }

    return formattedResponse(data=updatedNonprofitJobModels)


def viewOtherProfile(request):
    '''
    Required fields:
        userId
    '''

    requiredFields = ['userId']
    verifiedRequestResponse = verifyRequest(request.POST, requiredFields)
    if verifiedRequestResponse['isMissingFields']:
        errorMessage = verifiedRequestResponse['errorMessage']
        return formattedResponse(isError=True, errorMessage=errorMessage)

    request = request.POST

    userId = request['userId']

    if Account.objects.filter(userId=userId).exists():
        userToView = Account.objects.get(userId=userId)
        userToViewModel = getUserModel(userToView)
    else:
        errorMessage = 'Unknown user'
        return formattedResponse(isError=True, errorMessage=errorMessage)

    otherProfileData = {
        'userToView': userToViewModel
    }

    return formattedResponse(data=otherProfileData)


def viewJob(request):
    '''
    Required fields:
        jobId
        jobType
    '''

    requiredFields = ['jobId', 'jobType']
    verifiedRequestResponse = verifyRequest(request.POST, requiredFields)
    if verifiedRequestResponse['isMissingFields']:
        errorMessage = verifiedRequestResponse['errorMessage']
        return formattedResponse(isError=True, errorMessage=errorMessage)

    request = request.POST
    jobId = request['jobId']
    jobType = request['jobType']

    jobToView = getJob(jobId=jobId, jobType=jobType)

    if jobToView is not None:
        jobToViewModel = formatJob(
            job=jobToView,
            jobType=jobType
        )

    else:
        errorMessage = 'Unknown job'
        return formattedResponse(isError=True, errorMessage=errorMessage)

    jobData = {
        'jobToView': jobToViewModel
    }

    return formattedResponse(data=jobData)


def viewNonprofit(request):
    '''
    Required fields:
        nonprofitId
    '''

    requiredFields = ['nonprofitId']
    verifiedRequestResponse = verifyRequest(request.POST, requiredFields)
    if verifiedRequestResponse['isMissingFields']:
        errorMessage = verifiedRequestResponse['errorMessage']
        return formattedResponse(isError=True, errorMessage=errorMessage)

    request = request.POST

    nonprofitId = request['nonprofitId']

    if Nonprofit.objects.filter(pk=nonprofitId).exists():
        nonprofitToView = Nonprofit.objects.get(pk=nonprofitId)
        nonprofitToViewModel = getNonprofitModel(nonprofitToView)

    else:
        errorMessage = 'Unknown nonprofit'
        return formattedResponse(isError=True, errorMessage=errorMessage)

    nonprofitData = {
        'nonprofitToView': nonprofitToViewModel
    }

    return formattedResponse(data=nonprofitData)


def getPostedJobs(request):
    '''
    Required fields:
        query
    '''

    requiredFields = ['query']
    verifiedRequestResponse = verifyRequest(request.POST, requiredFields)
    if verifiedRequestResponse['isMissingFields']:
        errorMessage = verifiedRequestResponse['errorMessage']
        return formattedResponse(isError=True, errorMessage=errorMessage)

    request = request.POST

    # currently ignoring query

    postedJobs = PostedJob.objects.all()
    formattedPostedJobs = formatJobs(postedJobs, jobType=POSTED_JOB_TYPE)

    postedJobsData = {
        'postedJobs': formattedPostedJobs
    }
    return formattedResponse(data=postedJobsData)


def getNonprofits(request):
    '''
    Required fields:
        query
    '''

    requiredFields = ['query']
    verifiedRequestResponse = verifyRequest(request.POST, requiredFields)
    if verifiedRequestResponse['isMissingFields']:
        errorMessage = verifiedRequestResponse['errorMessage']
        return formattedResponse(isError=True, errorMessage=errorMessage)

    request = request.POST

    # currently ignoring query

    nonprofits = Nonprofit.objects.all()
    formattedNonprofits = formatNonprofitsForUserModel(nonprofits)

    nonprofitsData = {
        'nonprofits': formattedNonprofits
    }

    return formattedResponse(data=nonprofitsData)


def getOtherUsers(request):
    '''
    Required fields:
        query
        userId
    '''

    requiredFields = ['query', 'userId']
    verifiedRequestResponse = verifyRequest(request.POST, requiredFields)
    if verifiedRequestResponse['isMissingFields']:
        errorMessage = verifiedRequestResponse['errorMessage']
        return formattedResponse(isError=True, errorMessage=errorMessage)

    request = request.POST

    userId = request['userId']
    # currently ignoring query
    allUsers = Account.objects.all()
    otherUsers = filter(lambda accountObject: str(accountObject.userId) !=
                                              userId, allUsers)

    formattedOtherUsers = formatUsersForAfilliationOrApplications(otherUsers)

    otherUsersData = {
        'otherUsers': formattedOtherUsers
    }

    return formattedResponse(data=otherUsersData)

