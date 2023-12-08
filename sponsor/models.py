from django.db import models
from donation_platform.models import ArticlesType, ArticlesStates, Users, ArticlesZones, Organization
from django.utils import timezone

class Sponsor(models.Model):
    sponsor_id = models.AutoField(primary_key=True)
    sponsor_name = models.CharField(max_length=50)
    sponsor_description = models.TextField()
    type = models.ForeignKey(ArticlesType, models.DO_NOTHING, related_name='sponsor_type')
    state = models.ForeignKey(ArticlesStates, models.DO_NOTHING, related_name='sponsor_state')
    sponsor_attachment = models.TextField(blank=True, null=True)
    sponsor_created_at = models.DateTimeField()
    user = models.ForeignKey(Users, models.DO_NOTHING, related_name='sponsor_user')
    zone = models.ForeignKey(ArticlesZones, models.DO_NOTHING, related_name='sponsor_zone')
    geom_point = models.TextField(blank=True, null=True)
    has_requests = models.BooleanField()
    request_count = models.IntegerField()
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    organization = models.ForeignKey(Organization, models.DO_NOTHING, null=True, related_name='sponsor_organization')

    class Meta:
        managed = False
        db_table = 'sponsor'

