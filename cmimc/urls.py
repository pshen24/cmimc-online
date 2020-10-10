from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from website import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contests', views.contest_list, name='contest_list'),
    path('admin/', admin.site.urls),
    
    path('signup', views.signup, name='signup'),
    path('login', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('change-password', auth_views.PasswordChangeView.as_view(template_name='change_password.html', success_url='done'), name='change_password'),
    path('change-password/done', auth_views.PasswordChangeDoneView.as_view(template_name='change_password_done.html'), name='change_password_done'),
#    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='reset_password.html'), name='reset_password'),

    path('exam/<int:exam_id>/problem/<str:problem_number>', views.problem_info, name='problem_info'),
    path('exam/<int:exam_id>/problem/<str:problem_number>/submit', views.submit, name='submit'),
    path('exam/<int:exam_id>', views.exam_status, name='exam_status'),
]


