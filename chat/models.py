from django.db import models
from donation_platform.models import Users, Conversation
from django.utils import timezone

# Create your models here.
class Chat(models.Model):
    chat_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, models.DO_NOTHING, related_name='user_chat')
    conv = models.ForeignKey(Conversation, models.DO_NOTHING, related_name='conv_chat')
    content = models.TextField()
    sent_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chat'

