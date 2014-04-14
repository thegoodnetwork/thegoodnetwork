'''
These functions are used in views.py as helper functions
to views functions used for the server-to-client interaction
'''

from models import Account, PostedJob, CurrentJob, CompletedJob, UserSkill, \
    PostedJobSkill, CurrentJobSkill, CompletedJobSkill, UserProfileImage, \
    NonprofitProfileImage, NonprofitRelations, Nonprofit


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
    if not hasEmployee:
        skills = PostedJobSkill.objects.filter(job=job)
    else:
        skills = CurrentJobSkill.objects.filter(job=job) if \
            CurrentJobSkill.objects.filter(job=job).exists() else \
            CompletedJobSkill.objects.filter(job=job)

    formattedJob = {
        'nonprofitId': str(job.nonprofit.pk),
        'nonprofitName': str(job.nonprofit.name),
        #'employerProfileImageUrl': str(
        #    ProfileImage
        #   .objects
        #    .get(
        #        account=job.employer
        #    )
        #    .profileImageUrl),
        'title': str(job.title),
        'description': str(job.description),
        'compensation': str(job.compensation),
        'city': str(job.city),
        'state': str(job.state),
        'jobId': str(job.pk),
        'timeCreated': str(job.timeCreated),
        'skills': formatSkills(skills)
    }

    if hasEmployee:
        formattedJob['employeeId'] = str(job.employee.userId)
        formattedJob['employeeFirstName'] = str(job.employee.firstName)
        formattedJob['employeeLastName'] = str(job.employee.lastName)
        formattedJob['employeeProfileImageUrl'] = getUserProfileImageUrl(job
                                                                         .employee)

    return formattedJob


def formatJobs(jobs, hasEmployee=False):
    formattedJobs = None

    if jobs is not None:
        formattedJobs = []
        for job in jobs:
            formattedJob = formatJob(job, hasEmployee=hasEmployee)
            formattedJobs.append(formattedJob)

    return formattedJobs


def formatSkills(skills, hasStrength=False):
    formattedSkills = None

    if skills is not None:
        formattedSkills = []
        for skill in skills:
            formattedSkill = str(skill.skill)
            formattedSkills.append(formattedSkill)

    return formattedSkills


def getUserProfileImageUrl(account):
    return None if not UserProfileImage.objects.filter(account=account) \
        .exists() else str(UserProfileImage.objects.get(account=account).url)


def getUserModel(account):
    userId = str(account.userId)
    firstName = str(account.firstName)
    lastName = str(account.lastName)
    aboutMe = str(account.aboutMe)
    profileImageUrl = getUserProfileImageUrl(account)

    # get user-specific jobs
    currentJobsAsEmployee = None if not CurrentJob.objects.filter(
        employee=account).exists() else \
        formatJobs(
            CurrentJob.objects.filter(employee=account),
            hasEmployee=True
        )

    completedJobsAsEmployee = None if not CompletedJob.objects.filter(
        employee=account).exists() else \
        formatJobs(
            CompletedJob.objects.filter(employee=account),
            hasEmployee=True
        )

    jobs = {
        'currentJobsAsEmployee': currentJobsAsEmployee,
        'completedJobsAsEmployee': completedJobsAsEmployee
    }

    # get skills
    skills = None if not UserSkill.objects.filter(
        account=account).exists() else formatSkills(
        UserSkill.objects.get(account=account), hasStrength=True)

    # get nonprofits
    nonprofitRelations = None if not NonprofitRelations.objects.filter(
        userId=userId) \
        .exists() else NonprofitRelations.objects.filter(userId=userId)

    nonprofits = []
    if nonprofitRelations is not None:
        for relation in nonprofitRelations:
            nonprofit = Nonprofit.objects.get(pk=relation.nonprofitId)
            nonprofits.append({
                'nonprofitId': nonprofit.pk,
                'name': nonprofit.name,
            })

    userModel = {
        'userId': userId,
        'profileImageUrl': profileImageUrl,
        'firstName': firstName,
        'lastName': lastName,
        'aboutMe': aboutMe,
        'skills': skills,
        'jobs': jobs,
        'nonprofits': nonprofits
    }

    return userModel


def getNonprofitModel(nonprofit):
    nonprofitId = str(nonprofit.pk)
    name = str(nonprofit.name)
    mission = str(nonprofit.mission)
    description = str(nonprofit.description)

    # get the jobs associated with the nonprofit
    postedJobs = None if not PostedJob.objects.filter(nonprofit=nonprofit) \
        .exists() else formatJobs(PostedJob.objects.filter(nonprofit=nonprofit))

    currentJobs = None if not CurrentJob.objects.filter(nonprofit=nonprofit) \
        .exists() else formatJobs(
        CurrentJob.objects.filter(nonprofit=nonprofit),
        hasEmployee=True
    )

    completedJobs = None if not CompletedJob.objects.filter(
        nonprofit=nonprofit) \
        .exists() else formatJobs(
        CompletedJob.objects.filter(nonprofit=nonprofit),
        hasEmployee=True
    )

    jobs = {
        'postedJobs': postedJobs,
        'currentJobs': currentJobs,
        'completedJobs': completedJobs
    }

    # get the nonprofit affiliates
    nonprofitRelations = None if not NonprofitRelations.objects.filter(
        nonprofitId=nonprofit.pk).exists() else NonprofitRelations.objects \
        .filter(nonprofitId=nonprofit.pk)

    nonprofitAffiliates = []
    if nonprofitRelations is not None:
        for relation in nonprofitRelations:
            nonprofitAffiliate = Account.objects.get(userId=str(relation
                                                                .userId))
            nonprofitAffiliates.append({
                'userId': str(nonprofitAffiliate.userId),
                'firstName': str(nonprofitAffiliate.firstName),
                'lastName': str(nonprofitAffiliate.lastName),
                'profileImageUrl': getUserProfileImageUrl(nonprofitAffiliate)
            })

    nonprofitModel = {
        'nonprofitId': nonprofitId,
        'name': name,
        'mission': mission,
        'description': description,
        'jobs': jobs,
        'affiliates': nonprofitAffiliates
    }

    return nonprofitModel