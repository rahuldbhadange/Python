from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template

# Don't Repeat Yourself : DRY


def home_page(request):
    my_title = "Homepage"
    context = {"title": my_title, "my_list": [1, 2, 3, 4, 5, 6]}
    return render(request, "home.html", context)    # authentication is due to settings /TEMPLATES/context_processors


def home_page_if(request):
    my_title = "Homepage"
    context = {'title': my_title}
    if request.user.is_authenticated:
        context = {"title": my_title, "my_list": [1, 2, 3, 4, 5, 6]}
    return render(request, "home1.html", context)    # authentication is due to settings /TEMPLATES/context_processors


def about_page(request):
    return render(request, "about.html", {"title": "About Us"})
    # return HttpResponse("<h1>About Us</h1>")


def contact_page(request):
    return render(request, "contact.html", {"title": "Contact Us", "phone": '9110444828'})
    # return HttpResponse("<h1>Contact Us</h1>")


def example_page(request):
    context = {"title": "example"}
    template_name = "contact.html"
    template_obj = get_template(template_name)  # getting template result
    rendered_item = template_obj.render(context)
    return HttpResponse()   # rendering the response as per template and context


def home_page_experiment(request):
    my_title = "Homepage"
    context = {"title": my_title}
    template_name = "title.txt"
    template_obj = get_template(template_name)  # getting template result
    rendered_string = template_obj.render(context)
    return render(request, "hello_world.html", {"title": rendered_string})
    # return render(request, "hello_world.html", {"title": my_title})
