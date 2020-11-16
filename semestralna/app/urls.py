from django.urls import path
from . import views

app_name = 'app'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login', views.LoginView.as_view(), name='login'),
    path('user_login', views.user_login, name='user_login'),
    path('user_logout', views.user_logout, name='user_logout'),
    path('test', views.TestView.as_view(), name='test'),
    path('remove_discussion/<int:pk>',
         views.remove_discussion, name='remove_discussion'),
    path('add_discussion', views.add_discussion, name='add_discussion')
]
