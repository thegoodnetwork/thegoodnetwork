'''
These functions are used in views.py as helper functions
to views functions used for the server-to-client interaction
'''

from models import Account, PostedJob, CurrentJob, CompletedJob, UserSkill, \
    PostedJobSkill, CurrentJobSkill, CompletedJobSkill, UserProfileImage, \
    NonprofitProfileImage, NonprofitRelation, Nonprofit, UserTitle, \
    PostedJobTitle, CurrentJobTitle, CompletedJobTitle, PostedJobApplication, \
    NonprofitAffiliateRequest

POSTED_JOB_TYPE = 'postedJob'
CURRENT_JOB_TYPE = 'currentJob'
COMPLETED_JOB_TYPE = 'completedJob'


def verifyRequest(params, requiredFields):
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
    }


def formatJob(job, jobType):
    formattedJob = {
        'nonprofitId': str(job.nonprofit.pk),
        'nonprofitName': str(job.nonprofit.name),
        'nonprofitImageUrl': str(job.nonprofit.imageUrl),
        'titles': formatTitles(getJobTitles(job, jobType=jobType)),
        'description': str(job.description),
        'compensation': str(job.compensation),
        'city': str(job.city),
        'state': str(job.state),
        'name': str(job.name),
        'jobId': str(job.pk),
        'timeCreated': str(job.timeCreated),
        'skills': formatSkills(getJobSkills(job, jobType=jobType)),
        'jobType': jobType
    }

    if jobType == POSTED_JOB_TYPE:
        formattedJob['applicants'] = formatUsersForAffiliationOrApplications(
            getJobApplicants(job))
    else:
        formattedJob['employeeId'] = str(job.employee.userId)
        formattedJob['employeeName'] = str(job.employee.name)
        formattedJob['employeeProfileImageUrl'] = getUserProfileImageUrl(
            job.employee
        )
        formattedJob['timeTaken'] = str(job.timeTaken)

    if jobType == COMPLETED_JOB_TYPE:
        formattedJob['timeCompleted'] = str(job.timeCompleted)

    return formattedJob


def formatJobs(jobs, jobType):
    formattedJobs = []

    if jobs:
        formattedJobs = map(lambda jobObject: formatJob(jobObject,
                                                        jobType=jobType),
                            jobs
        )

    return formattedJobs


def formatSkills(skills):
    return map(lambda skillObject: str(skillObject.skill), skills)


def formatTitles(titles):
    return map(lambda titleObject: str(titleObject.title), titles)


def formatNonprofitForUserModel(nonprofit):
    formattedNonprofit = {
        'nonprofitId': str(nonprofit.pk),
        'name': str(nonprofit.name),
        'mission': str(nonprofit.mission)
    }

    return formattedNonprofit


def formatNonprofitsForUserModel(nonprofits):
    formattedNonprofits = map(lambda nonprofit: formatNonprofitForUserModel(
        nonprofit), nonprofits)

    return formattedNonprofits


def formatUserForAffiliationOrApplication(account):
    formattedUser = {
        'userId': str(account.userId),
        'name': str(account.name),
        'profileImageUrl': getUserProfileImageUrl(account),
        'titles': formatTitles(getUserTitles(account)),
        'skills': formatSkills(getUserSkills(account))
    }


    return formattedUser


def formatUsersForAffiliationOrApplications(accounts):
    print 'formatting: ' + str(accounts)
    formattedUsers = map(lambda account:
                         formatUserForAffiliationOrApplication(account),
                         accounts)

    return formattedUsers


def formatAffiliationRequest(affiliationRequest):
    formattedRequest = {
        'nonprofit': formatNonprofitForUserModel(affiliationRequest.nonprofit),
        'potentialAffiliate': formatUserForAffiliationOrApplication(
            affiliationRequest.potentialAffiliate)
    }

    return formattedRequest


def formatAffiliationRequests(affiliationRequests):
    formattedRequests = map(
        lambda request: formatAffiliationRequest(request),
        affiliationRequests
    )

    return formattedRequests


def getUserProfileImageUrl(account):
    return None if not UserProfileImage.objects.filter(account=account) \
        .exists() else str(UserProfileImage.objects.get(account=account).url)


def getUserAffiliationRequests(account):
    affiliationRequests = NonprofitAffiliateRequest.objects.filter(
        potentialApplicant=account)

    return affiliationRequests


def getJobSkills(job, jobType):
    skills = []
    if jobType == POSTED_JOB_TYPE:
        skills = PostedJobSkill.objects.filter(job=job)
    elif jobType == CURRENT_JOB_TYPE:
        skills = CurrentJobSkill.objects.filter(job=job)
    elif jobType == COMPLETED_JOB_TYPE:
        skills = CompletedJobSkill.objects.filter(job=job)

    return skills


def getJobApplicants(job):
    applications = PostedJobApplication.objects.filter(job=job)
    jobApplicants = map(lambda applicationObject: applicationObject.applicant,
                        applications)

    return jobApplicants


def getJobTitles(job, jobType):
    titles = []
    if jobType == POSTED_JOB_TYPE:
        titles = PostedJobTitle.objects.filter(job=job)
    elif jobType == CURRENT_JOB_TYPE:
        titles = CurrentJobTitle.objects.filter(job=job)
    elif jobType == COMPLETED_JOB_TYPE:
        titles = CompletedJobTitle.objects.filter(job=job)

    return titles


def getUserSkills(account):
    skills = UserSkill.objects.filter(account=account)

    return skills


def getPostedJobsAsApplicant(account):
    userJobApplications = PostedJobApplication.objects.filter(
        applicant=account)
    postedJobsAsApplicant = map(lambda applicationObject: applicationObject
                                .job, userJobApplications)

    return postedJobsAsApplicant


def getCurrentJobsAsEmployee(account):
    currentJobsAsEmployee = CurrentJob.objects.filter(employee=account)

    return currentJobsAsEmployee


def getCompletedJobsAsEmployee(account):
    completedJobsAsEmployee = CompletedJob.objects.filter(employee=account)

    return completedJobsAsEmployee


def getUserNonprofits(account):
    userId = str(account.userId)
    nonprofitRelations = NonprofitRelation.objects.filter(userId=userId) if \
        NonprofitRelation.objects.filter(userId=userId).exists() else None

    nonprofits = []
    if nonprofitRelations is not None:
        
        for relation in nonprofitRelations:
            print 'relation: ' + userId + ' ' + str(relation.nonprofitId)
            nonprofit = Nonprofit.objects.get(pk=str(relation.nonprofitId))
            nonprofits.append(nonprofit)

    return nonprofits


def getUserTitles(account):
    titles = UserTitle.objects.filter(account=account)
    return titles


def getUserModel(account):
    userId = str(account.userId)
    name = str(account.name)
    aboutMe = str(account.aboutMe)
    profileImageUrl = getUserProfileImageUrl(account)
    resume = str(account.resume)
    # get titles
    titles = formatTitles(getUserTitles(account))

    print 'got basic user model'
    # get user-specific jobs
    currentJobsAsApplicant = formatJobs(getPostedJobsAsApplicant(account),
                                        jobType=POSTED_JOB_TYPE)
    currentJobsAsEmployee = formatJobs(getCurrentJobsAsEmployee(account),
                                       jobType=CURRENT_JOB_TYPE)
    completedJobsAsEmployee = formatJobs(getCompletedJobsAsEmployee(account),
                                         jobType=COMPLETED_JOB_TYPE)

    jobs = {
        'jobsAsApplicant': currentJobsAsApplicant,
        'currentJobsAsEmployee': currentJobsAsEmployee,
        'completedJobsAsEmployee': completedJobsAsEmployee
    }

    print 'got jobs'
    # get skills
    skills = formatSkills(getUserSkills(account))

    # get nonprofits
    formattedUserNonprofits = map(lambda nonprofit: getNonprofitModel(
        nonprofit), getUserNonprofits(account))


    print 'got nonprofits'
    userModel = {
        'userId': userId,
        'resume': resume,
        'profileImageUrl': profileImageUrl,
        'name': name,
        'aboutMe': aboutMe,
        'titles': titles,
        'skills': skills,
        'jobs': jobs,
        'nonprofits': formattedUserNonprofits
    }

    return userModel


def getNonprofitPostedJobs(nonprofit):
    postedJobs = PostedJob.objects.filter(nonprofit=nonprofit)
    return postedJobs


def getNonprofitCurrentJobs(nonprofit):
    currentJobs = CurrentJob.objects.filter(nonprofit=nonprofit)
    return currentJobs


def getNonprofitCompletedJobs(nonprofit):
    completedJobs = CompletedJob.objects.filter(nonprofit=nonprofit)
    return completedJobs


def getNonprofitAffiliates(nonprofit):
    nonprofitId = str(nonprofit.pk)
    nonprofitRelations = NonprofitRelation.objects.filter(
        nonprofitId=nonprofitId)

    nonprofitAffiliates = []
    print 'getting affiliates ' + nonprofitId
    for relation in nonprofitRelations:
        nonprofitAffiliate = Account.objects.get(userId=str(relation
                                                            .userId))
        nonprofitAffiliates.append(nonprofitAffiliate)

    print 'finished getting affiliates'
    print str(nonprofitAffiliates)
    return nonprofitAffiliates


def getNonprofitAffiliateRequests(nonprofit):
    affiliateRequestsByNonprofit = NonprofitAffiliateRequest.objects.filter(
        nonprofit=nonprofit)

    return affiliateRequestsByNonprofit


def getNonprofitModel(nonprofit):
    nonprofitId = str(nonprofit.pk)
    name = str(nonprofit.name)
    mission = str(nonprofit.mission)
    description = str(nonprofit.description)
    website = str(nonprofit.website)
    address = str(nonprofit.address)
    imageUrl = str(nonprofit.imageUrl)

    print 'getting nonprofit ' + str(nonprofit.name)
    # get the jobs associated with the nonprofit
    postedJobs = formatJobs(getNonprofitPostedJobs(nonprofit),
                            jobType=POSTED_JOB_TYPE)
    currentJobs = formatJobs(getNonprofitCurrentJobs(nonprofit),
                             jobType=CURRENT_JOB_TYPE)
    completedJobs = formatJobs(getNonprofitCompletedJobs(nonprofit),
                               jobType=COMPLETED_JOB_TYPE)

    jobs = {
        'postedJobs': postedJobs,
        'currentJobs': currentJobs,
        'completedJobs': completedJobs
    }


    nonprofitAffiliates = formatUsersForAffiliationOrApplications(
       getNonprofitAffiliates(nonprofit)
    )

    #print 'getting affiliates: ' + str(nonprofitAffiliates)
    nonprofitModel = {
        'nonprofitId': nonprofitId,
        'name': name,
        'mission': mission,
        'description': description,
        'website': website,
        'address': address,
        'jobs': jobs,
        'affiliates': nonprofitAffiliates,
        'imageUrl': imageUrl
    }

    return nonprofitModel


def getJob(jobId, jobType):
    job = None

    if jobType == POSTED_JOB_TYPE:
        job = PostedJob.objects.get(pk=jobId) if PostedJob.objects.filter(
            pk=jobId).exists() else None

    elif jobType == CURRENT_JOB_TYPE:
        job = CurrentJob.objects.get(pk=jobId) if CurrentJob.objects.filter(
            pk=jobId).exists() else None

    elif jobType == COMPLETED_JOB_TYPE:
        job = CompletedJob.objects.get(pk=jobId) if CompletedJob.objects \
            .filter(pk=jobId).exists() else None

    return job
