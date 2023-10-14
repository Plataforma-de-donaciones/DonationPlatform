from django.db import models
from donation_platform.models import ArticlesType, ArticlesStates, Users, ArticlesZones
from django.utils import timezone
from PIL import Image

class MedicalEquipment(models.Model):
    eq_id = models.AutoField(primary_key=True)
    eq_name = models.CharField(max_length=50)
    eq_description = models.TextField()
    type = models.ForeignKey(ArticlesType, models.DO_NOTHING, related_name='eq_type')
    state = models.ForeignKey(ArticlesStates, models.DO_NOTHING, related_name='eq_state')
    eq_created_at = models.DateTimeField()
    user = models.ForeignKey(Users, models.DO_NOTHING, related_name='eq_user')
    zone = models.ForeignKey(ArticlesZones, models.DO_NOTHING, related_name='eq_type')
    geom_point = models.TextField(blank=True, null=True)
    has_requests = models.BooleanField()
    request_count = models.IntegerField()
    eq_confirmation_date = models.DateTimeField(blank=True, null=True)
    eq_attachment = models.ImageField(upload_to='static/')

    class Meta:
        managed = False
        db_table = 'medical_equipment'

