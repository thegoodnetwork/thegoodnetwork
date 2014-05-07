from django.shortcuts import render_to_response


def index(request):
    return render_to_response('index.html')

def login(request):
    return render_to_response('partials/login.html')

def myProfile(request):
    return render_to_response('partials/myProfile.html')