from django.db import models
from donation_platform.models import Users
from django.utils import timezone
from PIL import Image

class News(models.Model):
    new_id = models.AutoField(primary_key=True)
    new_name = models.CharField(max_length=100)
    new_description = models.TextField()
    new_subject = models.CharField(max_length=70, blank=True, null=True)
    is_highlighted = models.BooleanField()
    views_count = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(Users, models.DO_NOTHING, related_name='news_user')
    new_created_at = models.DateTimeField()
    attachments = models.ImageField(upload_to='static/', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'news'

