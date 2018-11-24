from django import forms
from .models import Application2018, Airport
from .forms_field_other import OptionalChoiceField, OptionalMultiChoiceField

from django.core.validators import ValidationError
from django.forms.widgets import CheckboxSelectMultiple, HiddenInput, RadioSelect, Select, TextInput, Textarea

from dal import autocomplete
import ast
from .data import *
from .models import STATUS_CHOICES


class Application2018Form(forms.ModelForm):

    use_required_attribute = False # Django 1.10+ renders "required" HTML attribute, which needs to be disabled, otherwise we won't be able to save drafts without first filling out all required fields -- see https://docs.djangoproject.com/en/dev/releases/1.10/

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '') # do not append colon to the widget labels
        if kwargs.get('instance'):
            kwargs['initial'] = {
                # these are the fields which use CheckboxSelectMultiple widget
                'events': ast.literal_eval(kwargs.get('instance').events or '[]'),
                'profession': ast.literal_eval(kwargs.get('instance').profession or '[]'),
                'degrees': ast.literal_eval(kwargs.get('instance').degrees or '[]'),
                'skills': ast.literal_eval(kwargs.get('instance').skills or '[]'),
                'expenses': ast.literal_eval(kwargs.get('instance').expenses or '[]'),
                'permissions': ast.literal_eval(kwargs.get('instance').permissions or '[]'),
                'acknowledgments': ast.literal_eval(kwargs.get('instance').acknowledgments or '[]'),
            }

        # # careful about hardcoding values for "self.initial", we could end up with hardcoded values everywhere
        # self.initial['partners'] = ast.literal_eval(self.initial.get('partners', '[]'))

        super().__init__(*args, **kwargs)

        self.fields['gender'] = OptionalChoiceField(
            label=Application2018.GENDER_VERBOSE_NAME,
            help_text=Application2018.GENDER_HELP_TEXT,
            choices=Application2018.GENDER_CHOICES,
        )

        self.fields['ethnicity'] = OptionalMultiChoiceField(
            choices=Application2018.ETHNICITY_CHOICES,
            label=Application2018.ETHNICITY_VERBOSE_NAME,
            help_text=Application2018.ETHNICITY_HELP_TEXT,
        )

        self.fields['airport'] = forms.ModelChoiceField(
            queryset=Airport.objects.all(),
            widget=autocomplete.ModelSelect2(url='application:airport-autocomplete'),
            label=Application2018.AIRPORT_VERBOSE_NAME,
            help_text=Application2018.AIRPORT_HELP_TEXT,
        )


    class Meta:
        model = Application2018
        fields = (
            'email',
            'type',
            'first_name',
            'last_name',
            'nickname',
            'alternate_email',
            'twitter_username',
            'orcid',
            'affiliation_1',
            'affiliation_2',
            'affiliation_3',
            'affiliation_4',
            'affiliation_5',
            'bio',
            'essay_interest',
            'essay_ideas',
            'events',
            'events_detail',
            'area_of_interest',
            'citizenship',
            'residence',
            'profession',
            'experience',
            'degrees',
            'field',
            'gender',
            'age',
            'ethnicity',
            'language_1',
            'language_2',
            'language_3',
            'language_4',
            'skills',
            'expenses',
            'fundraising_potential',
            'scholarship_comments',
            'location',
            'airport',
            'comments',
            'referred_by',
            'attended',
            'engagement',
            'permissions',
            'acknowledgments',
        )

        # "HiddenInput" removed -- we are rendering
        # 'referred_by': HiddenInput,
        # 'attended': HiddenInput,
        # 'engagement': HiddenInput,

        widgets = {
            'attended': Textarea(attrs={'rows': 2, 'cols': 80,}),
            'engagement': Textarea(attrs={'rows': 2, 'cols': 80,}),
            'type': RadioSelect(choices=Application2018.TYPE_CHOICES),
            'events': CheckboxSelectMultiple(choices=Application2018.EVENTS_CHOICES),
            'area_of_interest': RadioSelect(choices=Application2018.AREA_OF_INTEREST_CHOICES),
            'citizenship': Select(choices=Application2018.COUNTRY_CHOICES),
            'residence': Select(choices=Application2018.COUNTRY_CHOICES),
            'profession': CheckboxSelectMultiple(choices=Application2018.PROFESSION_CHOICES),
            'experience': RadioSelect(choices=Application2018.EXPERIENCE_CHOICES),
            'degrees': CheckboxSelectMultiple(choices=Application2018.DEGREES_CHOICES),
            'field': Select(choices=Application2018.FIELD_CHOICES),
            'age': RadioSelect(choices=Application2018.AGE_CHOICES),
            'language_1': Select(choices=Application2018.LANGUAGE_CHOICES),
            'language_2': Select(choices=Application2018.LANGUAGE_CHOICES),
            'language_3': Select(choices=Application2018.LANGUAGE_CHOICES),
            'language_4': Select(choices=Application2018.LANGUAGE_CHOICES),
            'skills': CheckboxSelectMultiple(choices=Application2018.SKILLS_CHOICES),
            'expenses': CheckboxSelectMultiple(choices=Application2018.EXPENSES_CHOICES),
            'fundraising_potential': RadioSelect(choices=Application2018.FUNDRAISING_POTENTIAL_CHOICES),
            'permissions': CheckboxSelectMultiple(choices=Application2018.PERMISSIONS_CHOICES), # to check all choices: `attrs={'checked' : True}`
            'acknowledgments': CheckboxSelectMultiple(choices=Application2018.ACKNOWLEDGMENTS_CHOICES),
        }

    def clean_orcid(self):
        o = self.cleaned_data['orcid'].replace('-', '')
        if o:
            # add dashes in proper places
            o = '-'.join([o[:4], o[4:8], o[8:12], o[12:16]])
        return o

    def clean(self):
        cleaned_data = super().clean()

        errors = {}

        # Q27 (expenses) -- Q28 (fundraising_potential) -- Q30 (location) -- Q31 (airport) -- Validation: Required if scholarship requested (type=invite_scholarship).
        if cleaned_data.get('type') == 'invite_scholarship':
            msg = 'This field is required when scholarship is requested (see "Application Type" question).'
            if not cleaned_data.get('expenses'): errors.update({'expenses': msg})
            if not cleaned_data.get('fundraising_potential'): errors.update({'fundraising_potential': msg})
            if not cleaned_data.get('location'): errors.update({'location': msg})
            if not cleaned_data.get('airport'): errors.update({'airport': msg})

        if cleaned_data.get('events') == 'none' and cleaned_data.get('events_detail'):
                errors.update({'events_detail': 'This must be blank if None of the Above was selected in previous question'})

        try:
            ethnicity_0 = cleaned_data.get('ethnicity', [])[0]
        except:
            ethnicity_0 = []
        try:
            ethnicity_1 = cleaned_data.get('ethnicity', '')[1]
        except:
            ethnicity_1 = ''
        try:
            if ethnicity_0 == []:
                errors.update({'ethnicity': 'Please select “Prefer not to say” if you wish to leave this question blank, or provide an answer.'})
            if len(ethnicity_0)>1 and 'not_specified' in ethnicity_0:
                errors.update({'ethnicity': 'You cannot choose both "Prefer not to say" and another option.'})
            if 'other' in ethnicity_0 and ethnicity_1 == '':
                errors.update({'ethnicity': 'If you choose "Specified below", you must specify ethnicity in the text box'})
        except:
            errors.update({'ethnicity': 'Please make a selection.'}) # This is triggered when nothing is filled out (but potentially even at other times?).

        if errors:
            raise ValidationError(errors)

        return cleaned_data

"""
class ApplicationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            kwargs['initial'] = {
                'occupation': ast.literal_eval(kwargs.get('instance').occupation or '[]'),
                'degree': ast.literal_eval(kwargs.get('instance').degree or '[]'),
                'participation': ast.literal_eval(kwargs.get('instance').participation or '[]'),
                'expenses': ast.literal_eval(kwargs.get('instance').expenses or '[]'),
                'opt_outs': ast.literal_eval(kwargs.get('instance').opt_outs or '[]'),
                'acknowledgements': ast.literal_eval(kwargs.get('instance').acknowledgements or '[]'),
            }

        super().__init__(*args, **kwargs)

        self.fields['gender'] = OptionalChoiceField(
            label='Gender^',
            choices=GENDER_CHOICES,
        )

        self.fields['skills'] = OptionalMultiChoiceField(
            choices=SKILLS_CHOICES,
            label='Do you have any of the following skills?^',
            help_text='Check all that apply.',
        )

        self.fields['how_did_you_find_out'] = OptionalMultiChoiceField(
            choices=HOW_DID_YOU_FIND_OUT_CHOICES,
            label='How did you find out about OpenCon 2016?^',
            help_text='Check all that apply.',
        )

        self.fields['airport'] = forms.ModelChoiceField(
            queryset=Airport.objects.all(),
            widget=autocomplete.ModelSelect2(url='application:airport-autocomplete'),
            label='Closest international airport to the city you indicated in the previous question.',
            help_text='This question helps us understand how for you would need to travel. Begin by '
                      'typing the name of the city and suggestions will show up. Click the correct one. '
                      'You can also search by the three-letter IATA code (for example “LHR” for London). '
                      'If your airport does not show up, please type “Other Airport” and specify your '
                      'airport in the comments box below. Please enter an airport regardless of how close '
                      'you are located to Washington, DC, and note that U.S. regional/national airports '
                      'are permitted.',
        )
        self.fields['institution'] = forms.ModelChoiceField(
            queryset=Institution.objects.all(),
            widget=autocomplete.ModelSelect2(url='application:institution-autocomplete'),
            label='Primary Institution / Employer / Affiliation',
            help_text='Begin by typing the full name (no abbreviations) of the primary institution or '
                      'organization where you work or go to school. A list of suggestions will show up '
                      'as you type. If the correct name appears, click to select. If it does not appear, '
                      'finish typing the full name and click the option to “Create” the name. You may need '
                      'to scroll down to find this option.',
        )
        self.fields['organization'] = forms.ModelChoiceField(
            queryset=Organization.objects.all(),
            widget=autocomplete.ModelSelect2(url='application:organization-autocomplete'),
            label='Other Primary Affiliation / Organization / Project (Optional)',
            help_text='If you have another primary affiliation or project, you may list it here. Similar to the '
                      'question above, begin by typing the full name. If the correct name shows up automatically, '
                      'click to select. If not, then finish typing and click “Create.” If you have multiple other '
                      'affiliations, list only the most important one here. You may list any additional '
                      'affiliations in the Comments Box at the end of the application.',
            required=False,
        )


    class Meta:
        model = Application
        fields = (
            'email',
            'first_name',
            'last_name',
            'nickname',
            'alternate_email',
            'twitter_username',
            'institution',
            'organization',
            'area_of_interest',
            'description',
            'interested',
            'goal',
            'participation',
            'participation_text',
            'citizenship',
            'residence',
            'gender',
            'occupation',
            'degree',
            'experience',
            'fields_of_study',
            # 'ideas',
            'skills',
            'how_did_you_find_out',
            # 'visa_requirements',
            'scholarship',
            'expenses',
            'location',
            'airport',
            'additional_info',
            'opt_outs',
            'acknowledgements',
            'referred_by',
        )
        widgets = {
            'referred_by': HiddenInput,
            'occupation': CheckboxSelectMultiple(choices=OCCUPATION_CHOICES),
            'experience': RadioSelect(choices=EXPERIENCE_CHOICES),
            'citizenship': Select(choices=COUNTRY_CHOICES),
            'residence': Select(choices=COUNTRY_CHOICES),
            'fields_of_study': Select(choices=FIELDS_OF_STUDY_CHOICES),
            'degree': CheckboxSelectMultiple(choices=DEGREE_CHOICES),
            'area_of_interest': RadioSelect(choices=AREA_OF_INTEREST_CHOICES),
            'participation': CheckboxSelectMultiple(choices=PARTICIPATION_CHOICES),
            # 'visa_requirements': RadioSelect(choices=VISA_CHOICES),
            'expenses': CheckboxSelectMultiple(choices=EXPENSES_CHOICES),
            'scholarship': RadioSelect,
            'opt_outs': CheckboxSelectMultiple(choices=OPT_OUTS_CHOICES),
            'acknowledgements': CheckboxSelectMultiple(choices=ACKNOWLEDGEMENT_CHOICES),
        }
"""

class ChangeStatusAdminForm(forms.ModelForm):
    class Meta:
        model = Application2018
        fields = ('status', 'status_reason')
        widgets = {
            'status': Select(choices=STATUS_CHOICES),
        }
