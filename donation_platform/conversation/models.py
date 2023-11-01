from django.db import models
from donation_platform.models import Users

# Create your models here.
class Conversation(models.Model):
    conv_id = models.AutoField(primary_key=True)
    user_1 = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_1', related_name='user1_conversations1')
    user_2 = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_2', related_name='user2_conversations2')

    class Meta:
        managed = False
        db_table = 'conversation'

