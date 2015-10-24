from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets
from siteModel.models import News
from siteModel.models import UserProfile
from siteModel.models import Comments
from siteModel.serializers import NewsSerializer, UserSerializer, CommentSerializer
from siteModel.forms import UserForm, UserProfileForm
from siteModel.permissions import IsOwnerOrReadOnly
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

    # Get all News (write better solution later)
    news_list = News.objects.all()

    # Get the number of visits to the site.
    visits = request.session.get('visits')
    if not visits:
        visits = 0
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
    context['news_list'] = news_list

    return render(request, 'siteModel/index.html', context)

def about(request):
    context = {} 
    return render(request, 'siteModel/about.html', context)

def comments(request, pk):
    context = {}
    context['news_pk'] = pk
    return render(request, 'siteModel/comments.html', context)

def submit(request):
    context = {}
    return render(request, 'siteModel/submit.html', context)

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

class NewsViewSet(viewsets.ModelViewSet):

    serializer_class = NewsSerializer
    queryset = News.objects.all()
    model = News
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    def list(self, request, *args, **kwargs):
        """
        Return a list of News paginated by 20 items.
        Provide page number if necessary.
        """
        return super(NewsViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Return the News for a provided id
        """
        return super(NewsViewSet, self).retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Create news object.
        """
        return super(NewsViewSet, self).create(request, *args, **kwargs)

    def perform_create(self, serializer):
        # save the owner of the news
        serializer.save(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        """
        Update news object.
        Only the owner of the news can update it.
        """
        return super(NewsViewSet, self).update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Update part of news object. 
        Suggested to use this if you only need to update a single field.
        Only the owner of the news can patch it.
        """
        return super(NewsViewSet, self).partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Delete news. 
        Provide id of the news.
        Only the owner of the news can delete it.
        """
        return super(NewsViewSet, self).destroy(request, *args, **kwargs)

class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    model = UserProfile
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def list(self, request, *args, **kwargs):
        """
        Returns a list of Users paginated by 20 items.
        Provide page number if necessary.
        """
        return super(UserViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Return the User for a provided id
        """
        return super(UserViewSet, self).retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Create new user profile.
        """
        return super(UserViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Update user object.
        Only the user himself can update his userprofile 
        """
        return super(UserViewSet, self).update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Update part of user profile.
        Only the user can patch his profile.
        """
        return super(UserViewSet, self).partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Delete User Profile.
        Provide id of the user.
        """
        return super(UserViewSet, self).destroy(request, *args, **kwargs)

class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        news_id = self.kwargs['pk']
        return Comments.objects.filter(news=news_id)

    def perform_create(self, serializer):
        # save the owner of the news
        serializer.save(owner=self.request.user)

def testOauth(request):
    context = {}
    return render(request, 'siteModel/testOauth.html', context)