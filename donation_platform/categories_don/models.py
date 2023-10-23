from django.db import models
from donation_platform.models import Categories, Donation
#from django.utils import timezone


class CategoriesDon(models.Model):
    cat = models.ForeignKey(Categories, models.DO_NOTHING, related_name='cat_cat2')
    don = models.ForeignKey(Donation, models.DO_NOTHING, related_name='cat_don')

    class Meta:
        managed = False
        db_table = 'categories_don'
