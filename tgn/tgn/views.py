from django.shortcuts import render_to_response


def test(request):
    return render_to_response("index.html")


def fbtest(request):
    return render_to_response('fbloginindex.html')


def profile(request):
    return render_to_response('profile.html')


def otherProfile(request):
    return render_to_response('otherProfile.html')


def otherNonprofit(request):
    return render_to_response('otherNonprofit.html')


def myNonprofit(request):
    return render_to_response('myNonprofit.html')


def myJob(request):
    return render_to_response('myJob.html')


def searchResults(request):
    return render_to_response('searchResults.html')
