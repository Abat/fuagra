from django.shortcuts import render
from rest_framework import generics
from siteModel.models import News
from siteModel.serializers import NewsSerializer, UserSerializer
from siteModel.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from datetime import datetime

# Create your views here.
def index(request):
    context = {} 

    # Get the number of visits to the site.
    visits = request.session.get('visits')
    if not visits:
        visits = 1
    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    # check if last_visit cookie exists
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
        
        # cookie is more than a day old
        if (datetime.now() - last_visit_time).seconds > 5:
            visits = visits + 1
            reset_last_visit_time = True
    else:
        # Cookie doesn't exist
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits
    context['visits'] = visits

    return render(request, 'siteModel/index.html', context)

def about(request):
    context = {} 
    return render(request, 'siteModel/about.html', context)

# User Registration/Authentication

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'avatar' in request.FILES:
                profile.avatar = request.FILES['avatar']

            profile.save()
            registered = True

        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'siteModel/register.html', {'user_form':user_form,
     'profile_form':profile_form,
      'registered':registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Your Account is disabled.")
        else:
            print("Invalid login details :{0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'siteModel/login.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

# JSON starts here

class NewsList(generics.ListCreateAPIView):
    """
    List all news or create a new news.
    """
    queryset = News.objects.all()
    serializer_class = NewsSerializer

class NewsDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a code snippet.
    """
    queryset = News.objects.all()
    serializer_class = NewsSerializer

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
