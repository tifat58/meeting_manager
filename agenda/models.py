from django.db import models
from company.models import CompanyDetail, CompanyMemberDetail

# Create your models here.

class Meeting(models.Model):

    DEFAULT_COMPANY_ID = -1

    title = models.CharField(max_length=300)
    meeting_no = models.CharField(max_length=10, null=True, blank=True)
    description = models.CharField(max_length=1000)
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    company_meeting = models.ForeignKey(CompanyDetail, on_delete=models.CASCADE, default=DEFAULT_COMPANY_ID, null=True, blank=True) #relation with companyDetail table
    isActive = models.NullBooleanField()
    isDelete = models.NullBooleanField()
    insertUser = models.CharField(max_length=50)
    insertDate = models.DateField(blank=True, null=True)
    updateUser = models.CharField(max_length=50)
    updateDate = models.DateField(blank=True, null=True)
    project = models.CharField(max_length=100)


class Agenda(models.Model):

    DEFAULT_MEETING_ID = -1

    title = models.CharField(max_length=300)
    short_description = models.CharField(max_length=500, null=True, blank=True)
    full_article = models.TextField(max_length=429496729)
    meeting_agenda = models.ForeignKey(Meeting, on_delete=models.CASCADE, null=True, blank=True) #relation with Meeting Table
    isActive = models.NullBooleanField()
    isDelete = models.NullBooleanField()
    insertUser = models.CharField(max_length=50)
    insertDate = models.DateField(blank=True, null=True)
    updateUser = models.CharField(max_length=50)
    updateDate = models.DateField(blank=True, null=True)
    project = models.CharField(max_length=100)



class MemberVote(models.Model):

    VOTE_IN_CHOICE = (
        ('pending','0'),
        ('Endorsed','1'),
        ('Opposed','2')
    )

    vote_member = models.ForeignKey(CompanyMemberDetail, on_delete=models.CASCADE)
    vote_agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE)
    vote = models.CharField(max_length=50, default='0', choices=VOTE_IN_CHOICE)
    isActive = models.NullBooleanField(default=True)
    isDelete = models.NullBooleanField(default=False)
    insertUser = models.CharField(max_length=50, default='system')
    insertDate = models.DateTimeField(blank=True, null=True, default=None)
    updateUser = models.CharField(max_length=50, blank=True, null=True, default=None)
    updateDate = models.DateTimeField(blank=True, null=True, default=None)
    project = models.CharField(max_length=100,default='1')


class MemberRemarks(models.Model):
    remarks_member = models.ForeignKey(CompanyMemberDetail, on_delete=models.CASCADE)
    remarks_agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE)
    comment = models.TextField(max_length=1200)
    isActive = models.NullBooleanField(default=True)
    isDelete = models.NullBooleanField(default=False)
    insertUser = models.CharField(max_length=50, default='system')
    insertDate = models.DateTimeField(blank=True, null=True, default=None)
    updateUser = models.CharField(max_length=50, blank=True, null=True, default=None)
    updateDate = models.DateTimeField(blank=True, null=True, default=None)
    project = models.CharField(max_length=100,default='1')











