from django.http import HttpResponseRedirect, HttpResponse, Http404
from .handleupload import handle_uploaded_file
from django.template.loader import get_template
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json

from .models import Post, Comment, Reply
from .forms import PostForm, CommentForm, ReplyForm

def index(request):
    # posts
    latest_post_list = Post.objects.order_by('-pub_date') #[:10]

    # comments implementation with lists
    post_comments = {}
    for post in latest_post_list:
        comment_replies = {}
        for comment in post.comments.all().order_by('-pub_date')[:2]:
            comment_replies[comment] = comment.replies.all().order_by('-pub_date')[:2]
        post_comments[post] = comment_replies
    
    print(post_comments)
    # convert to tuple so we can paginate
    post_comments = tuple(post_comments.items())
    # pagination
    paginator = Paginator(post_comments, 3)

    page = request.GET.get('page', 1)
    try:
        content = paginator.page(page)
    except PageNotAnInteger:
        content = paginator.page(1)
    except EmptyPage:
        content = paginator.page(paginator.num_pages)
    
    context = {
        'post_comments': content, #paginator.page(1).object_list,
    }
    return render(request, 'memes/index.html', context)

# when visiting user's own profile
@login_required(login_url='/accounts/login')
def selfprofile(request):
    instance = request.user
    user_post_list = instance.posts.all().order_by('-pub_date')[:10]
    context = {
        "user_self": instance,
        "user_post_list": user_post_list,
    }
    return render(request, "memes/profile_self.html", context)

# when visiting other user profiles
def profile(request, id=None):
    instance = get_object_or_404(User, id=id)
    user_post_list = instance.posts.all().order_by('-pub_date')[:10]
    context = {
        "user_scoped": instance,
        "user_post_list": user_post_list,
    }
    return render(request, "memes/profile.html", context)

@login_required(login_url='/accounts/login')
def upload(request):
        
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.creator = request.user
        instance.save()
        # message success
        messages.success(request, "Successfully uploaded")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
    }
    return render(request, "memes/upload.html", context)

def post_detail(request, id=None):
    # get post
    post = get_object_or_404(Post, id=id)

    # get comments and replies
    comment_replies = {}
    for comment in post.comments.all().order_by('-pub_date')[:40]:
        comment_replies[comment] = comment.replies.all().order_by('-pub_date')[:2]

    context = {
        "post": post,
        "comment_replies": comment_replies,
    }
    return render(request, "memes/detail.html", context)

@login_required(login_url='/accounts/login')
def post_delete(request, id=None):
    # get post
    post = get_object_or_404(Post, id=id)

    # check if it's actually the creator that wants to delete post
    instance = request.user
    if post.creator.id == instance.id:
        post.delete()
        return HttpResponseRedirect("/profile_self.html")

    else:
        # error page here
        raise Http404

@login_required(login_url='/accounts/login')
def comment_create(request):
    if request.method == 'POST':
        try:
            comment_content = request.POST.get('comment_content')
            comment_parentpost = Post.objects.get(id = request.POST.get('comment_parentpost'))

            # we can add more regulation here later (for example, some kinds of user can't comment on some kinds of posts)
            response_data = {}

            comment = Comment(text=comment_content, creator=request.user, post=comment_parentpost)
            comment.save()

            response_data['result']     = 'Create comment successful!'
            response_data['commentpk']  = comment.pk
            response_data['text']       = comment.text
            response_data['pub_date']   = "Just now"
            response_data['creator']    = comment.creator
            response_data['creatorId']  = comment.creator.id
            response_data['post']       = comment.post

            return HttpResponse(
                json.dumps(response_data, default=str),
                content_type="application/json"
            )
        except Exception as e:
            print(e)
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

@login_required(login_url='/accounts/login')
def reply_create(request):
    if request.method == 'POST':
        try:
            reply_content = request.POST.get('reply_content')
            reply_parentComment = Comment.objects.get(id = request.POST.get('reply_parentcomment'))

            # if the comment actually exists, we can add more checks here later if the user is actually allowed to reply.
            response_data = {}

            reply = Reply(text=reply_content, creator=request.user, comment=reply_parentComment)
            reply.save()

            response_data['result']     = 'Create reply successful!'
            response_data['commentpk']  = reply.pk
            response_data['text']       = reply.text
            response_data['pub_date']   = "Just now"
            response_data['creator']    = reply.creator
            response_data['creatorId']  = reply.creator.id
            response_data['comment']    = reply.comment
            
            return HttpResponse(
                json.dumps(response_data, default=str),
                content_type="application/json"
            )
        except Exception as e:
            print(e)
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

# about links
def about_cookies(request):
    return render(request, "about/cookies.html")

def about_privacy(request):
    return render(request, "about/privacy.html")

def about_tos(request):
    return render(request, "about/tos.html")

def about_rules(request):
    return render(request, "about/rules.html")