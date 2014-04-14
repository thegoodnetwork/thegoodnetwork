'''
These functions are used in views.py as helper functions
to views functions used for the server-to-client interaction
'''

from models import Account, PostedJob, CurrentJob, CompletedJob, UserSkill, \
    PostedJobSkill, CurrentJobSkill, CompletedJobSkill, UserProfileImage, \
    NonprofitProfileImage, NonprofitRelations, Nonprofit, UserTitle, \
    PostedJobTitle, CurrentJobTitle, CompletedJobTitle


def verifyRequest(request, requiredFields):
    params = request.POST
    isMissingFields = False
    missingFields = []
    errorMessage = None
    for field in requiredFields:
        if not field in params:
            isMissingFields = True
            missingFields.append(field)

    if isMissingFields:
        errorMessage = 'Request is missing: ' + str(missingFields)

    return {
        'isMissingFields': isMissingFields,
        'errorMessage': errorMessage,
        'requestAsPost': request.POST
    }


def formatJob(job, hasEmployee=False):
    formattedJob = {
        'nonprofitId': str(job.nonprofit.pk),
        'nonprofitName': str(job.nonprofit.name),
        'titles': formatTitles(getJobTitles(job, hasEmployee=hasEmployee)),
        'description': str(job.description),
        'compensation': str(job.compensation),
        'city': str(job.city),
        'state': str(job.state),
        'jobId': str(job.pk),
        'timeCreated': str(job.timeCreated),
        'skills': formatSkills(getJobSkills(job, hasEmployee=hasEmployee))
    }

    if hasEmployee:
        formattedJob['employeeId'] = str(job.employee.userId)
        formattedJob['employeeFirstName'] = str(job.employee.firstName)
        formattedJob['employeeLastName'] = str(job.employee.lastName)
        formattedJob['employeeProfileImageUrl'] = getUserProfileImageUrl(
            job.employee
        )
        formattedJob['timeTaken'] = str(job.timeTaken)

    return formattedJob


def formatJobs(jobs, hasEmployee=False):
    formattedJobs = None

    if jobs is not None:
        formattedJobs = []
        for job in jobs:
            formattedJob = formatJob(job, hasEmployee=hasEmployee)
            formattedJobs.append(formattedJob)

    return formattedJobs


def formatSkills(skills):
    return map(lambda skillObject: str(skillObject.skill), skills)


def formatTitles(titles):
    return map(lambda titleObject: str(titleObject.title), titles)


def getUserProfileImageUrl(account):
    return None if not UserProfileImage.objects.filter(account=account) \
        .exists() else str(UserProfileImage.objects.get(account=account).url)


def getJobSkills(job, hasEmployee=False):
    if not hasEmployee:
        skills = PostedJobSkill.objects.filter(job=job)
    else:
        skills = CurrentJobSkill.objects.filter(job=job) if \
            CurrentJobSkill.objects.filter(job=job).exists() else \
            CompletedJobSkill.objects.filter(job=job)

    return skills


def getJobTitles(job, hasEmployee=False):
    if not hasEmployee:
        titles = PostedJobTitle.objects.filter(job=job)
    else:
        titles = CurrentJobTitle.objects.filter(job=job) if \
            CurrentJobTitle.objects.filter(job=job).exists() else \
            CompletedJobTitle.filter(job=job)

    return titles


def getUserSkills(account):
    skills = None if not UserSkill.objects.filter(account=account).exists() \
        else UserSkill.objects.filter(account=account)

    return skills


def getCurrentJobsAsEmployee(account):
    currentJobsAsEmployee = None if not CurrentJob.objects.filter(
        employee=account).exists() else \
        CurrentJob.objects.filter(employee=account)

    return currentJobsAsEmployee


def getCompletedJobsAsEmpployee(account):
    completedJobsAsEmployee = None if not CompletedJob.objects.filter(
        employee=account).exists() else \
        CompletedJob.objects.filter(employee=account)

    return completedJobsAsEmployee


def getUserNonprofits(account):
    userId = str(account.userId)
    nonprofitRelations = NonprofitRelations.objects.filter(userId=userId) if \
        NonprofitRelations.objects.filter(userId=userId).exists() else None

    nonprofits = []
    if nonprofitRelations is not None:
        for relation in nonprofitRelations:
            nonprofit = Nonprofit.objects.get(pk=str(relation.nonprofitId))
            nonprofits.append(nonprofit)

    return nonprofits


def getUserTitles(account):
    titles = UserTitle.objects.filter(account=account)
    return titles


def getUserModel(account):
    userId = str(account.userId)
    firstName = str(account.firstName)
    lastName = str(account.lastName)
    aboutMe = str(account.aboutMe)
    profileImageUrl = getUserProfileImageUrl(account)
    titles = formatTitles(getUserTitles(account))

    # get user-specific jobs
    currentJobsAsEmployee = formatJobs(getCurrentJobsAsEmployee(account),
                                       hasEmployee=True)
    completedJobsAsEmployee = formatJobs(getCompletedJobsAsEmpployee(account),
                                         hasEmployee=True)

    jobs = {
        'currentJobsAsEmployee': currentJobsAsEmployee,
        'completedJobsAsEmployee': completedJobsAsEmployee
    }

    # get skills
    skills = formatSkills(getUserSkills(account))

    # get nonprofits
    unformattedUserNonprofits = getUserNonprofits(account)
    formattedUserNonprofits = map(lambda nonprofitObject: {
        'nonprofitId': str(nonprofitObject.pk),
        'name': str(nonprofitObject.name),
        'mission': str(nonprofitObject.mission)},
                                  unformattedUserNonprofits)

    userModel = {
        'userId': userId,
        'profileImageUrl': profileImageUrl,
        'firstName': firstName,
        'lastName': lastName,
        'aboutMe': aboutMe,
        'titles': titles,
        'skills': skills,
        'jobs': jobs,
        'nonprofits': formattedUserNonprofits
    }

    return userModel


def getNonprofitPostedJobs(nonprofit):
    postedJobs = PostedJob.objects.filter(nonprofit=nonprofit) if \
        PostedJob.objects.filter(nonprofit=nonprofit).exists() else None

    return postedJobs


def getNonprofitCurrentJobs(nonprofit):
    currentJobs = CurrentJob.objects.filter(nonprofit=nonprofit) if \
        CurrentJob.objects.filter(nonprofit=nonprofit).exists() else None

    return currentJobs


def getNonprofitCompletedJobs(nonprofit):
    completedJobs = CompletedJob.objects.filter(nonprofit=nonprofit) if \
        CompletedJob.objects.filter(nonprofit=nonprofit).exists() else None

    return completedJobs


def getNonprofitAffiliates(nonprofit):
    nonprofitId = str(nonprofit.pk)
    nonprofitRelations = NonprofitRelations.objects.filter(
        nonprofitId=nonprofitId) if \
        NonprofitRelations.objects.filter(nonprofitId=nonprofitId).exists() \
        else None

    nonprofitAffiliates = []
    if nonprofitRelations is not None:
        for relation in nonprofitRelations:
            nonprofitAffiliate = Account.objects.get(userId=str(relation
                                                                .userId))
            nonprofitAffiliates.append(nonprofitAffiliate)

    return nonprofitAffiliates


def getNonprofitModel(nonprofit):
    nonprofitId = str(nonprofit.pk)
    name = str(nonprofit.name)
    mission = str(nonprofit.mission)
    description = str(nonprofit.description)

    # get the jobs associated with the nonprofit
    postedJobs = formatJobs(getNonprofitPostedJobs(nonprofit))
    currentJobs = formatJobs(getNonprofitCurrentJobs(nonprofit),
                             hasEmployee=True)
    completedJobs = formatJobs(getNonprofitCompletedJobs(nonprofit),
                               hasEmployee=True)

    jobs = {
        'postedJobs': postedJobs,
        'currentJobs': currentJobs,
        'completedJobs': completedJobs
    }

    # get the nonprofit affiliates

    nonprofitAffiliates = map(lambda affiliateObject: {
        'userId': str(affiliateObject.userId),
        'firstName': str(affiliateObject.firstName),
        'lastName': str(affiliateObject.lastName),
        'profielImageUrl': getUserProfileImageUrl(affiliateObject)
    }, getNonprofitAffiliates(nonprofit))

    nonprofitModel = {
        'nonprofitId': nonprofitId,
        'name': name,
        'mission': mission,
        'description': description,
        'jobs': jobs,
        'affiliates': nonprofitAffiliates
    }

    return nonprofitModel