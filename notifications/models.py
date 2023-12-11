from django.db import models
from donation_platform.models import MedicalEquipment, Donation, Volunteer, Sponsor, Conversation, Users, Event, Requests
from django.utils import timezone

class Notifications(models.Model):
    noti_id = models.AutoField(primary_key=True)
    noti_title = models.CharField(max_length=50)
    noti_content = models.TextField()
    noti_date = models.DateTimeField(blank=True, null=True)
    was_read = models.BooleanField()
    eq = models.ForeignKey(MedicalEquipment, models.DO_NOTHING, related_name='noti_eq', null=True)
    don = models.ForeignKey(Donation, models.DO_NOTHING, related_name='noti_don', null=True)
    vol = models.ForeignKey(Volunteer, models.DO_NOTHING, related_name='noti_vol', null=True)
    sponsor = models.ForeignKey(Sponsor, models.DO_NOTHING, related_name='noti_sponsor', null=True)
    event = models.ForeignKey(Event, models.DO_NOTHING, related_name='noti_event', null=True)
    user = models.ForeignKey(Users, models.DO_NOTHING, related_name='noti_user')
    conv = models.ForeignKey(Conversation, models.DO_NOTHING, related_name='noti_conv', null=True)
    request = models.ForeignKey(Requests, models.DO_NOTHING, related_name='noti_req', null=True)

    class Meta:
        managed = False
        db_table = 'notifications'

