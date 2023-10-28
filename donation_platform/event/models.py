from django.db import models
from donation_platform.models import ArticlesType, ArticlesStates, Users, ArticlesZones, Organization
from django.utils import timezone

class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=50)
    event_description = models.TextField()
    type = models.ForeignKey(ArticlesType, models.DO_NOTHING, related_name="event_type")
    state = models.ForeignKey(ArticlesStates, models.DO_NOTHING, related_name="event_state")
    event_date = models.DateTimeField()
    user = models.ForeignKey(Users, models.DO_NOTHING, related_name="event_user")
    zone = models.ForeignKey(ArticlesZones, models.DO_NOTHING, related_name="event_zone")
    geom_point = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    organization = models.ForeignKey(Organization, models.DO_NOTHING, blank=True, null=True, related_name="event_organization")

    class Meta:
        managed = False
        db_table = 'event'

