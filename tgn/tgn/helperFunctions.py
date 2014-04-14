'''
These functions are used in views.py as helper functions
to views functions used for the server-to-client interaction
'''

from models import Account, PostedJob, CurrentJob, CompletedJob, UserSkill, \
    PostedJobSkill, CurrentJobSkill, CompletedJobSkill, UserProfileImage, \
    NonprofitProfileImage, NonprofitRelations


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
        'description': str(job.jobDescription),
        'compensation': str(job.jobCompensation),
        'jobId': str(job.pk),
        'timeCreated': str(job.timeCreated),
        'skills': formatSkills(skills)
    }

    if hasEmployee:
        formattedJob['employeeId'] = str(job.employee.userId)
        formattedJob['employeeFirstName'] = str(job.employee.firstName)
        formattedJob['employeeLastName'] = str(job.employee.lastName)
        formattedJob['employeeProfileImageUrl'] = str(
            UserProfileImage
            .objects
            .get(
                account=job.employee
            )
            .profileImageUrl)

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
            
            if hasStrength:
                formattedSkill = {
                    'skill': str(skill.skill),
                    'strength': str(skill.strength)
                }
            else:
                formattedSkill = str(skill.skill)

            formattedSkills.append(formattedSkill)

    return formattedSkills
