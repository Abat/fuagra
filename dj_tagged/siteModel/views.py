from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets
from siteModel.models import News
from siteModel.models import NewsCategory
from siteModel.models import NewsCategoryUserPermission
from siteModel.models import UserProfile
from siteModel.models import Comments
from siteModel.models import User # Simple email confirm
from siteModel.models import Vote
from siteModel.models import PasswordResetRequest
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
from django.http import JsonResponse
from django.http import Http404
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings
from notifications.signals import notify
import logging
from django.views.decorators.csrf import csrf_exempt
import uuid
import json


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

def faq(request):
    context = {}
    return render(request, 'siteModel/faq.html', context)

def comments(request, pk):
    context = {}
    context['news_pk'] = pk
    return render(request, 'siteModel/comments.html', context)

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
            if new_email:
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
            errors = user_form.errors.copy()
            errors.update(profile_form.errors)
            return render(request, 'siteModel/errors.html', {"errors": errors})
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

def create_password_reset_message(uuid):
    return """
    Hello,<br><br> 
    It seems that you have requested a password change for your account at Fuagrakz. 
    Please visit here <a href="http://www.fuagra.kz/accounts/reset_password/?request_id={0}">http://www.fuagra.kz/accounts/reset_password/?request_id={0}</a> to change your password.<br><br>
    If you did not make this request, please ignore this message.<br><br>Thanks,<br>Fuagrakz Team""".format(uuid)

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
                errors = {"error" : "Your Account is disabled." }
                return render(request, 'siteModel/errors.html', {"errors": errors})
        else:
            errors = {"error" : "Invalid login details" }
            return render(request, 'siteModel/errors.html', {"errors": errors})
    else:
        #This is the key used by django to redirect (notice next= ... in redirects!)
        context = {}
        if request.GET.get('next') is not None:
            context['next'] = request.GET.get('next')
        return render(request, 'siteModel/login.html', context)

def request_password_reset(request):
    if not request.user.is_anonymous():
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        email = request.POST.get('email')
        if not email:
            return createAPIErrorJsonReponse('??.', 404)
        logger = logging.getLogger("django")
        logger.info("reset email is " + email)
        try:
            user = User.objects.get(email = email)
            try:
                pass_request = PasswordResetRequest.objects.get(email = email) 
                if not pass_request.is_expired():
                    return createAPIErrorJsonReponse('Please wait before trying again.', 404) #TODO WHAT TO DO IF GUY TRYING TO SPAM ONE EMAIL ADDRESS?
                else:
                    #Delete it and create new request.
                    pass_request.delete()
            except PasswordResetRequest.DoesNotExist:
                pass
        except User.DoesNotExist:
            return createAPIErrorJsonReponse('No user with that email exists (Perhaps you haven\'t confirmed your email?).', 401)

        #creating request
        request_id = str(uuid.uuid4())
        valid_until_date = timezone.now() + PasswordResetRequest.expire_time_delta()
        request_pass = PasswordResetRequest.objects.create (email = email, request_id = request_id, date_valid = valid_until_date)
        request_pass.save();
        html_message = create_password_reset_message(request_id)
        send_mail('Confirm', html_message, settings.EMAIL_HOST_USER,
                [email], fail_silently=False, html_message=html_message)
        return createAPISuccessJsonReponse({'result': 'ok'})
    else:
        context = {}
        if request.GET.get('request_id') is not None:
            context['request_id'] = request.GET.get('request_id')
        return render(request, 'siteModel/resetPasswordRequest.html', context)  

def submit_password_change(request):
    if not request.user.is_anonymous():
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        new_pass = request.POST.get('password')
        new_pass_confirm = request.POST.get('confirm_password')
        logger = logging.getLogger("django")
        logger.info("pass restglegnS" + str(new_pass))
        logger.info("SET USER PERMIS" + str(new_pass_confirm))
        if new_pass != new_pass_confirm:
            return createAPIErrorJsonReponse('Passwords don\'t match...', 200) #TODO WHAT TO DO IF GUY TRYING TO SPAM ONE EMAIL ADDRESS?
        if not is_valid_password(new_pass):
            return createAPIErrorJsonReponse('Password is not valid.', 200) #TODO WHAT TO DO IF GUY TRYING TO SPAM ONE EMAIL ADDRESS?
        
        request_id = request.POST.get('request_id', None)
        if not request_id:
            return createAPIErrorJsonReponse('No request id.', 404)
        try:
            pass_request = PasswordResetRequest.objects.get(request_id = request_id) 
            user = User.objects.get(email = pass_request.email)
            if not pass_request.is_expired():
                user.set_password(new_pass)
                user.save()
                pass_request.delete()
                return createAPISuccessJsonReponse({'result': 'ok'})
            else:
                pass_request.delete()
                return createAPIErrorJsonReponse('This url is expired, please request a password change again.', 404) #TODO WHAT TO DO IF GUY TRYING TO SPAM ONE EMAIL ADDRESS?
        except PasswordResetRequest.DoesNotExist:
            pass
    else:
        #This is the key used by django to redirect (notice next= ... in redirects!)
        context = {}
        if request.GET.get('request_id') is not None:
            context['request_id'] = request.GET.get('request_id')
        return render(request, 'siteModel/passwordReset.html', context)

    return createAPIErrorJsonReponse('Forbidden.', 404) #TODO WHAT TO DO IF GUY TRYING TO SPAM ONE EMAIL ADDRESS?

#TODO merge with the one is forms.py
def is_valid_password(password):
    if (not password or len(password) < 8):
        return False
    return True

@login_required
def set_user_permission(request):
    logger = logging.getLogger("django")
    #TODO
    post_data = json.loads(request.body.decode("utf-8"))
    if request.method == 'POST':
        category = post_data['category']
        username = post_data['username']
        try:
            target_user = User.objects.get(username = username)
        except User.DoesNotExist:
            return createAPIErrorJsonReponse('User does not exist.', 404)
        role = post_data['role']

        success = validate_user_options(request.user, target_user, category, role)

        if success:
            news_category = NewsCategory.objects.get(title = category)
            obj, created = NewsCategoryUserPermission.objects.get_or_create(user = target_user, category = news_category)
            obj.permission = map_role_to_code(role)
            obj.save()
            return createAPISuccessJsonReponse({'result': 'ok'})
        else:
            return createAPIErrorJsonReponse('Missing Parameters or unauthorized.', 401)
            
    else:
        return createAPIErrorJsonReponse('Forbidden', 404)

def can_user_post(user, category):
    logger = logging.getLogger("django")
    logger.info("SET USER PERMIS" + str(category))
    if not category_exists(category):
        logger.info("NO EXIST CATEGORY")
        return False
    try:
        user_permission = NewsCategoryUserPermission.objects.get(user = user, category = category)
        permission = user_permission.permission
        #Banned and cannot post
        logger.info("permission" + permission)
        if permission == 'BN':
            logger.info("cant post then")
            return False
    except NewsCategoryUserPermission.DoesNotExist:
        logger.info("NO EXIST")
        #They are a user. and can post.
        pass
    return True

def can_user_delete(user, category):
    if not category_exists(category):
        return False
    try:
        permission = NewsCategoryUserPermission.objects.get(user = user, category = category).permission
        #Only admin and mods can delete
        if permission == 'MD' or permission == 'AD':
            return True
    except NewsCategoryUserPermission.DoesNotExist:
        #They are a user
        pass
    return False

def validate_user_options(requester_user, target_user, category, role):
    logger = logging.getLogger("django")
    logger.info("SET USER PERMIS")
    if (requester_user.is_anonymous()):
        logger.info("IS ANONY")
        return False
    if target_user is None:
        logger.info("NO TARGET USER")
        return False
    if category is None:
        logger.info("CATEGORY NONE")
        return False
    if not category_exists(category):
        logger.info("CATAGENORY NO EXIST")
        return False
    if role is None:
        logger.info("NO TARGET ROLE")
        return False

    req_permission = None
    try:
        req_permission = NewsCategoryUserPermission.objects.get(user = requester_user, category = category).permission
    except NewsCategoryUserPermission.DoesNotExist:
        logger.info ("WTF REQUESTER INFO NO EXIST")
        req_permission = None

    cur_permission = None
    try:
        cur_permission = NewsCategoryUserPermission.objects.get(user = target_user, category = category).permission
    except NewsCategoryUserPermission.DoesNotExist:
        cur_permission = None

    requester_permission = map_permission_values(req_permission)
    target_user_current_permission = map_permission_values(cur_permission)
    target_user_permission = map_permission_values(role, True)
    
    #Invalid string passed in
    if (target_user_permission == 0):
        logger.info("INVALID TARGET USER POERMISSION")
        return False

    #Can't change someone higher than you
    if (requester_permission <= target_user_current_permission):
        logger.info("INVALID RANK" + str(requester_permission) + " " + str(target_user_current_permission))
        return False

    #No point in setting the same value
    if (target_user_current_permission == target_user_permission):
        logger.info("SAME VAL")
        return False

    #moderator only set by admin.
    if target_user_permission == 4:
        return True

    #target_user_permission 1-3 can be set by mod or admin
    if requester_permission == 4 or requester_permission == 5:
        return True

def map_role_to_code(role):
    the_dict = {'AD': 'AD', 'MD': 'MD', 'EX': 'EX', 'US': 'US', 'BN': 'BN',
            'Admin': 'AD', 'Moderator': 'MD', 'Expert': 'EX', 'User': 'US', 'Banned': 'BN'};
    return the_dict.get(role, 'US')

def map_code_to_role(role):
    the_dict = {'AD': 'Admin', 'MD': 'Moderator', 'EX': 'Expert', 'US': 'User', 'BN': 'Banned'};
    return the_dict.get(role, 'User')

def map_permission_values (permission, null_check = False):
    the_dict = {'AD': 5, 'MD': 4, 'EX': 3, 'US': 2, 'BN': 1,
            'Admin': 5, 'Moderator': 4, 'Expert': 3, 'User': 2, 'Banned': 1};
    if null_check:
        return the_dict.get(permission, 0)
    else:
        return the_dict.get(permission, 2)

def category_exists(category):
    if (category is None):
        return False
    #Check if news category specified exists.
    news_category_objects = NewsCategory.objects.filter(title=category)
    return news_category_objects.count() > 0

@login_required
def check_user_permission(request, category):
    if not category_exists(category):
        return createAPIErrorJsonReponse('Category does not exist.', 404)
    else:
        try:
            user_permission = NewsCategoryUserPermission.objects.get(user = request.user, category = category)
            permission = user_permission.permission
            string_permission = map_code_to_role(permission);
            return createAPISuccessJsonReponse({ "permission" : string_permission })
        except NewsCategoryUserPermission.DoesNotExist:
            string_permission = map_code_to_role("Default");
            return createAPISuccessJsonReponse({ "permission" : string_permission })

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

def list_category(request):
    if request.method == "GET":
        categories = NewsCategory.objects.all()
        data = [{'title': item.title} for item in categories]
        return HttpResponse(json.dumps(data), content_type="application/json")
    raise Http404("Category List invalid method.")

@login_required
def notifications(request):
    context = {}

    user = request.user
    # Get all News (write better solution later)
    context['notifications'] = user.notifications.all()

    return render(request, 'siteModel/notifications.html', context)

class NewsViewSet(viewsets.ModelViewSet):

    serializer_class = NewsSerializer
    queryset = News.objects.all()
    model = News
    def list(self, request, *args, **kwargs):
        """
        Return a list of News paginated by 20 items.
        Provide page number if necessary.
        """
   
        news_category = self.request.query_params.get('category', None)
        news_list = None

        #Getting news list/filtering
        if news_category is not None:
            #Check if news category specified exists.
            if category_exists(news_category):
                news_list = News.objects.filter(category=news_category)
            else:
                news_list = News.objects.all()
        else: #If no filtering, pass in all news
            news_list = News.objects.all()
                
        #sort style
        sort_style = None
        if self.request.query_params.get('sort') is not None:
            sort_style = self.request.query_params.get('sort')

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
        user = get_user(request)
        category = request.DATA['category']
        can_post = can_user_post(user, category)
        if can_post:
            return super(NewsViewSet, self).create(request, *args, **kwargs)
        else:
            return createAPIErrorJsonReponse('Unauthorized or banned.', 401)
        

    def perform_create(self, serializer):
        # save the owner of the news
        user = get_user(self.request)
        category = self.request.DATA['category']
        news = serializer.save(owner=user, username=user.username)
        if news is not None:
            if category == "Feedback":
                permissions = NewsCategoryUserPermission.objects.filter(category=category, permission="AD")
                for permission in permissions:
                    recipient = permission.user
                    notify.send(user, verb=u'leaved a feedback', recipient=recipient, target=news, description=news.title)

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
        Only the owner of the news can delete it. ---- need to verify this.
        """
        user = get_user(self.request)
        category = News.objects.get(id=int(self.kwargs['pk'])).category.title
        can_delete = can_user_delete(user, category)
        if can_delete:
            return super(NewsViewSet, self).destroy(request, *args, **kwargs)
        else:
            return createAPIErrorJsonReponse('Unauthorized.', 401)

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

class CommentViewSet(viewsets.ModelViewSet):

    serializer_class = CommentSerializer
    queryset = Comments.objects.all()
    model = Comments
    
    def list(self, request, *args, **kwargs):
        news_id = self.kwargs['pk']
        comments = Comments.objects.filter(news=news_id)
        
        #sort style
        sort_style = self.request.query_params.get('sort', None)

        rankAlgo = RankHelper.parse_rank_style(sort_style)

        self.queryset = rankAlgo.sort_list_of_news(comments)
        return super(CommentViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        comment_id = self.kwargs['comment_pk']
        comment = get_object_or_404(Comments, pk=comment_id)
        serializer = self.get_serializer(comment)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Create comments object.
        """
        news_id = self.kwargs['pk']
        news = News.objects.get(id=int(news_id))
        category = news.category.title
        user = get_user(request)
        can_post = can_user_post(user, category)
        if can_post:
            return super(CommentViewSet, self).create(request, *args, **kwargs)
        else:
            return createAPIErrorJsonReponse('Unauthorized or banned.', 401)

    def perform_create(self, serializer):
        # save the owner of the news
        user = self.request.user

        comment = serializer.save(owner=user, username=user.username)
        if comment is not None:
            news_object = News.objects.get(id=int(comment.news_id))
            news_object.num_comments += 1
            news_object.save()
            if (comment.parent is not None) and (user != comment.parent.owner):
                notify.send(user, verb=u'replied to your comment', recipient=comment.parent.owner, action_object=comment, target=news_object)
            elif user != news_object.owner:
                notify.send(user, verb=u'commented on', recipient=news_object.owner, action_object=comment, target=news_object, description=news_object.title)

    def destroy(self, request, *args, **kwargs):
        """
        Delete comment
        """
        user = get_user(self.request)
        category = News.objects.get(id=int(self.kwargs['pk'])).category.title
        can_delete = can_user_delete(user, category)
        if can_delete:
            comment_id = self.kwargs['comment_pk']
            comment = get_object_or_404(Comments, pk = comment_id)
            comment.content = "[deleted]"
            comment.save()
            return createAPISuccessJsonReponse({'result':'success'})
        else:
            return createAPIErrorJsonReponse('Unauthorized.', 401)



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
                elif vote.vote_status == Vote.DOWNVOTE_STATUS:
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
                elif vote.vote_status == Vote.DOWNVOTE_STATUS:
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




def createAPIErrorJsonReponse(msg, code):
    return JsonResponse({'status': 'error',
                        'reason': msg}, status=code)

def createAPISuccessJsonReponse(repDict):
    repDict['status'] = 'success'
    return JsonResponse(repDict)
    
