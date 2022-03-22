from django.shortcuts import render,redirect
import json
import os
from .models import Post
from .forms import PostForm,NewUser
import requests
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def homepage(request):
    return render(request,'news_blog/home.html',{})

@login_required(login_url='/login/')
def news_page(request,optional=''):
    API_KEY = os.getenv('API_KEY')
    link = f'https://newsapi.org/v2/top-headlines?country=in&apiKey={API_KEY}'
    if request.method == 'POST':
        post = request.POST
        if post['q']:
            link = f'https://newsapi.org/v2/{post["sort"]}?q={post["q"]}&apiKey={API_KEY}'
        else:
            if post['category'] != 'all':
                link = f'https://newsapi.org/v2/top-headlines?country=in&category={post["category"]}&apiKey={API_KEY}'

    category = ['business','entertainment','general','health','science','sport','technology']
    response = requests.get(link)
    print(link)
    if response:
        articles = response.json()['articles']
        return render(request,'news_blog/news.html',{'articles':articles,'category':category})
    else:
        return render(request, 'news_blog/news.html', {'category': category})

@login_required(login_url='/login/')
def article(request,title):
    value = None
    for article in request.session['articles']:
        if article['title'] == title:
            value = article
    return render(request,'news_blog/article.html',{'article':value})

def register(request):
    form = NewUser()

    if request.method == 'POST':
        form = NewUser(request.POST)
        if form.is_valid():
            user = form.save()
            request.session['username'] = form.cleaned_data.get('username')
            login(request,user)
            messages.success(request,'Registration complete')
            return redirect('/')
        messages.error(request,'Unsuccessful registration')
    return render (request,'news_blog/registration.html',{'form':form})

@login_required(login_url='/login/')
def all_blogs(request):

    if request.method == 'POST':
        posts = request.user.post_set.all()
        for post in posts:
            if request.POST.get('c' + str(post.id)) == 'remove':
                post.delete()

                messages.info(request, 'Post has been permanently removed')
    posts = request.user.post_set.all()
    return render(request,'news_blog/blog.html',{'posts':posts})

@login_required(login_url='/login/',redirect_field_name='next')
def create_new(request):

    if request.method == 'POST':

        if not request.POST.get('title') or not request.POST.get('content'):
            messages.error(request, 'All fields are necessary')
        else:
            p = Post(title=request.POST.get('title'),content=request.POST.get('content'),user=request.user)
            p.save()
            messages.success(request, 'Post created succesfully')
            return redirect('/blog/')

    return render(request,'news_blog/create.html',{})


def login_request(request):
    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(request,request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)

            if user:
                login(request,user)
                messages.info(request,'Logged in successfully')
                request.session['username'] = form.cleaned_data.get('username')
                return redirect('/')
            else:
                messages.error(request,'Username or password is invalid')
        else:
            messages.error(request, 'Username or password is invalid')
    return render(request,'news_blog/login.html',{'form':form})

@login_required(login_url='/login/')
def get_post(request,id):
    post = request.user.post_set.get(id=id)
    if post:
        return render(request, 'news_blog/post.html', {'post': post})
    else:
        messages.error(request,"No such post exists")
        redirect('/blog')

@login_required(login_url='/login/')
def logout_request(request):
    logout(request)
    messages.info(request,"You have successfully logged out")
    return redirect('/')
