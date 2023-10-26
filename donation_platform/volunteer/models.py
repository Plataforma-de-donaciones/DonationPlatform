from django.db import models
from donation_platform.models import ArticlesType, ArticlesStates, Users, ArticlesZones
from django.utils import timezone

class Volunteer(models.Model):
    vol_id = models.AutoField(primary_key=True)
    vol_name = models.CharField(max_length=50)
    vol_description = models.TextField()
    type = models.ForeignKey(ArticlesType, models.DO_NOTHING, related_name='volunteer_type')
    state = models.ForeignKey(ArticlesStates, models.DO_NOTHING, related_name='volunteer_state')
    vol_tasks = models.TextField(blank=True, null=True)
    vol_created_at = models.DateTimeField()
    user = models.ForeignKey(Users, models.DO_NOTHING, related_name='volunteer_user')
    zone = models.ForeignKey(ArticlesZones, models.DO_NOTHING, related_name='volunteer_zone')
    geom_point = models.TextField(blank=True, null=True)
    has_requests = models.BooleanField()
    request_count = models.IntegerField()
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    vol_rating = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'volunteer'

