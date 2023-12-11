from django.db import models
from donation_platform.models import MedicalEquipment, Donation, Volunteer, Conversation, Users, Event, Requests, ArticlesZones, ArticlesStates, ArticlesType, Conversation, Sponsor
from django.utils import timezone

class Requests(models.Model):
    req_name = models.CharField(max_length=50)
    zone = models.ForeignKey(ArticlesZones, models.DO_NOTHING, related_name='req_zone')
    req_description = models.TextField()
    accept_terms = models.BooleanField()
    user = models.ForeignKey(Users, models.DO_NOTHING, related_name='req_user')
    eq = models.ForeignKey(MedicalEquipment, models.DO_NOTHING, related_name='req_eq', null=True)
    don = models.ForeignKey(Donation, models.DO_NOTHING,  related_name='req_donation', null=True)
    vol = models.ForeignKey(Volunteer, models.DO_NOTHING, related_name='req_volunteer', null=True)
    sponsor = models.ForeignKey(Sponsor, models.DO_NOTHING, related_name='req_sponsor', null=True)
    req_sent_date = models.DateTimeField()
    has_confirmation = models.BooleanField()
    confirmed_at = models.DateTimeField(blank=True, null=True)
    state = models.ForeignKey(ArticlesStates, models.DO_NOTHING, related_name='req_state')
    type = models.ForeignKey(ArticlesType, models.DO_NOTHING, related_name='req_type')
    conv = models.ForeignKey(Conversation, models.DO_NOTHING, related_name='req_conv', null=True)

    class Meta:
        managed = False
        db_table = 'requests'

