from django.http import HttpResponse
from django.shortcuts import render_to_response

from helperFunctions import *

from django.forms.util import ValidationError
from open_facebook.api import FacebookAuthorization, OpenFacebook
from django_facebook.auth_backends import FacebookBackend

import json


def test(request):
    return render_to_response("index.html")


def fbtest(request):
    return render_to_response('fbloginindex.html')


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

def loggedIn(request):
    return render_to_response('loggedIn.html');
