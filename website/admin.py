from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from .forms import UserCreationForm, UserChangeForm
from .models import Contest, Exam, Problem, User, Mathlete, Team, Competitor, Submission


class UserAdmin(DefaultUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ('name', 'email', 'is_staff', 'is_active',)
    list_filter = ('name', 'email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('name', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('name',)
    ordering = ('name',)


admin.site.register(Contest)
admin.site.register(Exam)
admin.site.register(Problem)
admin.site.register(User, UserAdmin)
admin.site.register(Mathlete)
admin.site.register(Team)
admin.site.register(Competitor)
admin.site.register(Submission)

