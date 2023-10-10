from django.db import models
from donation_platform.models import Organization
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Users(models.Model):
    user_name = models.CharField(max_length=50)
    user_email = models.CharField(max_length=50, unique=True)
    user_password = models.TextField()
    organization = models.ForeignKey(Organization, models.DO_NOTHING, blank=True, null=True, related_name='users_organization')
    user_state = models.IntegerField()
    erased_at = models.DateTimeField(blank=True, null=True)
    erased_reason = models.TextField(blank=True, null=True)
    last_login = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'users'
        
    def __str__(self):
        return self.user_name
    
    @property
    def is_authenticated(self):
        return True
class Administrator(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name='user_administrator_user')
    start_date = models.DateTimeField()
    organization = models.ForeignKey(Organization, models.DO_NOTHING, blank=True, null=True, related_name='user_administrator_organization')
    administrator_state = models.IntegerField()
    erased_at = models.DateTimeField(blank=True, null=True)
    erase_reason = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'administrator'

class Moderator(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name='user_moderator_user')
    start_date = models.DateTimeField()
    organization = models.ForeignKey(Organization, models.DO_NOTHING, blank=True, null=True, related_name='user_moderator_organization')
    moderator_state = models.IntegerField()
    erased_at = models.DateTimeField(blank=True, null=True)
    erased_reason = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'moderator'

@receiver(pre_save, sender=Users, dispatch_uid="pre_save_user_signal")
def update_administrator_state(sender, instance, **kwargs):
    if instance.user_state == 0:
        Administrator.objects.filter(user=instance).update(administrator_state=0)

# Verificar el estado del usuario antes de crear un administrador
def create_administrator(user, start_date, organization, administrator_state):
    if user.user_state == 1:
        Administrator.objects.create(user=user, start_date=start_date, organization=organization, administrator_state=administrator_state)
    else:
        raise ValueError("El usuario debe estar activo para crear un administrador.")

@receiver(pre_save, sender=Users, dispatch_uid="pre_save_moderator_signal")
def update_moderator_state(sender, instance, **kwargs):
    if instance.user_state == 0:
        Moderator.objects.filter(user=instance).update(moderator_state=0)

# Verificar el estado del usuario antes de crear un moderador
def create_moderator(user, start_date, organization, moderator_state):
    if user.user_state == 1:
        Moderator.objects.create(user=user, start_date=start_date, organization=organization, moderator_state=moderator_state)
    else:
        raise ValueError("El usuario debe estar activo para crear un moderador.")

