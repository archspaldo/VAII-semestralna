from django.urls import path
from . import views

app_name = 'app'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login', views.LoginView.as_view(), name='login'),
    path('edit/<int:pk>', views.EditView.as_view(), name='edit'),
    path('add', views.AddView.as_view(), name='add'),
    path('user_logout', views.user_logout, name='user_logout'),
    path('test', views.TestView.as_view(), name='test'),
    path('remove_discussion/<int:pk>',
         views.remove_discussion, name='remove_discussion'),
    path('discussion/<int:pk>', views.DiscussionView.as_view(), name='discussion'),
    path('reply', views.reply, name='reply'),
    path('comments/<int:topic>/<int:comment>', views.get_comments, name='comments'),
    path('comments/<int:topic>/', views.get_comments_all, name='comments'),
]