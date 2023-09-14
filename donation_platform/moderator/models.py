from django.db import models
from donation_platform.models import Organization, Users
from django.utils import timezone


class Moderator(models.Model):
    user = models.ForeignKey(Users, models.DO_NOTHING, related_name='moderator_user')
    start_date = models.DateTimeField()
    organization = models.ForeignKey(Organization, models.DO_NOTHING, blank=True, null=True, related_name='moderator_organization')
    moderator_state = models.IntegerField()
    erased_at = models.DateTimeField(blank=True, null=True)
    erased_reason = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'moderator'
