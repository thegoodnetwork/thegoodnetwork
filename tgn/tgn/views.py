from django.shortcuts import render_to_response


def index(request):
    return render_to_response('index.html')

def login(request):
    return render_to_response('partials/login.html')

def myProfile(request):
    return render_to_response('partials/myProfile.html')

def otherProfile(request):
    return render_to_response('partials/otherProfile.html')

def myNonprofit(request):
    return render_to_response('partials/myNonprofit.html')

def otherNonprofit(request):
    return render_to_response('partials/otherNonprofit.html')

def myJob(request):
    return render_to_response('partials/myJob.html')

def jobApplicants(request):
    return render_to_response('partials/jobApplicants.html')

def searchResults(request):
    return render_to_response('partials/searchResults.html')
