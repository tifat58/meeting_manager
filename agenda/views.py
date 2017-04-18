from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import *
from company.models import CompanyDetail, CompanyMemberDetail
from datetime import date, datetime
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from account.models import UserDetail
# Create your views here.


def test(request):


    return HttpResponse("helllo")

@login_required
def add_meeting(request):

    context = {}
    if request.method == "POST":
        meeting_no = request.POST['meeting_no']
        meeting_title = request.POST['meeting_title']
        meeting_description = request.POST['meeting_description']
        start_date = datetime.strptime(request.POST['start'], "%m/%d/%Y")
        end_date = datetime.strptime(request.POST['end'], "%m/%d/%Y")
        # company_id = request.POST['company_id']

        company_id = request.session['company']

        meeting_obj, created = Meeting.objects.get_or_create(title = meeting_title,
                                                             defaults={'meeting_no' : meeting_no,
                                                                       'description' : meeting_description,
                                                                       'start_date' : start_date,
                                                                       'end_date' : end_date,
                                                                       'isActive' : True,
                                                                       'insertDate' : date.today(),
                                                                       'company_meeting': get_object_or_404(CompanyDetail, id=company_id)})

        if created:
            message = "New Meeting is Scheduled"
            context['message'] = message

    active_company_list = CompanyDetail.objects.filter(isActive=True)
    context['company_list'] = active_company_list

    return render(request, 'add_meeting.html', context)


@login_required
def add_agenda(request):

    context = {}
    company_id = request.session['company']

    if request.is_ajax():

        data = {}
        company = request.POST.get('company')
        meeting_list_objects = Meeting.objects.filter(company_meeting_id=company, isActive=True).order_by('-start_date')
        meeting_list = []
       # print(meeting_list_objects)
        for obj in meeting_list_objects:
            print(obj.title)
            meeting_list.append({'meeting_id' : obj.id, 'meeting_name' : obj.title})

        data['meeting_list'] = meeting_list

        return JsonResponse(data)

    if request.method == "POST":

        # company_id = request.POST['company_id']
        company_id = request.session['company']
        meeting_id = request.POST['meeting']
        agenda_title = request.POST['agenda_title']
        #meeting_description = request.POST['description']
        raw_description = request.POST['raw_html']

        agenda_obj = Agenda(title = agenda_title,
                            full_article=raw_description,
                            meeting_agenda_id=meeting_id,
                            isActive = True,
                            isDelete = False,
                            insertUser = 1,
                            insertDate = date.today(),
                            project = '1',
                            updateUser=1)

        agenda_obj.save()



    active_company_list = CompanyDetail.objects.filter(isActive=True)
    context['company_list'] = active_company_list

    active_meeting_list = Meeting.objects.filter(company_meeting_id=company_id, isActive=True).order_by('-start_date')
    context['active_meeting_list'] = active_meeting_list


    return render(request, 'add_agenda.html', context)


@login_required
class AgendaView(TemplateView):

    template_name = "add_agenda.html"

    def get_context_data(self, **kwargs):
        context = super(AgendaView, self).get_context_data(**kwargs)
        context['test'] = "HI there!!"

        return context


@login_required
def view_agenda_list(request):

    context = {}
    company_id = request.session['company']
    agenda_list = Agenda.objects.filter(isActive=True, meeting_agenda__company_meeting_id=company_id)
    context['active_agenda_list'] = agenda_list


    return render(request, 'view_agenda_list.html', context)


@login_required
def agenda_detail(request, agenda_id):
    context = {}

    if request.is_ajax():

        data = {}
        vote_value = request.POST.get('vote_value')
        member_id = request.POST.get('member')
        agenda_id = request.POST.get('agenda')

        if vote_value == '1' or vote_value == '2':
            vote_obj,created = MemberVote.objects.get_or_create(vote_member_id=member_id,
                                                                vote_agenda_id=agenda_id,
                                                                defaults={
                                                                    'vote' : vote_value,
                                                                    'isActive' : True,
                                                                    'insertUser' : request.user.id,
                                                                    'insertDate' : date.today()
                                                                })

            if created:
                data['json_message'] = 'ok'
            else:
                data['json_message'] = 'no'
        else:
            data['json_message'] = 'wrong'

        return JsonResponse(data)

    try:
        agenda_obj = Agenda.objects.get(id=agenda_id)

        context['agenda_obj'] = agenda_obj
        comment_list = MemberRemarks.objects.filter(remarks_agenda=agenda_obj, isActive=True).order_by('insertDate')
        context['comment_list'] = comment_list

        try:
            member_vote_value = MemberVote.objects.get(vote_member_id=request.session['member_detail_id'], vote_agenda=agenda_obj, isActive=True)
            context['member_vote_value'] = member_vote_value
        except ObjectDoesNotExist:
            pass
    except ObjectDoesNotExist:
        message = "No Agenda"


    return render(request, 'view_agenda_detail.html', context)


@login_required
def edit_agenda(request, agenda_id):
    context = {}

    if request.method == "POST":
        try:
            agenda_obj = Agenda.objects.get(id=agenda_id)
            agenda_obj.title = request.POST['agenda_title']
            agenda_obj.full_article = request.POST['raw_html']

            agenda_obj.save()

            url = reverse('agenda_list', kwargs={'meeting_id': agenda_obj.meeting_agenda.id})
            return HttpResponseRedirect(url)

        except ObjectDoesNotExist:
            pass

        return HttpResponseRedirect(reverse('agenda:agenda_list'))




    try:
        agenda_obj = Agenda.objects.get(id=agenda_id)

        context['agenda_obj'] = agenda_obj

    except ObjectDoesNotExist:
        pass


    return render(request, 'edit_agenda.html', context)


@login_required
def add_remarks(request,member_id, agenda_id):

    account_user_id = request.session['user_detail_id']

    if request.method == "POST":
        remarks = request.POST['remarks']

        try:
            remarks_obj = MemberRemarks(remarks_member_id = member_id,
                                        remarks_agenda_id = agenda_id,
                                        comment = remarks,
                                        insertDate = datetime.today(),
                                        insertUser = request.user.id,
                                        isActive = True
                                        )

            remarks_obj.save()

        except:
            pass


    url = reverse('agenda:agenda_detail_view', kwargs={'agenda_id':agenda_id})
    return HttpResponseRedirect(url)


@login_required
def meeting_dashboard(request, meeting_id):


    if request.is_ajax():
        data = {}
        meeting_id = request.POST.get('meeting_id')
        vote_status = []
        html_string = '<table class="table table-active table-bordered" style="text-align: center;">'

        member_list = CompanyMemberDetail.objects.filter(member_company__id=request.session['company'], member_designation__designation_title='Director', isActive=True).order_by('member__name')

        html_string = html_string + '<thead style="text-align: center;"><tr><th>Agenda / B.O.D.</th>'

        for list in member_list:
            html_string = html_string + '<th>' + list.member.name + '</th>'


        html_string = html_string + '</tr></thead>'

        agenda_list = Agenda.objects.filter(meeting_agenda_id=meeting_id, isActive=True)
        count = 0

        html_string = html_string + '<tbody id="dashboard_body">'

        for agenda in agenda_list:

            html_string = html_string + '<tr>' + '<td  style="text-align: left;">' + agenda.title + '</td>'
            for member in member_list:
                try:
                    vote_value = MemberVote.objects.get(isActive=True,vote_member=member, vote_agenda=agenda)
                    if vote_value.vote == '1':
                        html_string = html_string + '<td>' + '<a href="#"><i class="fa fa-check text-navy"></i></a>' + '</td>'

                    else:
                        html_string = html_string + '<td>' + '<a href="#"><i class="fa fa-times text-danger"></i></a>' + '</td>'


                except ObjectDoesNotExist:
                    html_string = html_string + '<td>' + '</td>'


            html_string = html_string + '</tr>'

        html_string = html_string + '</tbody>'

        data['html_string'] = html_string
        print(html_string)

        return JsonResponse(data)

    context = {}
    vote_status = []
    member_list = CompanyMemberDetail.objects.filter(member_company__id=request.session['company'], member_designation__designation_title='Director', isActive=True).order_by('member__name')
    meeting_obj = Meeting.objects.filter(id=meeting_id)[0]
    agenda_list = Agenda.objects.filter(meeting_agenda_id=meeting_id, isActive=True)
    context['agenda_list'] = agenda_list
    context['meeting_obj'] = meeting_obj

    count = 0
    for agenda in agenda_list:
        vote_status.append([])
        vote_status[count].append(agenda.title)
        for member in member_list:
            try:
                vote_value = MemberVote.objects.get(isActive=True,vote_member=member, vote_agenda=agenda)
                if vote_value.vote == '1':
                    content = '<a href="#"><i class="fa fa-check text-navy"></i></a>'
                else:
                    content = '<a href="#"><i class="fa fa-times text-danger"></i></a>'
                vote_status[count].append(content)

            except ObjectDoesNotExist:
                vote_status[count].append("")

        count = count + 1




    context['member_list'] = member_list
    context['vote_status'] = vote_status

    return render(request, 'meeting_dashboard.html', context)

@login_required
def meeting_archive(request):

    context = {}
    get_ud_obj  = UserDetail.objects.get(id=request.session['user_detail_id'])
    meeting_list = Meeting.objects.filter(isActive=True, company_meeting=get_ud_obj.company_obj.member_company, start_date__lt=date.today())
    meeting_count = 0
    meeting_obj = []
    for meeting in meeting_list:
        agenda_set = []

        agenda_list = Agenda.objects.filter(isActive=True, meeting_agenda=meeting)
        for agenda in agenda_list:
            agenda_set.append(agenda)

        meeting_obj.append({'meeting_id' : meeting.id, 'title' : meeting.title, 'date' : meeting.start_date, 'description' : meeting.description, 'agenda_list' : agenda_set})

        meeting_count = meeting_count + 1

    context['meeting_list'] = meeting_list
    context['meeting_obj'] = meeting_obj

    return render(request, 'meeting_archive.html', context)


@login_required
def agenda_detail_view_mode(request, agenda_id):
    context = {}


    try:
        agenda_obj = Agenda.objects.get(id=agenda_id)

        context['agenda_obj'] = agenda_obj
        comment_list = MemberRemarks.objects.filter(remarks_agenda=agenda_obj, isActive=True).order_by('insertDate')
        context['comment_list'] = comment_list

        try:
            member_vote_value = MemberVote.objects.get(vote_member_id=request.session['member_detail_id'], vote_agenda=agenda_obj, isActive=True)
            context['member_vote_value'] = member_vote_value
        except ObjectDoesNotExist:
            pass
    except ObjectDoesNotExist:
        message = "No Agenda"


    return render(request, 'agenda_detail_view_mode.html', context)