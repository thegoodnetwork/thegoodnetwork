from django.shortcuts import render_to_response


def test(request):
    return render_to_response("index.html")


def fbtest(request):
    return render_to_response('fbloginindex.html')


def loggedIn(request):
    return render_to_response('loggedIn.html');

