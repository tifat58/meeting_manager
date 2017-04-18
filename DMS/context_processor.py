__author__ = 'Tusfiqur'
from account.models import UserDetail
from django.core.exceptions import ObjectDoesNotExist
from agenda.models import Meeting
from datetime import date

def get_member_detail(request):
    user_name = 'Invalid User'
    user_designation = 'None'
    current_meeting = 'No Scheduled Meeting'
    member_id = '0'
    profile_url = 'None'
    company_name = "None"
    try:
        user_detail_object = UserDetail.objects.get(id=request.session['user_detail_id'])
        user_name = user_detail_object.company_obj.member.name
        user_designation = user_detail_object.company_obj.member_designation.designation_title
        member_id = user_detail_object.company_obj.id
        profile_url = user_detail_object.company_obj.member.photo.url
        company_name = user_detail_object.company_obj.member_company.company_name

        get_meeting = Meeting.objects.filter(isActive=True, company_meeting=user_detail_object.company_obj.member_company, start_date__gte=date.today())[0]

        current_meeting = get_meeting.title
    except:
        pass

    return {'user_name' : user_name, 'user_designation' : user_designation, 'current_meeting' : current_meeting, 'member_id' : member_id, 'profile_url' : profile_url, 'company_name' : company_name }

