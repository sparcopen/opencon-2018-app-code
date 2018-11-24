from django import forms
from opencon.application.models import Application2018

import django_filters

from django.db.utils import ProgrammingError

class Round1NeedsReviewFilter(django_filters.FilterSet):
    # 2018-05-31`15:46:35 -- we have to use try-except -- if we don't, this code will crash during initial migration (`django_1 | django.db.utils.ProgrammingError: relation "application_application2018" does not exist`) -- "Application2018.objects" cannot be accessed before the database table is created...
    try:
        area_of_interest = django_filters.MultipleChoiceFilter(
            name='area_of_interest',
            label='Area of Interest',
            # choices=Application2018.AREA_OF_INTEREST_CHOICES,
            choices = [(i, dict(Application2018.AREA_OF_INTEREST_CHOICES).get(i)) for i in Application2018.objects.filter(need_rating1=True).values_list('area_of_interest', flat=True).order_by('area_of_interest').distinct()],
            widget=forms.CheckboxSelectMultiple,
        )

        field = django_filters.MultipleChoiceFilter(
            name='field',
            label='Field of Study',
            # choices=Application2018.FIELD_CHOICES,
            choices = [(i, dict(Application2018.FIELD_CHOICES).get(i)) for i in Application2018.objects.filter(need_rating1=True).values_list('field', flat=True).order_by('field').distinct()],
            widget=forms.CheckboxSelectMultiple,
        )

        citizenship = django_filters.MultipleChoiceFilter(
            name='citizenship',
            label='Citizenship of Applicant',
            # choices=Application2018.COUNTRY_CHOICES,
            choices = [(i, dict(Application2018.COUNTRY_CHOICES).get(i)) for i in Application2018.objects.filter(need_rating1=True).values_list('citizenship', flat=True).order_by('citizenship').distinct()],
            widget=forms.CheckboxSelectMultiple,
        )
    except ProgrammingError:
        pass
