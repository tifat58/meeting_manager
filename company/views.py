from django.shortcuts import render

from django.views.generic import  TemplateView
from .models import *
from datetime import datetime, date
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from account.models import UserDetail
# Create your views here.

@login_required
class CompanyView(TemplateView):

    template_name = "add_company.html"

    def get_context_data(self, **kwargs):

        context = super(CompanyView, self).get_context_data(**kwargs)

        return context

@login_required
def add_company(request):

    context = {}
    if request.method == "POST":
        company_obj, created = CompanyDetail.objects.get_or_create(company_name = request.POST['company_name'],
                                                             defaults={'abbreviated_name' : request.POST['abbreviated_name'],
                                                                       'company_description' : request.POST['company_description'],
                                                                       'isActive' : True,
                                                                       'insertDate' : date.today()})

        if created:
            message = "New Company is Added"
            context['message'] = message

    company_list = CompanyDetail.objects.filter(isActive=True).order_by('id')
    context['company_list'] = company_list

    return render(request, 'add_company.html', context)


@login_required
def add_designation(request):

    context = {}

    if request.method == "POST":
        designation_obj, created = Designation.objects.get_or_create(designation_title = request.POST['designation_name'],
                                                                     defaults={'description' : request.POST['designation_description'],
                                                                               'isActive' : True,
                                                                               'insertDate' : date.today()})

        if created:
            message = "New Designation is Added"
            context['message'] = message

        else:
            message = "Desigantion is Already created"
            context['message'] = message

    designation_list = Designation.objects.filter(isActive=True).order_by('id')
    context['designation_list'] = designation_list

    return render(request, 'add_designation.html', context)

@login_required
def add_company_member(request):

    context = {}

    if request.method == "POST":

        member_photo = request.FILES['image']
        username = request.POST['member_username']
        password = request.POST['member_password']
        '''
        member_obj, created = CompanyMember.objects.get_or_create(name = request.POST['member_name'],
                                                                  defaults={'title' : request.POST['title'],
                                                                            'photo' : member_photo,
                                                                            'isActive' : True,

                                                                            'insertDate' : date.today()})
                                                                            '''
        try:
            new_member = CompanyMember(name=request.POST['member_name'],
                                       title=request.POST['title'],
                                       photo=member_photo,
                                       isActive=True,
                                       insertDate=date.today())

            #group = request.POST['group']

            #member_details_list = CompanyMemberDetail.objects.filter(member_id=request.POST['member_name'])

            new_user = User(username=username,
                            password=password,
                            is_superuser=False,
                            is_active=True,
                            is_staff=True,
                            email='test@gmail.com',
                            date_joined=date.today())
            new_user.save()
            new_user.set_password(request.POST['member_password'])
            new_user.save()
            new_member.user_field = new_user
            new_member.save()
            message = "New Member is created Successfully"
        except:
            message = "Not created"

        context['message'] = message

    return render(request, 'add_company_member.html', context)

@login_required
def add_member_details(request):
    context = {}

    company_list = CompanyDetail.objects.filter(isActive=True).order_by('abbreviated_name')
    context['company_list'] = company_list

    designation_list = Designation.objects.filter(isActive=True).order_by('designation_title')
    context['designation_list'] = designation_list

    member_list = CompanyMember.objects.filter(isActive=True).order_by('name')
    context['member_list'] = member_list
    ''' #working
    if request.method == "POST":
        from_date = datetime.strptime(request.POST['start'], "%m/%d/%Y")
        member_detail_obj, created = CompanyMemberDetail.objects.get_or_create(member_id = request.POST['member'],
                                                                               member_company_id = request.POST['company'],
                                                                               member_designation_id = request.POST['designation'],
                                                                               defaults={'isActive' : True,
                                                                                         'insertDate' : date.today(),
                                                                                         'project' : '1',
                                                                                         'from_date' : from_date,
                                                                                         'to_date' : datetime.max.date()
                                                                               })

        if created:
            message = "Member details has been created"


        else:
            message = "Already created"

        context['message'] = message
        '''
    #temporary
    if request.method == "POST":
        from_date = datetime.strptime(request.POST['start'], "%m/%d/%Y")
        member_id = request.POST['member']
        #get_user_detail_obj = UserDetail.objects.filter(isActive=True, company_obj__member__id=member_id)[0]
        get_company_member = CompanyMember.objects.get(id=member_id)
        member_detail_obj, created = CompanyMemberDetail.objects.get_or_create(member_id = request.POST['member'],
                                                                               member_company_id = request.POST['company'],
                                                                               member_designation_id = request.POST['designation'],
                                                                               defaults={'isActive' : True,
                                                                                         'insertDate' : date.today(),
                                                                                         'project' : '1',
                                                                                         'from_date' : from_date,
                                                                                         'to_date' : datetime.max.date()
                                                                               })



        if created:
            message = "Member details has been created"
            new_user_detail_obj = UserDetail(user_obj=get_company_member.user_field,
                                             company_obj=member_detail_obj,
                                             user_type='2',
                                             isActive=True,
                                             isDelete=False,
                                             insertUser=request.user.id,
                                             insertDate=date.today())

            new_user_detail_obj.save()

        else:
            message = "Already created"

        context['message'] = message

    member_designation_list = CompanyMemberDetail.objects.filter(isActive=True).order_by('member__name')
    context['member_designation_list'] = member_designation_list

    return render(request, 'add_member_details.html', context)