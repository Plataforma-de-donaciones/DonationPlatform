from django.db import models
from donation_platform.models import Categories, MedicalEquipment
#from django.utils import timezone


class CategoriesMeq(models.Model):
    cat = models.ForeignKey(Categories, models.DO_NOTHING)
    eq = models.ForeignKey(MedicalEquipment, models.DO_NOTHING, related_name='cat_eq')

    class Meta:
        managed = False
        db_table = 'categories_meq'

