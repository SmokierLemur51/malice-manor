from django.shortcuts import render

MARKET = "Malice Manor Market"

# Create your views here.
def index(request):
    context = {"title": MARKET}
    render(request, "non_authenticated/index.html", context)


def about(request):
    context = {"title": MARKET}
    render(request, "non_authenticated/about.html", context)
