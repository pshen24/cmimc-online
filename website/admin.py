from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from website.forms import UserCreationForm, UserChangeForm
from website.models import Contest, Exam, Problem, User, Mathlete, Team, Competitor, Submission, Score


class UserAdmin(DefaultUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ('full_name', 'email', 'is_staff', 'is_active',)
    list_filter = ('full_name', 'email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('full_name', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('full_name', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('full_name',)
    ordering = ('full_name',)


admin.site.register(Contest)
admin.site.register(Exam)
admin.site.register(Problem)
admin.site.register(User, UserAdmin)
admin.site.register(Mathlete)
admin.site.register(Team)
admin.site.register(Competitor)
admin.site.register(Submission)
admin.site.register(Score)
