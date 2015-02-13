from django.shortcuts import render

# Create your views here.
def index(request):
    context = {} 
    return render(request, 'siteModel/index.html', context)

def about(request):
    context = {} 
    return render(request, 'siteModel/about.html', context)
