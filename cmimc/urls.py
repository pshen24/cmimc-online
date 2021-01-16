from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from website import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include

urlpatterns = [
    path('', views.home, name='home'),
    path('contests', views.contest_list, name='contest_list'),
    path('math/format', views.math_info, name='math_info'),
    path('math/sample-problems', views.math_sample_problems, name='math_sample_problems'),
    path('programming/format', views.prog_info, name='prog_info'),
    path('programming/sample-problems', views.prog_sample_problems, name='prog_sample_problems'),
    path('schedule', views.schedule, name='schedule'),
    path('registration', views.reg_info, name='reg_info'),
    path('faq', views.faq, name='faq'),
    path('resources', views.resources, name='resources'),
    path('mini-events', views.general_info.mini_events, name='mini_events'),

    path('admin', admin.site.urls),
    
    path('signup', views.signup, name='signup'),
    path('login', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('change-password', auth_views.PasswordChangeView.as_view(template_name='change_password.html', success_url='done'), name='change_password'),
    path('change-password/done', auth_views.PasswordChangeDoneView.as_view(template_name='change_password_done.html'), name='change_password_done'),
#    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='reset_password.html'), name='reset_password'),

    path('contest/<int:contest_id>/newteam', views.new_team, name='new_team'),
    path('team/<int:team_id>', views.team_info, name='team_info'),
    path('team/<int:team_id>/join/<str:invite_code>', views.join_team, name='join_team'),
    path('contest/<int:contest_id>/myteams', views.coach_teams, name='coach_teams'),
    
    path('exam/<int:exam_id>', views.all_problems, name='all_problems'),
    path('exam/<int:exam_id>/leaderboard', views.leaderboard, name='leaderboard'),
    path('exam/<int:exam_id>/problem/<int:problem_number>', views.view_problem, name='view_problem'),
    path('exam/<int:exam_id>/problem/<int:problem_number>/submit', views.submit, name='submit'),
    path('exam/<int:exam_id>/problem/<int:problem_number>/submit/task/<int:task_number>', views.submit, name='submit'),
    
    path('exam/<int:exam_id>/submissions', views.all_submissions, name='all_submissions'),
    path('submission/<int:submission_id>', views.view_submission, name='view_submission'),
    path('resubmit/<int:submission_id>', views.resubmit, name='resubmit'),

]
