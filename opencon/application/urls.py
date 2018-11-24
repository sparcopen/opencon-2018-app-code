from django.conf import settings
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.generic.base import RedirectView
from . import views
# from .models import Institution, Organization
from .views import Application2018ExportView, DraftExportView, UserExportView, Round1RatingExportView, Round1RatingExportView, Round2RatingExportView

from config.settings.base import DOWNLOAD_SECRET as authsecret

urlpatterns = [
    # #todo -- instead of hard-coded `url='/apply/'` use a reference to the view name (reverse_lazy?) -- `pattern_name='application-2018'`
    url(r'^$',       RedirectView.as_view(url='/apply/', permanent=False), name='root'),
    url(r'^apply/$', RedirectView.as_view(url='/apply-2018/', permanent=False), name='application-root'),
    # url(r'^apply-2016/$', views.ApplicationView.as_view(), name='application-2016'),
    url(r'^apply-2018/$', views.ApplicationView2018.as_view(), name='application-2018'),
    url(r'^checkstatus/$', RedirectView.as_view(url='/check_status/', permanent=False), name='check_status_redirect'),
    url(r'^check_status/$', views.check_status, name='check_status'),
    url(r'^check_status_private/$', login_required(views.check_status_private), name='check_status_private'),
    url(r'^check_email/(?P<email>[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)$',
        views.check_email, name='check_email'),
    url(r'^send_email/(?P<email>[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)$',
        views.send_email, name='send_email'),
    url(r'^airport-autocomplete/$', views.AirportAutocomplete.as_view(), name='airport-autocomplete'),
    # url(r'^country-autocomplete/$', views.CountryAutocomplete.as_view(), name='country-autocomplete'),
    # url(r'^institution-autocomplete/$',
    #     views.InstitutionAutocomplete.as_view(
    #         model=Institution,
    #         create_field='name',
    #     ),
    #     name='institution-autocomplete'),
    # url(r'^organization-autocomplete/$',
    #     views.OrganizationAutocomplete.as_view(
    #         model=Organization,
    #         create_field='name',
    #     ),
    #     name='organization-autocomplete'),
    url(r'^referral/(?P<referral>\w{1,' + str(settings.MAX_CUSTOM_REFERRAL_LENGTH) + '})$',
        views.ReferralApplicationView.as_view(), name='referral'),
    url(r'^saved/(?P<uuid>[^/]+)/$', views.PreFilledApplicationView.as_view(), name='access_draft'),
    url(r'^thank-you/(?P<pk>[0-9a-f-]+)', views.ThankYou.as_view(), name='thank_you'),

    # for regular download URLs: use login_required
    url(r'^export/applications/$', login_required(views.Application2018ExportView.as_view()), name='export_apps_2018'),
    url(r'^export/drafts/$', login_required(views.DraftExportView.as_view()), name='export_drafts'),
    url(r'^export/users/$', login_required(views.UserExportView.as_view()), name='export_users'),
    url(r'^export/round0ratings/$', login_required(views.Round0RatingExportView.as_view()), name='export_round0ratings'),
    url(r'^export/round1ratings/$', login_required(views.Round1RatingExportView.as_view()), name='export_round1ratings'),
    url(r'^export/round2ratings/$', login_required(views.Round2RatingExportView.as_view()), name='export_round2ratings'),

    url(r'^export/applications-full/$', login_required(views.Application2018ExportFullView.as_view()), name='export_apps_2018_full'),
    url(r'^export/drafts-full/$', login_required(views.DraftExportFullView.as_view()), name='export_drafts_full'),
    url(r'^export/users-full/$', login_required(views.UserExportFullView.as_view()), name='export_users_full'),
    url(r'^export/round0ratings-full/$', login_required(views.Round0RatingExportFullView.as_view()), name='export_round0ratings_full'),
    url(r'^export/round1ratings-full/$', login_required(views.Round1RatingExportFullView.as_view()), name='export_round1ratings_full'),
    url(r'^export/round2ratings-full/$', login_required(views.Round2RatingExportFullView.as_view()), name='export_round2ratings_full'),

    # for secret link download URLs: no login_required
    url(r'^export/' + authsecret + '/applications/$', views.Application2018ExportView.as_view(), name='export_apps_2018_secretlink'),
    url(r'^export/' + authsecret + '/drafts/$', views.DraftExportView.as_view(), name='export_drafts_secretlink'),
    url(r'^export/' + authsecret + '/users/$', views.UserExportView.as_view(), name='export_users_secretlink'),
    url(r'^export/' + authsecret + '/round0ratings/$', views.Round0RatingExportView.as_view(), name='export_round0ratings_secretlink'),
    url(r'^export/' + authsecret + '/round1ratings/$', views.Round1RatingExportView.as_view(), name='export_round1ratings_secretlink'),
    url(r'^export/' + authsecret + '/round2ratings/$', views.Round2RatingExportView.as_view(), name='export_round2ratings_secretlink'),

    url(r'^export/' + authsecret + '/applications-full/$', views.Application2018ExportFullView.as_view(), name='export_apps_2018_secretlink_full'),
    url(r'^export/' + authsecret + '/drafts-full/$', views.DraftExportFullView.as_view(), name='export_drafts_secretlink_full'),
    url(r'^export/' + authsecret + '/users-full/$', views.UserExportFullView.as_view(), name='export_users_secretlink_full'),
    url(r'^export/' + authsecret + '/round0ratings-full/$', views.Round0RatingExportFullView.as_view(), name='export_round0ratings_secretlink_full'),
    url(r'^export/' + authsecret + '/round1ratings-full/$', views.Round1RatingExportFullView.as_view(), name='export_round1ratings_secretlink_full'),
    url(r'^export/' + authsecret + '/round2ratings-full/$', views.Round2RatingExportFullView.as_view(), name='export_round2ratings_secretlink_full'),
]
