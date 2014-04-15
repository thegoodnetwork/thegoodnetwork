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

    verifiedRequestResponse = verifyRequest(request, requiredFields)
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
    requiredFields = ['userId', 'profile']

    verifiedRequestResponse = verifyRequest(request, requiredFields)
    if verifiedRequestResponse['isMissingFields']:
        errorMessage = verifiedRequestResponse['errorMessage']
        return formattedResponse(isError=True, errorMessage=errorMessage)

    request = request.POST
    userId = request['userId']
    profile = json.loads(request['profile'])

    aboutMe = profile['aboutMe']
    titles = profile['titles']
    skills = profile['skills']

    if Account.objects.filter(userId=userId).exists():
        account = Account.objects.get(userId=userId)

        account.aboutMe = aboutMe

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
            title = str(title.title)
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
        'aboutMe': str(account.aboutMe)
    }

    return formattedResponse(data=updatedProfileModel)