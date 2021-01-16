from django.db import models
from django.conf import settings

class Mathlete(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='mathlete', \
            unique=True, on_delete=models.CASCADE)

    def __str__(self):
        return "Mathlete: {0} ({1})".format(self.user.name, self.user.email)

    def get_team(self, contest):
        return self.teams.filter(contest=contest).first()


