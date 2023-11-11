from django.db import models
#from donation_platform.models import Attachments
from django.utils import timezone

class Attachments(models.Model):
    atta_id = models.AutoField(primary_key=True)
    atta_url = models.TextField()

    class Meta:
        managed = False
        db_table = 'attachments'
