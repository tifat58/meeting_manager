from django.db import models
from django.contrib.auth.models import User
from company.models import CompanyDetail, CompanyMember, CompanyMemberDetail


# Create your models here.


class UserDetail(models.Model):
    user_obj = models.ForeignKey(User)
    company_obj = models.ForeignKey(CompanyMemberDetail, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=100)
    isActive = models.NullBooleanField(default=True)
    isDelete = models.NullBooleanField(default=False)
    insertUser = models.CharField(max_length=50, default='system')
    insertDate = models.DateField(blank=True, null=True, default=None)
    updateUser = models.CharField(max_length=50, blank=True, null=True, default=None)
    updateDate = models.DateField(blank=True, null=True, default=None)
    project = models.CharField(max_length=100,default='1')



class MenuTable(models.Model):
    menu_string = models.CharField(max_length=100)
    url_string = models.CharField(max_length=250)
    parent_id = models.ForeignKey("self", blank=True,null=True)
    group_permission_id = models.CharField(max_length=50)
    has_child = models.NullBooleanField(default="null")
    isActive = models.NullBooleanField()
    isDelete = models.NullBooleanField()
    insertUser = models.CharField(max_length=50)
    insertDate = models.DateField(blank=True, null=True)
    updateUser = models.CharField(max_length=50, blank=True, null=True)
    updateDate = models.DateField(blank=True, null=True)
    project = models.CharField(max_length=100)



class GroupTable(models.Model):
    group_name = models.CharField(max_length=200)
    isActive = models.NullBooleanField(default=True)
    isDelete = models.NullBooleanField(default=False)
    insertUser = models.CharField(max_length=50, default='system')
    insertDate = models.DateField(blank=True, null=True, default=None)
    updateUser = models.CharField(max_length=50, blank=True, null=True, default=None)
    updateDate = models.DateField(blank=True, null=True, default=None)
    project = models.CharField(max_length=100,default='1')

class UserGroupTable(models.Model):
    user_id = models.ForeignKey(UserDetail)
    group_id = models.ForeignKey(GroupTable)
    isActive = models.NullBooleanField(default=True)
    isDelete = models.NullBooleanField(default=False)
    insertUser = models.CharField(max_length=50, default='system')
    insertDate = models.DateField(blank=True, null=True, default=None)
    updateUser = models.CharField(max_length=50, blank=True, null=True, default=None)
    updateDate = models.DateField(blank=True, null=True, default=None)
    project = models.CharField(max_length=100,default='1')

class MenuGroupTable(models.Model):
    menu_id = models.ForeignKey(MenuTable)
    menu_group_id = models.ForeignKey(GroupTable)
    isActive = models.NullBooleanField(default=True)
    isDelete = models.NullBooleanField(default=False)
    insertUser = models.CharField(max_length=50, default='system')
    insertDate = models.DateField(blank=True, null=True, default=None)
    updateUser = models.CharField(max_length=50, blank=True, null=True, default=None)
    updateDate = models.DateField(blank=True, null=True, default=None)
    project = models.CharField(max_length=100,default='1')

