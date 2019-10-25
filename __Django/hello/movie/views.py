from django.http import HttpResponse

def index(request):
    return HttpResponse("<h1> hello friends this is a movie page </h1>")


def details(request, MovieName_id):
    return HttpResponse("<h1> welcome in id :" + str(MovieName_id) + "</h1>")

