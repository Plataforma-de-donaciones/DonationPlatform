from django.db import models
#from django.utils import timezone


class ArticlesType(models.Model):
    type_id = models.AutoField(primary_key=True)
    type_name = models.TextField()

    class Meta:
        managed = False
        db_table = 'articles_type'
