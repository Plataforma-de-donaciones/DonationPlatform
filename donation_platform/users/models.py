from django.db import models
from donation_platform.models import Organization
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

#class Users(models.Model):
 #   user_name = models.CharField(max_length=50)
  #  user_email = models.CharField(max_length=50, unique=True)
   # user_password = models.TextField()
    #organization = models.ForeignKey(Organization, models.DO_NOTHING, blank=True, null=True, related_name='users_organization')
    #user_state = models.IntegerField()
    #erased_at = models.DateTimeField(blank=True, null=True)
    #erased_reason = models.TextField(blank=True, null=True)
    #last_login = models.DateTimeField(default=timezone.now)

    #class Meta:
        #managed = False
        #db_table = 'users'
class CustomUserManager(BaseUserManager):
    def create_user(self, user_name, user_email, user_password, **extra_fields):
        if not user_email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(user_email)
        user = self.model(user_name=user_name, user_email=email, **extra_fields)
        user.set_password(user_password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_name, user_email, user_password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(user_name, user_email, user_password, **extra_fields)

class Users(AbstractBaseUser):
    user_name = models.CharField(max_length=50, unique=True)
    user_email = models.EmailField(unique=True)
    user_password = models.TextField()
    user_state = models.IntegerField()
    erased_at = models.DateTimeField(blank=True, null=True)
    erased_reason = models.TextField(blank=True, null=True)
    last_login = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'user_name'
    EMAIL_FIELD = 'user_email'
    REQUIRED_FIELDS = ['user_email', 'user_password']

    def __str__(self):
        return self.user_name

    @property
    def password(self):
        return self.user_password

    @password.setter
    def password(self, value):
        self.user_password = value

    class Meta:
        db_table = 'users'

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

