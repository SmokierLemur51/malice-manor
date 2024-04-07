from django.shortcuts import render

MARKET = "Malice Manor Market"

# Create your views here.
def index(request):
    context = {"title": MARKET}
    render(request, "index.html", context)


def about(request):
    context = {"title": MARKET}
    render(request, "about.html", context)
