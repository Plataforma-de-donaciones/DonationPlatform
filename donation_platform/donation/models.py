from django.db import models
from donation_platform.models import ArticlesType, ArticlesStates, Users, ArticlesZones
from django.utils import timezone
from PIL import Image

class Donation(models.Model):
    don_id = models.AutoField(primary_key=True)
    don_name = models.CharField(max_length=50)
    don_description = models.TextField()
    type = models.ForeignKey(ArticlesType, models.DO_NOTHING, related_name='donation_type')
    state = models.ForeignKey(ArticlesStates, models.DO_NOTHING, related_name='donation_state')
    don_attachment = models.ImageField(upload_to='static/')
    don_created_at = models.DateTimeField()
    user = models.ForeignKey(Users, models.DO_NOTHING, related_name='donation_user')
    zone = models.ForeignKey(ArticlesZones, models.DO_NOTHING, related_name='donation_zone')
    geom_point = models.TextField(blank=True, null=True)
    has_requests = models.BooleanField()
    request_count = models.IntegerField()
    don_confirmation_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'donation'
