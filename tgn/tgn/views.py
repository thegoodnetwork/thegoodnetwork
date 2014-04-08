from django.http import render_to_response

def test(request):
    return render_to_response("index.html")
