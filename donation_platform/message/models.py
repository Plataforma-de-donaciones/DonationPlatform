from django.db import models
from donation_platform.models import Users, Conversation
from django.utils import timezone

# Create your models here.
class Message(models.Model):
    mess_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, models.DO_NOTHING, db_column='user_id', related_name='user_mess')
    conv = models.ForeignKey(Conversation, models.DO_NOTHING, db_column='conv_id', related_name='conv_mess')
    content = models.TextField()
    sent_date = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'message'

