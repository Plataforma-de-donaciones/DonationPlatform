from django.db import models
#from django.utils import timezone


class ArticlesZones(models.Model):
    zone_id = models.AutoField(primary_key=True)
    zone_name = models.TextField()

    class Meta:
        managed = False
        db_table = 'articles_zones'

