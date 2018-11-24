import json
import pytz

from datetime import datetime

from dal import autocomplete
from django.conf import settings
from django.http import Http404
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponse
from django.views import View
from django.views.generic import FormView, TemplateView
from django.utils import timezone

from .forms import Application2018Form
from .helpers import is_valid_email_address
from .models import Airport, Draft, Application2018, Reference
from .resources import Application2018Resource, DraftResource, UserResource, Round0RatingResource, Round1RatingResource, Round2RatingResource, Application2018FullResource, DraftFullResource, UserFullResource, Round0RatingFullResource, Round1RatingFullResource, Round2RatingFullResource
from . import constants


# todo: find better solution for prefilling fields!
def post_to_json(post):
    dictionary = {}
    for key in post.keys():
        data = post.getlist(key)
        dictionary[key] = data
    return json.dumps(dictionary)


from .models import MULTIFIELD_NAMES
def load_json_to_initial(data):
    # #todo -- #annualcheck -- check these fields if they are in sync with Application2018
    # see forms.py -- add all of the following: OptionalChoiceField, OptionalMultiChoiceField
    # Year 2016: MULTIFIELD_NAMES += ['skills_0', 'gender_0', 'how_did_you_find_out_0', ]
    # Year 2017 (2018): MULTIFIELD_NAMES += ['gender_0', 'ethnicity_0', ]
    global MULTIFIELD_NAMES
    MULTIFIELD_NAMES += ['gender_0', 'ethnicity_0', ]
    for key in data.keys():
        if key not in MULTIFIELD_NAMES:
            data[key] = data[key][0]

    # handle OptionalChoiceField items:
    # gender_0[0] can be None, so including this in try-except because None cannot be indexed
    try:
        gender_0 = data.get('gender_0', '')[0]
    except:
        gender_0 = ''

    try:
        gender_1 = data.get('gender_1', '')
    except:
        gender_1 = ''

    data['gender'] = [gender_0, gender_1]

    # handle OptionalMultiChoiceField items:
    data['ethnicity'] = [data.get('ethnicity_0', ''), data.get('ethnicity_1', '')]

    return data


class ApplicationView2018(FormView):
    """View shows the application itself"""
    form_class = Application2018Form
    template_name = 'application/application_form-2018.html'

    def get_referral(self, referral=None):
        if referral is None or not Reference.objects.filter(key=referral).exists():
            return {}
        reference = Reference.objects.get(key=referral)
        return {
            'image': reference.image,
            'image_url': reference.image_url,
            'name': reference.name,
            'text': reference.text,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'action_url': self.request.get_full_path(),
            'organization': self.get_referral(self.kwargs.get('referral')),
        })
        return context

    def get_success_url(self):
        """Get the success url with the right primary key so a customized thank you message can be shown"""
        application_pk = self.application.pk
        return reverse('application:thank_you', kwargs={'pk': application_pk})

    def remove_form_errors(self, form):
        """Removes the errors from the form except for email and acknowledgment which is required for draft as well"""
        for field in form:
            if field.name in ['email', 'acknowledgments']:
                continue
            form.errors[field.name] = form.error_class()
        return form

    def save_draft(self, form):
        """
        Tries to save the draft. Checks whether the email and acknowledgment is valid.
        Returns the whether the draft was saved, the form itself and the the draft if it was created.
        """
        form = self.remove_form_errors(form)

        email = form.data['email']
        acknowledgments = form.data.getlist('acknowledgments')

        # #todo -- #annualcheck -- check length of acknowledgments (or check in models.py programmatically)
        if is_valid_email_address(email) and len(acknowledgments) == 4:
            draft, created = Draft.objects.get_or_create(email=email)
            if created:
                draft.data = post_to_json(self.request.POST)
                draft.save()
                return True, form, draft

            form.add_error('email', 'A draft application associated with your e-mail address has '
                           'already been saved on our servers. If you cannot access it, contact us. ')
        return False, form, None

    def is_after_deadline(self):
        deadline_unaware = datetime.strptime(constants.APPLICATION_DEADLINE, '%Y/%m/%d %H:%M')
        deadline = pytz.utc.localize(deadline_unaware)

        referral = self.kwargs.get('referral', '')

        try:
            reference = Reference.objects.get(key=referral)
            if reference.deadline:
                deadline = reference.deadline
        except Reference.DoesNotExist:
            pass

        return timezone.now() > deadline

    def form_invalid(self, form):
        """
        Handles the form when it's invalid. For save,
        it tries to save a draft for submit it invokes super().form_invalid()
        """
        if '_save' in self.request.POST:
            valid, form, draft = self.save_draft(form)
            if valid:
                Draft.send_access(draft) # send e-mail with link
                return render(self.request, 'application/form_saved.html', {'draft': draft})
        return super().form_invalid(form)

    def form_valid(self, form):
        """
        If the form was saved, it saves a draft and renders a info message.
        If the form was submitted, it saves it and set a inactive flag for draft.
        """
        if '_save' in self.request.POST:
            _, _, draft = self.save_draft(form)
            Draft.send_access(draft) # send e-mail with link
            return render(self.request, 'application/form_saved.html', {'draft': draft})
        elif '_submit':
            self.application = form.save()
            email = form.data['email']
            if Draft.objects.filter(email=email).exists():
                draft = Draft.objects.get(email=email)
                draft.inactive = True
                draft.save()
            return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        # admins can see the application form even after the deadline
        if self.is_after_deadline() and not request.user.is_superuser:
            return redirect(settings.REDIRECT_URL)

        return super().dispatch(request, *args, **kwargs)


'''
class ApplicationView(FormView):
    """View shows the application itself"""
    form_class = ApplicationForm
    template_name = 'application/application_form.html'

    """
    def get_referral(self, referral=None):
        if referral is None or not Reference.objects.filter(key=referral).exists():
            return {}
        reference = Reference.objects.get(key=referral)
        return {
            'image': reference.image,
            'name': reference.name,
            'text': reference.text,
        }
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'action_url': self.request.get_full_path(),
            'organization': self.get_referral(self.kwargs.get('referral')),
        })
        return context

    def get_success_url(self):
        """Get the success url with the right primary key so a customized thank you message can be shown"""
        application_pk = self.application.pk
        return reverse('application:thank_you', kwargs={'pk': application_pk})

    def remove_form_errors(self, form):
        """Removes the errors from the form except for email and acknowledgment which is required for draft as well"""
        for field in form:
            if field.name in ['email', 'acknowledgments']:
                continue
            form.errors[field.name] = form.error_class()
        return form

    def save_draft(self, form):
        """
        Tries to save the draft. Checks whether the email and acknowledgment is valid.
        Returns the whether the draft was saved, the form itself and the the draft if it was created.
        """
        form = self.remove_form_errors(form)

        email = form.data['email']
        acknowledgments = form.data.getlist('acknowledgments')

        if is_valid_email_address(email) and len(acknowledgments) == 4:
            draft, created = Draft.objects.get_or_create(email=email)
            if created:
                draft.data = post_to_json(self.request.POST)
                draft.save()
                return True, form, draft

            form.add_error('email', 'An draft application associated with your e-mail address has '
                           'already been saved on our servers. If you cannot access it, contact us. ')
        return False, form, None

    def is_after_deadline(self):
        deadline_unaware = datetime.strptime(constants.APPLICATION_DEADLINE, '%Y/%m/%d %H:%M')
        deadline = pytz.utc.localize(deadline_unaware)

        """
        referral = self.kwargs.get('referral', '')

        try:
            reference = Reference.objects.get(key=referral)
            if reference.deadline:
                deadline = reference.deadline
        except Reference.DoesNotExist:
            pass
        """

        return timezone.now() > deadline

    def form_invalid(self, form):
        """
        Handles the form when it's invalid. For save,
        it tries to save a draft for submit it invokes super().form_invalid()
        """
        if '_save' in self.request.POST:
            valid, form, draft = self.save_draft(form)
            if valid:
                return render(self.request, 'application/form_saved.html', {'draft': draft})
        return super().form_invalid(form)

    def form_valid(self, form):
        """
        If the form was saved, it saves a draft and renders a info message.
        If the form was submitted, it saves it and set a inactive flag for draft.
        """
        if '_save' in self.request.POST:
            _, _, draft = self.save_draft(form)
            return render(self.request, 'application/form_saved.html', {'draft': draft})
        elif '_submit':
            self.application = form.save()
            email = form.data['email']
            if Draft.objects.filter(email=email).exists():
                draft = Draft.objects.get(email=email)
                draft.inactive = True
                draft.save()
            return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if self.is_after_deadline():
            return redirect(settings.REDIRECT_URL)

        return super().dispatch(request, *args, **kwargs)
'''

class PreFilledApplicationView(ApplicationView2018):
    """View for handling the application with prefilled data from draft"""
    def get_draft(self):
        """Gets the draft based on uuid and raises a 404 if the draft does not exists"""
        try:
            draft_uuid = self.kwargs.get('uuid')
            draft = Draft.all_objects.get(uuid=draft_uuid)
            return draft
        except (ValueError, Draft.DoesNotExist):
            raise Http404

    def save_draft(self, form):
        """Saves the draft and makes sure the email wasn't changed"""
        form = self.remove_form_errors(form)
        draft_uuid = self.kwargs.get('uuid')
        draft = Draft.objects.get(uuid=draft_uuid)

        # Do not change email doesn't matter what
        mutable = self.request.POST._mutable
        self.request.POST._mutable = True
        self.request.POST['email'] = draft.email
        self.request.POST._mutable = mutable
        draft.data = post_to_json(self.request.POST)
        draft.save()
        return True, form, draft

    def get_initial(self):
        """Loads the initial data from draft"""
        draft = self.get_draft()
        draft_data = json.loads(draft.data)
        return load_json_to_initial(draft_data)

    def get(self, request, uuid, *args, **kwargs):
        draft = self.get_draft()
        if draft.inactive:
            return render(self.request, 'application/already_submitted.html', {})
        return super().get(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        data = json.loads(self.get_draft().data)
        referral = data.get('referred_by', [''])[0]
        self.kwargs['referral'] = referral
        return super().dispatch(request, *args, **kwargs)


class ReferralApplicationView(ApplicationView2018):
    """View shows the application with referral code"""
    def get_initial(self):
        referral = self.kwargs.get('referral')
        return {'referred_by': referral}


def check_status_private(request):
    context = {}
    email = request.GET.get('email', None)
    if Application2018.objects.filter(email=email).exists():
        context.update({'application': Application2018.objects.get(email=email)})
    elif Draft.objects.filter(email=email).exists():
        context.update({'draft': Draft.objects.get(email=email)})
    return render(request, 'application/status.html', context)


def check_status(request):
    return render(request, 'application/already_submitted.html', {})
    # #todo -- update this view
    pass

def check_email(request, email):
    if Application2018.objects.filter(email=email).exists():
        context = {}
        return render(request, 'application/popup_already_submitted.html', context)

    if Draft.objects.filter(email=email).exists():
        context = {'draft': Draft.objects.get(email=email)}
        return render(request, 'application/popup_saved_draft.html', context)

    context = {}
    return render(request, 'application/popup_alright.html', context)


def send_email(request, email):
    draft = get_object_or_404(Draft, email=email)
    status = draft.send_access()
    if status:
        template_name = 'application/access_sent.html'
    else:
        template_name = 'application/access_not_sent.html'
    return render(request, template_name, {})


class AirportAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Airport.objects.all()
        if self.q:
            qs = qs.filter(Q(name__icontains=self.q) | Q(iata_code__istartswith=self.q))
        return qs


class InstitutionAutocomplete(autocomplete.Select2QuerySetView):
    def has_add_permission(self, request):
        return True

    def get_queryset(self):
        qs = Institution.objects.filter(show=True)
        if self.q:
            qs = qs.filter(Q(name__icontains=self.q))
        return qs


class OrganizationAutocomplete(autocomplete.Select2QuerySetView):
    def has_add_permission(self, request):
        return True

    def get_queryset(self):
        qs = Organization.objects.filter(show=True)
        if self.q:
            qs = qs.filter(Q(name__icontains=self.q))
        return qs


class CountryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Country.objects.all()
        if self.q:
            qs = qs.filter(Q(name__icontains=self.q))
        return qs


class ThankYou(TemplateView):
    template_name = 'application/thank_you.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'application': self.application})
        return context

    def get(self, request, pk, *args, **kwargs):
        self.application = get_object_or_404(Application2018, pk=pk)
        return redirect('http://www.opencon2018.org/thank_you?referral=' + str(self.application.my_referral))
        # return super().get(request, *args, **kwargs)

# --- export of selected fields (for google docs / spreadsheet) ---

class Application2018ExportView(View):

    def get(self, request, *args, **kwargs ):
        dataset = Application2018Resource().export()
        response = HttpResponse(dataset.csv, content_type='csv')
        response['Content-Disposition'] = 'attachment; filename=opencon_applications_2018.csv'
        return response

class DraftExportView(View):

    def get(self, request, *args, **kwargs ):
        dataset = DraftResource().export()
        response = HttpResponse(dataset.csv, content_type='csv')
        response['Content-Disposition'] = 'attachment; filename=opencon_drafts.csv'
        return response

class UserExportView(View):

    def get(self, request, *args, **kwargs ):
        dataset = UserResource().export()
        response = HttpResponse(dataset.csv, content_type='csv')
        response['Content-Disposition'] = 'attachment; filename=opencon_users.csv'
        return response

class Round0RatingExportView(View):

    def get(self, request, *args, **kwargs ):
        dataset = Round0RatingResource().export()
        response = HttpResponse(dataset.csv, content_type='csv')
        response['Content-Disposition'] = 'attachment; filename=opencon_round0ratings.csv'
        return response

class Round1RatingExportView(View):

    def get(self, request, *args, **kwargs ):
        dataset = Round1RatingResource().export()
        response = HttpResponse(dataset.csv, content_type='csv')
        response['Content-Disposition'] = 'attachment; filename=opencon_round1ratings.csv'
        return response

class Round2RatingExportView(View):

    def get(self, request, *args, **kwargs ):
        dataset = Round2RatingResource().export()
        response = HttpResponse(dataset.csv, content_type='csv')
        response['Content-Disposition'] = 'attachment; filename=opencon_round2ratings.csv'
        return response

# --- export of full tables (all fields) ---

class Application2018ExportFullView(View):

    def get(self, request, *args, **kwargs ):
        dataset = Application2018FullResource().export()
        response = HttpResponse(dataset.csv, content_type='csv')
        response['Content-Disposition'] = 'attachment; filename=opencon_applications_full.csv'
        return response

class DraftExportFullView(View):

    def get(self, request, *args, **kwargs ):
        dataset = DraftFullResource().export()
        response = HttpResponse(dataset.csv, content_type='csv')
        response['Content-Disposition'] = 'attachment; filename=opencon_drafts_full.csv'
        return response

class UserExportFullView(View):

    def get(self, request, *args, **kwargs ):
        dataset = UserFullResource().export()
        response = HttpResponse(dataset.csv, content_type='csv')
        response['Content-Disposition'] = 'attachment; filename=opencon_users_full.csv'
        return response

class Round0RatingExportFullView(View):

    def get(self, request, *args, **kwargs ):
        dataset = Round0RatingFullResource().export()
        response = HttpResponse(dataset.csv, content_type='csv')
        response['Content-Disposition'] = 'attachment; filename=opencon_round0ratings_full.csv'
        return response

class Round1RatingExportFullView(View):

    def get(self, request, *args, **kwargs ):
        dataset = Round1RatingFullResource().export()
        response = HttpResponse(dataset.csv, content_type='csv')
        response['Content-Disposition'] = 'attachment; filename=opencon_round1ratings_full.csv'
        return response

class Round2RatingExportFullView(View):

    def get(self, request, *args, **kwargs ):
        dataset = Round2RatingFullResource().export()
        response = HttpResponse(dataset.csv, content_type='csv')
        response['Content-Disposition'] = 'attachment; filename=opencon_round2ratings_full.csv'
        return response
