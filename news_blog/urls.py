from django.urls import path
from . import views

urlpatterns = [

    path('',views.homepage,name='home'),
    path('news/',views.news_page,name='news'),
    path('news/<str:title>',views.article,name='article'),
    path('create/',views.create_new,name='create'),
    path('blog/',views.all_blogs,name='blog'),
    path('blog/<int:id>',views.get_post,name='getpost'),
    path('register/',views.register,name='registration'),
    path('logout/',views.logout_request,name='logout_request'),
    path('login/',views.login_request,name='login_request'),
    ]