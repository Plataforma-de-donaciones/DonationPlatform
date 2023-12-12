from django.db import models

class Categories(models.Model):
    cat_id = models.AutoField(primary_key=True)
    cat_name = models.TextField()

    class Meta:
        managed = False
        db_table = 'categories'

