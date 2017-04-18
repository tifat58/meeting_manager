__author__ = 'Tusfiqur'

from django.http import  HttpResponseRedirect
from django.shortcuts import render
from company.models import CompanyDetail
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User,Group
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from account.models import UserDetail
from django.core.exceptions import ObjectDoesNotExist
from agenda.models import Agenda, MemberVote, Meeting
from company.models import CompanyMemberDetail
from datetime import date, datetime


def login_page(request):
    context = {}
    company_list = CompanyDetail.objects.filter(isActive=True).order_by('abbreviated_name')
    context['company_list'] = company_list
    return render(request, 'login.html', context)

@login_required
def start_page(request, meeting_id):

    context = {}
    company_id = request.session['company']
    agenda_list = Agenda.objects.filter(isActive=True, meeting_agenda_id=meeting_id)
    try:
        meeting_obj = Meeting.objects.get(id=meeting_id)
    except:
        meeting_obj = "No Scheduled Meeting "

    display_list = []

    for list in agenda_list:
        try:
            agenda_vote = MemberVote.objects.get(vote_member=request.session['member_detail_id'], vote_agenda=list, isActive=True)
            vote_status = 'Active'
            if agenda_vote.vote == '1':
                vote_status = "Endorsed"
            if agenda_vote.vote == '2':
                vote_status = "Opposed"

            display_list.append({'id': list.id,
                                 'agenda_title': list.title,
                                 'create_date': list.insertDate,
                                 'vote_status': vote_status})

        except ObjectDoesNotExist:
            display_list.append({'id': list.id,
                                 'agenda_title': list.title,
                                 'create_date': list.insertDate,
                                 'vote_status': 'Active'})


    context['display_list'] = display_list
    context['active_agenda_list'] = agenda_list
    context['meeting'] = meeting_obj

    return render(request, 'home_page.html', context)

def dashboard_page(request):

    return render(request, 'dashboard_one.html')

def article_page(request):

    return render(request, 'article_template.html')

def login(request):
    context = {}

    '''if request.user.is_authenticated():
        print("False")
        return HttpResponseRedirect(reverse('start'))
    '''
    try:
        username = request.POST['username']
        password = request.POST['password']
        company = request.POST['company_name']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:

                try:
                    user_detail_obj = UserDetail.objects.get(isActive=True, user_obj=user, company_obj__member_company_id=company)
                    auth_login(request,user)
                    request.session['user_detail_id'] = user_detail_obj.id
                    request.session['member_detail_id'] = user_detail_obj.company_obj.id
                except ObjectDoesNotExist:
                    context['error'] = "No User for the company"
            else:
                context['error'] = 'Non active user'
        else:
            context['error'] = 'Wrong username or password'
    except:
        context['error'] = ''

    populateContext(request,context)

    if context['authenticated']:
        request.session['company'] = company
        #return HttpResponseRedirect(reverse('start'))
        return HttpResponseRedirect(reverse('start'))
    company_list = CompanyDetail.objects.filter(isActive=True).order_by('abbreviated_name')
    context['company_list'] = company_list
    return render(request, 'login.html', context)


@login_required
def meeting_list(request):

    context = {}
    try:
        get_ud_obj  = UserDetail.objects.get(id=request.session['user_detail_id'])
        get_meeting = Meeting.objects.filter(isActive=True, company_meeting=get_ud_obj.company_obj.member_company, start_date__gte=date.today())
        context['meeting_list'] = get_meeting

    except:
        pass


    return render(request, 'meeting_list.html', context)

def logout(request):
    context = {}
    try:
        auth_logout(request)
    except:
        context['error'] = 'some error occured'

    populateContext(request,context)
    return HttpResponseRedirect(reverse('login'))


def populateContext(request, context):
    context['authenticated'] = request.user.is_authenticated()
    if context['authenticated'] == True:
        context['username'] = request.user.username


