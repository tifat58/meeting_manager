from django.shortcuts import render
from .models import *
from datetime import date
from company.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

# Create your views here.

@login_required
def add_user(request):

    context = {}
    user_list = UserDetail.objects.all().order_by('id')

    assigned_list = user_list.values('company_obj__member__id')
    member_list = CompanyMember.objects.exclude(id__in=assigned_list)
    group_list = GroupTable.objects.filter(isActive=True)

    if request.method=="POST":
        group = request.POST['group']
        username = request.POST['username']
        password = request.POST['password']
        member_details_list = CompanyMemberDetail.objects.filter(member_id=request.POST['member_name'])

        new_user = User(username=username,
                        password=password,
                        is_superuser=False,
                        is_active=True,
                        is_staff=True,
                        email='test@gmail.com',
                        date_joined=date.today())
        new_user.save()
        new_user.set_password(request.POST['password'])
        new_user.save()

        for list in member_details_list:

            new_user_detail_obj = UserDetail(user_obj=new_user,
                                             company_obj=list,
                                             user_type=group,
                                             isActive=True,
                                             isDelete=False,
                                             insertUser=request.user.id,
                                             insertDate=date.today())

            new_user_detail_obj.save()


    context['user_list'] = user_list
    context['member_list'] = member_list
    context['group_list'] = group_list

    return render(request, 'add_user.html', context)


@login_required
def add_user_group(request):

    context = {}
    if request.method == 'POST':
        group_name = request.POST['group_name']

        new_group_obj, created = GroupTable.objects.get_or_create(
            group_name = group_name,
            defaults= {
                'isActive' : True,
                'insertUser' : request.user.id,
                'insertDate' : date.today(),
                'project' : '1',

            }
        )

        if created:
            message = 'New user group is created'

        else:
            message = 'User group as same name already exists'

        context['message'] = message

    group_list = GroupTable.objects.all()

    context['group_list'] = group_list

    return render(request, 'add_user_group.html', context)

@login_required
def add_menu(request):
    context = {}

    return render(request, 'add_menu.html', context)

@login_required
def change_password(request):
    context = {}
    if request.method == 'POST':
        if request.user.check_password(request.POST['current_password']):
            request.user.set_password(request.POST['new_password'])
            request.user.save()
            update_session_auth_hash(request, request.user)
            context['message'] = '<p style="text-align: center; color: darkgreen;"><strong>Your account password has been updated!!!</strong> </p>'
        else:
            context['message'] = '<p style="text-align: center; color: darkred;"><strong>Current password did not match!!! Passoword has not been updated.</strong> </p>'


    return render(request, 'change_password.html', context)

