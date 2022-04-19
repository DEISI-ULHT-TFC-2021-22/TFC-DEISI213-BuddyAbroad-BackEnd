# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Languages(models.Model):
    name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'Languages'


class InterestCategories(models.Model):
    name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'InterestCategories'


class Interests(models.Model):
    name = models.CharField(max_length=45, blank=True, null=True)
    category = models.ForeignKey(InterestCategories, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Interests'


class Trips(models.Model):
    name = models.CharField(max_length=45, blank=True, null=True)
    description = models.CharField(max_length=45, blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    image = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=45, blank=True, null=True)
    details = models.CharField(max_length=45, blank=True, null=True)
    maxsize = models.IntegerField(db_column='maxSize', blank=True, null=True)  # Field name made lowercase.
    duration = models.IntegerField(blank=True, null=True)
    guide = models.ForeignKey('Users', models.DO_NOTHING)

    class Meta:
        db_table = 'Trips'


class BuddyMatchTourist(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    language = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    participants = models.CharField(max_length=100, blank=True, null=True)
    buddy = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'buddy_match_tourist'


class Messages(models.Model):
    message = models.CharField(max_length=400, blank=True, null=True)
    sender = models.ForeignKey('Users', models.DO_NOTHING,related_name="sender", db_column='sender', blank=True, null=True)
    recipient = models.ForeignKey('Users', models.DO_NOTHING, db_column='recipient', blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'messages'
        unique_together = (('sender', 'recipient'),)


class Roles(models.Model):
    description = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)

    class Meta:
        db_table = 'roles'


class UserTrips(models.Model):
    paidprice = models.FloatField(db_column='paidPrice', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    status = models.CharField(max_length=45, blank=True, null=True)
    groupsize = models.IntegerField(db_column='groupSize', blank=True, null=True)  # Field name made lowercase.
    user_tripscol = models.CharField(max_length=45, blank=True, null=True)
    guide = models.ForeignKey('Users',models.DO_NOTHING)
    tourist = models.ForeignKey('Users',models.DO_NOTHING,related_name="tourist")
    reference = models.ForeignKey(Trips, models.DO_NOTHING)

    class Meta:
        db_table = 'user_trips'


class Users(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    dob = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    image = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    tourcount = models.IntegerField(db_column='tourCount', blank=True, null=True)  # Field name made lowercase.
    guide = models.BooleanField(blank=True, null=True)
    interests = models.ManyToManyField(Interests, blank=True)
    languages = models.ManyToManyField(Languages, blank=True)

    class Meta:
        db_table = 'users'


