from django.shortcuts import render


def index(request):
    """ Returns the home page """

    return render(request, 'home/index.html')
