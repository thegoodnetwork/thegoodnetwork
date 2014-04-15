from django.shortcuts import render_to_response


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

def profile(request):
    return render_to_response('profile.html');

def otherProfile(request):
    return render_to_response('otherProfile.html');

def otherNonprofit(request):
    return render_to_response('otherNonprofit.html');
