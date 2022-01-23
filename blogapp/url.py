from django.contrib.auth.views import LogoutView
from django.urls import path, include

from django.conf import settings
from django.contrib.auth import views as auth_view
from django.conf.urls.static import static
from django.views.generic import TemplateView

from blogapp import views

urlpatterns = [
                  path('loginView/', views.loginView, name='login_view'),
                  path('logoutView/', views.logoutPage, name='logout_view'),
                  path('registration/', views.registration, name='registration'),
                  path('profilePage/', views.profilePage, name='profile_page'),
                  path('', views.Home, name='home_page'),
                  path('showblog/<int:id>', views.showblog, name='show_blog'),
                  path('adminPage/', views.admin_page, name='admin_page'),
                  path('notapproved/', views.not_approved, name='not_approved'),
                  path('blogView/', views.blogview, name='blog_view'),
                  path('myblogView/', views.MyBLog, name='myblog_view'),
                  path('update/', views.updateView, name='update_view'),
                  path('forget/', views.forgetpassword, name='forget_password'),
                  path('reset/<uidb64>/<token>/',
                       auth_view.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
                       name='password_reset_confirm'),

                  path('reset_password_complete/',
                       auth_view.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
                       name='password_reset_complete'),



              ] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)

# urlpatterns += static(settings.MEDIA_URL,
#                               document_root=settings.MEDIA_ROOT)
