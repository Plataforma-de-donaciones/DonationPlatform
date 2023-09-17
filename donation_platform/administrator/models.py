from django.db import models
from donation_platform.models import Organization, Users
from django.utils import timezone

# Create your models here.
class Administrator(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name='administrator_user')
    start_date = models.DateTimeField()
    organization = models.ForeignKey(Organization, models.DO_NOTHING, blank=True, null=True, related_name='administrator_organization')
    administrator_state = models.IntegerField()
    erased_at = models.DateTimeField(blank=True, null=True)
    erase_reason = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'administrator'

