from django.db import models
from django.contrib.auth.models import User
import os
from datetime import date

# Create your models here.

class CompanyDetail(models.Model):
    company_name = models.CharField(max_length=200)
    abbreviated_name = models.CharField(max_length=20)
    company_description = models.CharField(max_length=500, null=True, blank=True)
    isActive = models.NullBooleanField()
    isDelete = models.NullBooleanField()
    insertUser = models.CharField(max_length=50)
    insertDate = models.DateField(blank=True, null=True)
    updateUser = models.CharField(max_length=50)
    updateDate = models.DateField(blank=True, null=True)
    project = models.CharField(max_length=100)


class Designation(models.Model):
    designation_title = models.CharField(max_length=50)
    description = models.CharField(max_length=200, null=True, blank=True)
    isActive = models.NullBooleanField()
    isDelete = models.NullBooleanField()
    insertUser = models.CharField(max_length=50)
    insertDate = models.DateField(blank=True, null=True)
    updateUser = models.CharField(max_length=50)
    updateDate = models.DateField(blank=True, null=True)
    project = models.CharField(max_length=100)


def upload_location(instance, filename):
    filebase, extension = filename.split(".")
    return "images/members/%s" %(filename)

class CompanyMember(models.Model):

    GENDER_IN_CHOICE = (
        ('1', 'Mr.'),
        ('2', 'Ms.')
    )
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=40, choices=GENDER_IN_CHOICE, null=True, blank=True)
    name = models.CharField(max_length=300)
    photo = models.ImageField(upload_to=upload_location,
                              null=True,
                              blank=True,
                              width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    isActive = models.NullBooleanField(default=True)
    isDelete = models.NullBooleanField(default=False)
    insertUser = models.CharField(max_length=50, default='system')
    insertDate = models.DateField(blank=True, null=True, default=None)
    updateUser = models.CharField(max_length=50, blank=True, null=True, default=None)
    updateDate = models.DateField(blank=True, null=True, default=None)
    project = models.CharField(max_length=100,default='1')
    user_field = models.OneToOneField(User, null=True, blank=True, default=None, on_delete=models.CASCADE)


class CompanyMemberDetail(models.Model):
    member = models.ForeignKey(CompanyMember, on_delete=models.CASCADE)
    member_company = models.ForeignKey(CompanyDetail, on_delete=models.CASCADE)
    member_designation = models.ForeignKey(Designation, on_delete=models.CASCADE)
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    isActive = models.NullBooleanField(default=True)
    isDelete = models.NullBooleanField(default=False)
    insertUser = models.CharField(max_length=50, default='system')
    insertDate = models.DateField(blank=True, null=True, default=None)
    updateUser = models.CharField(max_length=50, blank=True, null=True, default=None)
    updateDate = models.DateField(blank=True, null=True, default=None)
    project = models.CharField(max_length=100,default='1')
