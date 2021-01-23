from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from website.forms import UserCreationForm, UserChangeForm
from website.models import Contest, Exam, Problem, User, Mathlete, Team, Competitor, Submission, Score, Task, TaskScore


class UserAdmin(DefaultUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ('email', 'name', 'role', 'is_staff', 'is_tester')
    list_filter = ('role', 'is_staff', 'is_tester')
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'email', 'full_name', 'alias', 'password', 'role')}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_tester', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'full_name', 'alias', 'password1', 'password2', 'role', 'is_superuser', 'is_staff', 'is_tester', 'is_active')}
        ),
    )
    search_fields = ('email', 'first_name', 'last_name', 'full_name')
    ordering = ('pk',)


class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'mathlete_list', 'coach', 'contest', 'is_finalized',)
    list_filter = ('contest', 'is_finalized',)
    search_fields = ('team_name',)

admin.site.register(Contest)
admin.site.register(Exam)
admin.site.register(Problem)
admin.site.register(User, UserAdmin)
admin.site.register(Mathlete)
admin.site.register(Team, TeamAdmin)
admin.site.register(Competitor)
admin.site.register(Submission)
admin.site.register(Score)
admin.site.register(Task)
admin.site.register(TaskScore)


