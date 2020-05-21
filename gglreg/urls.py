from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.login, name='login'),

    path('signup', views.signup, name='signup'),

    path('home', views.home, name='home'),

    path('logout', views.logout, name='logout'),

    path('activate/<uidb64>/<token>/',
         views.activate_account, name='activate'),

    path('account', views.account, name='account'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='reset_pass.html'), name='reset_password'),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='reset_pass_msg.html'), name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='reset_pass_confirm.html'), name='password_reset_confirm'),

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='reset_pass_complete.html'), name='password_reset_complete'),

    path('change_password/', auth_views.PasswordChangeView.as_view(template_name='change_password.html'), name='change_password'),

    path('change_password_done/', auth_views.PasswordChangeDoneView.as_view(template_name='change_password_done.html'), name='password_change_done'),
]

