from django.contrib import admin
from django.urls import path
from website import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contests', views.contest_list, name='contest_list'),
    path('admin/', admin.site.urls),
]


