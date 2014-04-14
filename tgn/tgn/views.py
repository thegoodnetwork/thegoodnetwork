from django.http import HttpResponse
from django.shortcuts import render_to_response

from helperFunctions import *

from django.forms.util import ValidationError
from open_facebook.api import FacebookAuthorization, OpenFacebook
from django_facebook.auth_backends import FacebookBackend

import json

FBOpen = OpenFacebook


def test(request):
    return render_to_response("index.html")


def fbtest(request):
    return render_to_response('fbloginindex.html')


def loggedIn(request):
    return render_to_response('loggedIn.html');

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
    userId = userInfo['userId']

    account, isAccountCreated = Account.objects.get_or_create(
        userId=userId,
        name=userName
    )

    if isAccountCreated:
        titles = []
        aboutMe = ''
        jobs = {}
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

