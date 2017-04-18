from django.conf.urls import include, url
from django.contrib import admin
from DMS import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # Examples:
    # url(r'^$', 'DMS.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^DMS/$', views.login_page, name="login"),
    url(r'^agenda/', include('agenda.urls', namespace="agenda")),
    url(r'^home/$', views.meeting_list, name="start"),
    url(r'^article/$', views.article_page, name="article"),
    url(r'^dashboard/$', views.dashboard_page, name="dashboard"),
    url(r'^company/', include('company.urls', namespace="company")),
    url(r'^account/', include('account.urls', namespace="account")),
    url(r'^login_authentication/$', views.login, name='dms_login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^meeting/$', views.meeting_list, name="meeting_list"),
    url(r'^(?P<meeting_id>[0-9]+)/agenda_list/$', views.start_page, name="agenda_list"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
