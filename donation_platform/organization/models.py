from django.db import models
from django.utils import timezone


class Organization(models.Model):
    org_name = models.CharField(max_length=50)
    org_email = models.CharField(max_length=50)
    org_description = models.TextField()

    class Meta:
        managed = False
        db_table = 'organization'

