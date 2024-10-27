from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('profile/<int:pk>', views.profile, name="profile"),
    path('login/', views.login_user, name="login"),
    path('logout', views.logout_user, name="logout"),
    path('register/', views.register_user, name="register"),
    path('update_user/', views.update_user, name="update_user"),
    path('delete_post/<int:pk>', views.delete_post, name="delete_post"),
    path('edit_post/<int:pk>', views.edit_post, name="edit_post"),
    path('post/<int:post_id>/', views.post_detail, name='post_detail')
]
