from django.db import models
#from django.utils import timezone


class ArticlesStates(models.Model):
    state_id = models.AutoField(primary_key=True)
    state_name = models.TextField()

    class Meta:
        managed = False
        db_table = 'articles_states'
