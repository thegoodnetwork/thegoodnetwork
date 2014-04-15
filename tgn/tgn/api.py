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
        requiredFields = ['aboutMe', 'titles', 'skills']
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
        'aboutMe': str(account.aboutMe)
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
            NonprofitRelations.objects.create(
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

