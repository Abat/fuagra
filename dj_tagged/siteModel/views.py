from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets
from siteModel.models import News
from siteModel.models import NewsCategory
from siteModel.models import UserProfile
from siteModel.models import Comments
from siteModel.models import User # Simple email confirm
from siteModel.models import Vote
from siteModel.ranking.ranking import *
from siteModel.ranking.rank_helper import *
from siteModel.serializers import NewsSerializer, UserSerializer, CommentSerializer, VoteSerializer
from siteModel.forms import UserForm, UserProfileForm
from siteModel.permissions import IsOwnerOrReadOnly
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import get_user
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings
import logging



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

    if not request.user.is_anonymous():
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            the_username = user.username
            the_password = user.password
            new_email = user_form.cleaned_data.get('email_address')
            confirmation_key = user.add_unconfirmed_email(new_email)
            
            send_mail('Confirm', _create_email_confirmation_message(the_username, confirmation_key), settings.EMAIL_HOST_USER,
            [new_email], fail_silently=False, html_message=_create_html_email_confirmation_message(user.username, confirmation_key))

            user.set_password(the_password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'avatar' in request.FILES:
                profile.avatar = request.FILES['avatar']

            profile.save()
            registered = True
            #Login user after registering
            user_acc = authenticate(username=the_username, password=the_password)
            login(request, user_acc)

        else:
            print(user_form.errors, profile_form.errors)
            return HttpResponse("Error: {0}, {1}".format(user_form.errors, profile_form.errors))
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'siteModel/register.html', {'user_form':user_form,
     'profile_form':profile_form,
      'registered':registered})

def _create_email_confirmation_message(user_name, confirmation_key):
    return 'Hello {0},\n\nThanks for registering at Fuagrakz. Please visit http://www.fuagra.kz/accounts/confirmation?key={1} to confirm the creation of your account.\n\nIf you are not the owner of this account, please ignore this message.\n\nThanks,\nFuagrakz Team'.format(user_name, confirmation_key)

#Probably want https later.
def _create_html_email_confirmation_message(user_name, confirmation_key):
    return 'Hello <strong>{0}</strong>,<br><br>Thanks for registering at Fuagrakz. Please visit this <a href="http://www.fuagra.kz/accounts/confirmation?key={1}">link</a> to confirm the creation of your account.<br><br>If you are not the owner of this account, please ignore this message.<br><br>Thanks,<br>Fuagrakz Team'.format(user_name, confirmation_key)

def user_login(request):

    if not request.user.is_anonymous():
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        redirect = request.POST.get('next')

        #Check empty
        if not redirect:
            redirect = '/'
            
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                logger = logging.getLogger("django")
                logger.info("views.user_login: Redirecting to" + redirect)
                login(request, user)
                return HttpResponseRedirect(redirect)
            else:
                return HttpResponse("Your Account is disabled.")
        else:
            print("Invalid login details :{0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        #This is the key used by django to redirect (notice next= ... in redirects!)
        context = {}
        if request.GET.get('next') is not None:
            context['next'] = request.GET.get('next')
        return render(request, 'siteModel/login.html', context)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def confirm_email(request):
    # Get an instance of a logger
    logger = logging.getLogger("django")
    logger.info("HELLO WORLD")
    confirmation_key = request.GET.get('key', 'ERROR')
    try:
        logger.info(confirmation_key)
        new_email = request.user.confirm_email(confirmation_key)
        logger.info("success")
        request.user.set_primary_email(new_email)
        request.user.email = new_email
        return HttpResponse("good")
    except:
        logger.info("fail didnt match!")
        return HttpResponse("bad")

@login_required
def resend_confirmation_email(request):
    emails = request.user.get_unconfirmed_emails
    email = emails[0]
    confirmation_key = request.user.reset_confirmation(email)
    send_mail('Confirm', 'Use http://www.fuagra.kz/accounts/confirmation?key=%s to confirm your new email' % confirmation_key, settings.EMAIL_HOST_USER,
            [email], fail_silently=False)
    return HttpResponse("uhh ok")

class NewsViewSet(viewsets.ModelViewSet):

    serializer_class = NewsSerializer
    queryset = News.objects.all()
    model = News
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)
    def list(self, request, *args, **kwargs):
        """
        Return a list of News paginated by 20 items.
        Provide page number if necessary.
        """

   
        news_category = request.GET.get('category', None)
        news_list = None

        #Getting news list/filtering
        if news_category is not None:
            #Check if news category specified exists.
            news_category_objects = NewsCategory.objects.filter(title=news_category)
            if news_category_objects.count() > 0:
                news_list = News.objects.filter(category=news_category)
            else:
                #TODO THROW EXCEPTION CATEGORY DOES NOT EXIST
                pass
        else: #If no filtering, pass in all news
            news_list = News.objects.all()
                
        #sort style
        sort_style = None
        if request.GET.get('sort') is not None:
            sort_style = request.GET.get('sort')

        rankAlgo = RankHelper.parse_rank_style(sort_style)

        self.queryset = rankAlgo.sort_list_of_news(news_list)

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
        user = get_user(self.request)
        serializer.save(owner=user, username=user.username)

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
    queryset = User.objects.all()
    serializer_class = UserSerializer
    model = User
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

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
        comments = Comments.objects.filter(news=news_id)
        
        #sort style
        sort_style = self.request.QUERY_PARAMS.get('sort', None)

        rankAlgo = RankHelper.parse_rank_style(sort_style)

        query_set = rankAlgo.sort_list_of_news(comments)

        return query_set

    def perform_create(self, serializer):
        # save the owner of the news
        user = self.request.user
        serializer.save(owner=user, username=user.username)


# class ApiEndpoint(ProtectedResourceView):
#     def get(self, request, *args, **kwargs):
#         return HttpResponse('Hello, OAuth2!')

@login_required
def secret_page(request, *args, **kwargs):
    return HttpResponse('Secret contents!', status=200)


class VoteViewSet(viewsets.ModelViewSet):
    model = Vote
    serializer_class = VoteSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        news_id = self.kwargs['news_id']
        return Vote.objects.filter(news=news_id)

    def list(self, request, *args, **kwargs):
        """
        Return a list of News paginated by 20 items.
        Provide page number if necessary.
        """
        return super(VoteViewSet, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Create news object.
        """
        return super(VoteViewSet, self).create(request, *args, **kwargs)

    def upvote(self, request, news_id):
        user = self.request.user
        serializer = VoteSerializer(data=request.data)
        news = get_object_or_404(News, pk=news_id)
        if serializer.is_valid():
            try:
                vote = Vote.objects.get(news=news_id, user=user)
                if vote.vote_status == Vote.CLEAR_STATUS:
                    vote.vote_status = Vote.UPVOTE_STATUS
                    news.upvotes += 1
                    vote.save()
                    news.save()
                    return Response({'upvote':'1'})
                if vote.vote_status == Vote.DOWNVOTE_STATUS:
                    vote.vote_status = Vote.UPVOTE_STATUS
                    news.upvotes += 1
                    news.downvotes -= 1
                    vote.save()
                    news.save()
                    return Response({'upvote':'1', 'downvote':'-1'})
                else:
                    vote.vote_status = Vote.CLEAR_STATUS
                    news.upvotes -= 1
                    vote.save()
                    news.save()
                    return Response({'upvote':'-1'})
            except Vote.DoesNotExist:
                serializer.save(user=user, vote_status=Vote.UPVOTE_STATUS)
                news.upvotes += 1
                news.save()
                return Response({'upvote':'1'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def downvote(self, request, news_id):
        user = self.request.user
        serializer = VoteSerializer(data=request.data)
        news = get_object_or_404(News, pk=news_id)
        if serializer.is_valid():
            try:
                vote = Vote.objects.get(news=news_id, user=user)
                if vote.vote_status == Vote.CLEAR_STATUS:
                    vote.vote_status = Vote.DOWNVOTE_STATUS
                    news.downvotes += 1
                    vote.save()
                    news.save()
                    return Response({'downvote':'1'})
                if vote.vote_status == Vote.DOWNVOTE_STATUS:
                    vote.vote_status = Vote.CLEAR_STATUS
                    news.downvotes -= 1
                    vote.save()
                    news.save()
                    return Response({'downvote':'-1'})
                else:
                    vote.vote_status = Vote.DOWNVOTE_STATUS
                    news.upvotes -= 1
                    news.downvotes += 1
                    vote.save()
                    news.save()
                    return Response({'downvote':'1', 'upvote':'-1'})
            except Vote.DoesNotExist:
                serializer.save(user=user, vote_status=Vote.DOWNVOTE_STATUS)
                news.downvotes += 1
                news.save()
                return Response({'downvote':'1'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        

    def retrieve(self, request, *args, **kwargs):
        """
        Return the User for a provided id
        """
        return super(VoteViewSet, self).retrieve(request, *args, **kwargs)


