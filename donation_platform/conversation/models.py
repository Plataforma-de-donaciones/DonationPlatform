from django.db import models
from donation_platform.models import Users

# Create your models here.
class Conversation(models.Model):
    conv_id = models.AutoField(primary_key=True)
    user_1 = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='conversation_user_1')
    user_2 = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='conversation_user_2')

    class Meta:
        managed = False
        db_table = 'conversation'

