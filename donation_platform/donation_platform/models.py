# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils import timezone

class Administrator(models.Model):
    user = models.OneToOneField('Users', on_delete=models.CASCADE, related_name="donation_platform_administrator_user")
    start_date = models.DateTimeField()
    organization = models.ForeignKey('Organization', models.DO_NOTHING, blank=True, null=True, related_name='donation_platform_administrator_organization')
    administrator_state = models.IntegerField()
    erased_at = models.DateTimeField(blank=True, null=True)
    erase_reason = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'administrator'


class ArticlesStates(models.Model):
    state_id = models.AutoField(primary_key=True)
    state_name = models.TextField()

    class Meta:
        managed = False
        db_table = 'articles_states'


class ArticlesType(models.Model):
    type_id = models.AutoField(primary_key=True)
    type_name = models.TextField()

    class Meta:
        managed = False
        db_table = 'articles_type'


class ArticlesZones(models.Model):
    zone_id = models.AutoField(primary_key=True)
    zone_name = models.TextField()

    class Meta:
        managed = False
        db_table = 'articles_zones'


class Attachments(models.Model):
    atta_id = models.AutoField(primary_key=True)
    atta_url = models.TextField()

    class Meta:
        managed = False
        db_table = 'attachments'


class AttachmentsEvent(models.Model):
    atta = models.ForeignKey(Attachments, models.DO_NOTHING)
    event = models.ForeignKey('Event', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'attachments_event'


class AttachmentsNew(models.Model):
    atta = models.ForeignKey(Attachments, models.DO_NOTHING)
    new = models.ForeignKey('News', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'attachments_new'


class Categories(models.Model):
    cat_id = models.AutoField(primary_key=True)
    cat_name = models.TextField()

    class Meta:
        managed = False
        db_table = 'categories'


class CategoriesDon(models.Model):
    cat = models.ForeignKey(Categories, models.DO_NOTHING)
    don = models.ForeignKey('Donation', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'categories_don'


class CategoriesEve(models.Model):
    cat = models.ForeignKey(Categories, models.DO_NOTHING)
    event = models.ForeignKey('Event', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'categories_eve'


class CategoriesMeq(models.Model):
    cat = models.ForeignKey(Categories, models.DO_NOTHING)
    eq = models.ForeignKey('MedicalEquipment', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'categories_meq'


class CategoriesNew(models.Model):
    cat = models.ForeignKey(Categories, models.DO_NOTHING)
    new = models.ForeignKey('News', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'categories_new'


class Conversation(models.Model):
    conv_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'conversation'


class Donation(models.Model):
    don_id = models.AutoField(primary_key=True)
    don_name = models.CharField(max_length=50)
    don_description = models.TextField()
    type = models.ForeignKey(ArticlesType, models.DO_NOTHING)
    state = models.ForeignKey(ArticlesStates, models.DO_NOTHING)
    don_attachment = models.TextField(blank=True, null=True)
    don_created_at = models.DateTimeField()
    user = models.ForeignKey('Users', models.DO_NOTHING)
    zone = models.ForeignKey(ArticlesZones, models.DO_NOTHING)
    geom_point = models.TextField(blank=True, null=True)
    has_requests = models.BooleanField()
    request_count = models.IntegerField()
    don_confirmation_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'donation'


class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=50)
    event_description = models.TextField()
    type = models.ForeignKey(ArticlesType, models.DO_NOTHING)
    state = models.ForeignKey(ArticlesStates, models.DO_NOTHING)
    event_date = models.DateTimeField()
    user = models.ForeignKey('Users', models.DO_NOTHING)
    zone = models.ForeignKey(ArticlesZones, models.DO_NOTHING)
    geom_point = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    organization = models.ForeignKey('Organization', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'event'


class MedicalEquipment(models.Model):
    eq_id = models.AutoField(primary_key=True)
    eq_name = models.CharField(max_length=50)
    eq_description = models.TextField()
    type = models.ForeignKey(ArticlesType, models.DO_NOTHING)
    state = models.ForeignKey(ArticlesStates, models.DO_NOTHING)
    eq_created_at = models.DateTimeField()
    user = models.ForeignKey('Users', models.DO_NOTHING)
    zone = models.ForeignKey(ArticlesZones, models.DO_NOTHING)
    geom_point = models.TextField(blank=True, null=True)
    has_requests = models.BooleanField()
    request_count = models.IntegerField()
    eq_confirmation_date = models.DateTimeField(blank=True, null=True)
    eq_attachment = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'medical_equipment'


class Message(models.Model):
    mess_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    conv = models.ForeignKey(Conversation, models.DO_NOTHING)
    content = models.TextField()
    sent_date = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'message'


class Moderator(models.Model):
    user = models.OneToOneField('Users', on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    organization = models.ForeignKey('Organization', models.DO_NOTHING)
    moderator_state = models.IntegerField()
    erased_at = models.DateTimeField(blank=True, null=True)
    erased_reason = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'moderator'


class News(models.Model):
    new_id = models.AutoField(primary_key=True)
    new_name = models.CharField(max_length=100)
    new_description = models.TextField()
    new_subject = models.CharField(max_length=70, blank=True, null=True)
    is_highlighted = models.BooleanField()
    views_count = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    new_created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'news'


class Notifications(models.Model):
    noti_id = models.AutoField(primary_key=True)
    noti_title = models.CharField(max_length=50)
    noti_content = models.TextField()
    noti_date = models.DateTimeField(blank=True, null=True)
    was_read = models.BooleanField()
    eq = models.ForeignKey(MedicalEquipment, models.DO_NOTHING, null=True)
    don = models.ForeignKey(Donation, models.DO_NOTHING, null=True)
    vol = models.ForeignKey('Volunteer', models.DO_NOTHING, null=True)
    sponsor = models.ForeignKey('Sponsor', models.DO_NOTHING, null=True)
    event = models.ForeignKey(Event, models.DO_NOTHING, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    conv = models.ForeignKey(Conversation, models.DO_NOTHING, null=True)
    request = models.ForeignKey('Requests', models.DO_NOTHING, null=True)

    class Meta:
        managed = False
        db_table = 'notifications'


class Organization(models.Model):
    org_name = models.CharField(max_length=50, unique=True)
    org_email = models.CharField(max_length=50, unique=True)
    org_description = models.TextField()

    class Meta:
        managed = False
        db_table = 'organization'


class Requests(models.Model):
    req_name = models.CharField(max_length=50)
    zone = models.ForeignKey(ArticlesZones, models.DO_NOTHING)
    req_description = models.TextField()
    accept_terms = models.BooleanField()
    user = models.ForeignKey('Users', models.DO_NOTHING)
    eq = models.ForeignKey(MedicalEquipment, models.DO_NOTHING, null=True)
    don = models.ForeignKey(Donation, models.DO_NOTHING, null=True)
    vol = models.ForeignKey('Volunteer', models.DO_NOTHING, null=True)
    req_sent_date = models.DateTimeField()
    has_confirmation = models.BooleanField()
    confirmed_at = models.DateTimeField(blank=True, null=True)
    state = models.ForeignKey(ArticlesStates, models.DO_NOTHING)
    type = models.ForeignKey(ArticlesType, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'requests'


class Sponsor(models.Model):
    sponsor_id = models.AutoField(primary_key=True)
    sponsor_name = models.CharField(max_length=50)
    sponsor_description = models.TextField()
    type = models.ForeignKey(ArticlesType, models.DO_NOTHING)
    state = models.ForeignKey(ArticlesStates, models.DO_NOTHING)
    sponsor_attachment = models.TextField(blank=True, null=True)
    sponsor_created_at = models.DateTimeField()
    user = models.ForeignKey('Users', models.DO_NOTHING)
    zone = models.ForeignKey(ArticlesZones, models.DO_NOTHING)
    geom_point = models.TextField(blank=True, null=True)
    has_requests = models.BooleanField()
    request_count = models.IntegerField()
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    organization = models.ForeignKey(Organization, models.DO_NOTHING, null=True)

    class Meta:
        managed = False
        db_table = 'sponsor'


class Users(models.Model):
    user_name = models.CharField(max_length=50)
    user_email = models.CharField(max_length=50, unique=True)
    user_password = models.TextField()
    organization = models.ForeignKey(Organization, models.DO_NOTHING, blank=True, null=True)
    user_state = models.IntegerField()
    erased_at = models.DateTimeField(blank=True, null=True)
    erased_reason = models.TextField(blank=True, null=True)
    last_login = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'users'


class Volunteer(models.Model):
    vol_id = models.AutoField(primary_key=True)
    vol_name = models.CharField(max_length=50)
    vol_description = models.TextField()
    type = models.ForeignKey(ArticlesType, models.DO_NOTHING)
    state = models.ForeignKey(ArticlesStates, models.DO_NOTHING)
    vol_tasks = models.TextField(blank=True, null=True)
    vol_created_at = models.DateTimeField()
    user = models.ForeignKey(Users, models.DO_NOTHING)
    zone = models.ForeignKey(ArticlesZones, models.DO_NOTHING)
    geom_point = models.TextField(blank=True, null=True)
    has_requests = models.BooleanField()
    request_count = models.IntegerField()
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    vol_rating = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'volunteer'
