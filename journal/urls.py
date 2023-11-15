
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    # Home url 
    path('', views.home, name='home'),

    # Register url
    path('register/', views.register, name='register'),

    # Login url
    path('user-login/', views.user_login, name='user-login'),

    # Logout url
    path('user-logout/', views.user_logout, name='user-logout'),

    # Dashboard url
    path('dashboard/', views.dashboard, name='dashboard'),

    # Post thought url
    path('post-thought/', views.post_thought, name='post-thought'),

    # My thoughts url
    path('my-thoughts/', views.my_thoughts, name='my-thoughts'),

    # Update thoughts url
    path('update-thought/<str:pk>/', views.update_thought, name='update-thought'),

    # Delete thoughts url
    path('delete-thought/<str:pk>/', views.delete_thought, name='delete-thought'),

    # Delete thoughts url
    path('profile-management/', views.profile_management, name='profile-management'),

    # Delete account url
    path('delete-account/', views.delete_account, name='delete-account'),

    # Password management
    # Reset password url which gives users the ability to enter their email to receive a password reset link
    path('reset_password', auth_views.PasswordResetView.as_view(template_name='password_reset/password-reset.html'), name='reset_password'),

    # Notify's users that a reset password link was sent to their email
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(template_name='password_reset/password-reset-sent.html'), name='password_reset_done'),

    # Sends a reset password link to users email
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset/password-reset-form.html'), name='password_reset_confirm'),

    # Nofify's users that their password has been changed
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password-reset-complete.html'), name='password_reset_complete'),


]