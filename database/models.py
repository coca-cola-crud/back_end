# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

from django.db.models.signals import pre_save, pre_delete

from django.dispatch import receiver

from django.contrib.auth.models import User



class A(models.Model):
    xm = models.CharField(max_length=20, blank=True, null=True)
    gh = models.CharField(primary_key=True, max_length=10)
    sjhm = models.CharField(max_length=11, blank=True, null=True)
    yxdz = models.CharField(max_length=20, blank=True, null=True)
    xb = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'a'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class C(models.Model):
    kh = models.CharField(primary_key=True, max_length=10)
    km = models.CharField(max_length=20)
    xf = models.CharField(max_length=4)
    rkls = models.CharField(max_length=10)
    yx = models.CharField(max_length=20)
    gh = models.CharField(max_length=10)
    sksj = models.CharField(max_length=30)
    xkrs = models.IntegerField()
    xzrs = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'c'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class E(models.Model):
    xh = models.CharField(max_length=10)
    kh = models.CharField(max_length=10)
    km = models.CharField(max_length=20)
    xf = models.CharField(max_length=4)
    zpcj = models.CharField(max_length=4)
    rkls = models.CharField(max_length=10)
    sksj = models.CharField(max_length=30)
    id = models.CharField(primary_key=True, max_length=30)
    gh = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'e'


class S(models.Model):
    xh = models.CharField(primary_key=True, max_length=10)
    xm = models.CharField(max_length=10)
    nl = models.CharField(max_length=3)
    xb = models.CharField(max_length=4)
    yx = models.CharField(max_length=20)
    sjhm = models.CharField(max_length=11, blank=True, null=True)
    mm = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 's'


class T(models.Model):
    gh = models.CharField(primary_key=True, max_length=10)
    xm = models.CharField(max_length=20)
    xb = models.CharField(max_length=6)
    xl = models.CharField(max_length=10)
    yx = models.CharField(max_length=20)
    sjhm = models.CharField(max_length=11, blank=True, null=True)
    mm = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't'


class Y(models.Model):
    yxh = models.CharField(primary_key=True, max_length=10)
    yxm = models.CharField(max_length=20)
    dz = models.CharField(max_length=20)
    dh = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'y'

@receiver(pre_delete, sender=S)

def pre_delete_student(sender, instance, **kwargs):

     Xh = instance.xh

     course = E.objects.filter(xh=Xh)

     course.delete()





@receiver(pre_delete, sender=T)

def pre_delete_teacher(sender, instance, **kwargs):

     Gh= instance.gh

     course = C.objects.filter(gh=Gh)

     course.delete()



@receiver(pre_delete, sender=C)

def pre_delete_course(sender, instance, **kwargs):

     Kh= instance.kh

     course = E.objects.filter(kh=Kh)

     course.delete()

