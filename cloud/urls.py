from django.urls import path
from . import views

urlpatterns = [
    path('ec2/', views.list_ec2_instances, name='list_ec2'),
    path('ec2/action/', views.ec2_action, name='ec2_action'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]