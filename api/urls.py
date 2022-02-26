from django.urls import path
from . import views

urlpatterns = [
    path('',views.get_blogs,name='view_all'),
    path('<int:id>',views.make_changes,name='change'),
]