from django.db import models
from donation_platform.models import Organization
from django.utils import timezone

class Users(models.Model):
    user_name = models.CharField(max_length=50)
    user_email = models.CharField(max_length=50)
    user_password = models.TextField()
    organization = models.ForeignKey(Organization, models.DO_NOTHING, blank=True, null=True, related_name='users_organization')
    user_state = models.IntegerField()
    erased_at = models.DateTimeField(blank=True, null=True)
    erased_reason = models.TextField(blank=True, null=True)
    last_login = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'users'

