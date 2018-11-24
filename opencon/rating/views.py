from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.db.models import Count
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView, ListView

from django_filters.views import FilterView
from .filters import Round1NeedsReviewFilter

# #todo -- #annualcheck -- import the correct model
from opencon.application.models import Application2018

from .forms import Round0RateForm, Round1RateForm, Round2RateForm, ChangeStatusForm
from .models import User, Round0Rating, Round1Rating, Round2Rating

from abc import ABC, abstractproperty, abstractmethod

from opencon.application.models import DISPLAYED_FIELDS_ROUND_0, DISPLAYED_FIELDS_ROUND_1, DISPLAYED_FIELDS_ROUND_2

import ast
import operator  # custom sorting in django using a computed key


class AuthenticatedMixin(View, ABC):

    @abstractproperty
    def permission(self):
        pass

    def get(self, request, *args, **kwargs):
        if self.permission is None:
            raise AssertionError('Permission level was not set.')
        self.get_user(request)  # is logged in?
        return super().get(request, *args, **kwargs)

    def get_user(self, request=None):
        if request is not None:
            user_pk = request.session.get('user_pk')
            self.user = get_object_or_404(User, pk=user_pk, disabled_at=None)

        if not hasattr(self, 'user'):
            raise AssertionError(
                'You are trying to get the user but you have to invoke this function with request first.'
            )

        if self.permission == 0 and self.user.is_round_0_reviewer:
            return self.user
        elif self.permission == 1 and self.user.is_round_1_reviewer:
            return self.user
        elif self.permission == 2 and self.user.is_round_2_reviewer:
            return self.user
        elif self.permission == -1 and self.user: # any logged in user can access this view
            return self.user
        raise Http404

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'user': self.user})
        return context


class Login(View):
    def get(self, request, uuid):
        user = get_object_or_404(User, uuid=uuid)
        request.session['user_pk'] = user.pk
        if user.is_round_0_reviewer:
            return redirect('rating:rate_round0')
        elif user.is_round_1_reviewer:
            return redirect('rating:rate_round1')
        elif user.is_round_2_reviewer:
            return redirect('rating:rate_round2')
        raise Http404


class Logout(View):
    def get(self, request):
        del request.session['user_pk']
        return redirect('rating:logged_out')


class AbstractRateView(AuthenticatedMixin, View, ABC):
    displayed_data = DISPLAYED_FIELDS_ROUND_1

    @abstractproperty
    def rate_form_class(self):
        pass

    @abstractproperty
    def skip_url(self):
        pass

    @abstractmethod
    def rate(self, request, user, rating_pk):
        pass

    @abstractmethod
    def get(self, request, rating_pk=None):
        pass

    def get_context_data(self, created_by, application, rate_form=None):
        if not rate_form:
            rate_form = self.rate_form_class(
                initial={
                    'created_by': created_by.id,
                    'application': application.id,
                }
            )
        displayed_data = application.get_data(self.displayed_data)
        for item in displayed_data:

            # *** fix simple values ***
            if item.get('name')=='citizenship':
                item['content']=dict(Application2018.COUNTRY_CHOICES).get(item.get('content'))
            if item.get('name')=='residence':
                item['content']=dict(Application2018.COUNTRY_CHOICES).get(item.get('content'))
            if item.get('name')=='field':
                item['content']=dict(Application2018.FIELD_CHOICES).get(item.get('content'))
            # ... and more fields from R2 form
            if item.get('name')=='age':
                item['content']=dict(Application2018.AGE_CHOICES).get(item.get('content'))
            if item.get('name')=='fundraising_potential':
                item['content']=dict(Application2018.FUNDRAISING_POTENTIAL_CHOICES).get(item.get('content'))
            if item.get('name')=='experience':
                item['content']=dict(Application2018.EXPERIENCE_CHOICES).get(item.get('content'))

            # *** fix checkboxes ***
            if item.get('name')=='profession':
                item['content']=', '.join([dict(Application2018.PROFESSION_CHOICES).get(choice, '[*UNKNOWN OPTION*]') for choice in ast.literal_eval(item.get('content'))])
            if item.get('name')=='events':
                item['content']=', '.join([dict(Application2018.EVENTS_CHOICES).get(choice, '[*UNKNOWN OPTION*]') for choice in ast.literal_eval(item.get('content'))])
            if item.get('name')=='degrees':
                item['content']=', '.join([dict(Application2018.DEGREES_CHOICES).get(choice, '[*UNKNOWN OPTION*]') for choice in ast.literal_eval(item.get('content'))])
            if item.get('name')=='expenses':
                item['content']=', '.join([dict(Application2018.EXPENSES_CHOICES).get(choice, '[*UNKNOWN OPTION*]') for choice in ast.literal_eval(item.get('content'))])

            # *** fix checkboxes stored as simple comma-separated values ***
            # (these are imported elements, not properly stored as lists: `['value1', 'value2']` but as strings: `value1, value2`)
            if item.get('name')=='attended' and item.get('content'):
                item['content']=', '.join([dict(Application2018.ATTENDED_CHOICES).get(choice, '[*UNKNOWN OPTION*]') for choice in item.get('content').split(', ')])
            if item.get('name')=='engagement' and item.get('content'):
                item['content']=', '.join([dict(Application2018.ENGAGEMENT_CHOICES).get(choice, '[*UNKNOWN OPTION*]') for choice in item.get('content').split(', ')])

            # *** fix complex fields (gender, ethnicity) ***
            if item.get('name')=='gender':
                try:
                    content=ast.literal_eval(item.get('content'))
                    if content[1]:
                        item['content'] = dict(Application2018.GENDER_CHOICES).get(content[1])
                    else:
                        item['content'] = dict(Application2018.GENDER_CHOICES).get(content[0])
                except:
                    print('error parsing gender')

            if item.get('name')=='ethnicity':
                lst = []
                try:
                    content=ast.literal_eval(item.get('content'))
                    if content[0]:
                        lst.extend([dict(Application2018.ETHNICITY_CHOICES).get(choice, '[*UNKNOWN OPTION*]') for choice in content[0] if choice!='other'])
                    if content[1]:
                        lst.append(str('WRITTEN IN: ' + content[1]))
                    item['content']=', '.join(lst)
                except:
                    print('error parsing ethnicity')

        context = {
            'user': created_by,
            'rate_count': created_by.rated1.count(),
            'application_data': displayed_data,
            'forms': {
                'rate': rate_form,
                'status': ChangeStatusForm(
                    initial={
                        'choice': application.status,
                        'reason': application.status_reason,
                        'application': application.pk
                    }
                ),
            },
            'skip_url': self.skip_url,
        }

        return context

    def change_status(self, request, user, rating_pk):
        application = get_object_or_404(Application2018, pk=request.POST['application'])

        form = ChangeStatusForm(request.POST)
        if user.organizer and form.is_valid():
            ip = request.META.get('HTTP_X_REAL_IP') or request.META['REMOTE_ADDR']
            application.change_status(form.cleaned_data['choice'], user, ip, form.cleaned_data['reason'])

        return self.get(request, rating_pk)

    def post(self, request, rating_pk=None):
        user = super().get_user(request)
        if request.POST.get('choice'):
            return self.change_status(request, user, rating_pk)
        else:
            return self.rate(request, user, rating_pk)


class Round0RateView(AbstractRateView):
    displayed_data = DISPLAYED_FIELDS_ROUND_0
    rate_form_class = Round0RateForm
    permission = 0
    skip_url = reverse_lazy('rating:rate_round0')

    def get(self, request, rating_pk=None):
        user = super().get_user(request)

        if rating_pk is None:
            unrated0 = Application2018.objects.get_unrated0(user).order_by('?').first()
        else:
            unrated0 = get_object_or_404(Round0Rating, pk=rating_pk, created_by=user)
            if not unrated0.application.need_rating0:
                return render(request, 'rating/cannot_rate.html', context={'user': user})

        if unrated0:
            template_name = 'rating/round0-rate.html'

            if rating_pk is None:
                context = self.get_context_data(user, unrated0)
            else:
                rate_form = Round0RateForm(instance=unrated0)
                context = self.get_context_data(user, unrated0.application, rate_form)
        else:
            template_name = 'rating/all_rated.html'
            context = {'user': user}

        return render(request, template_name, context=context)

    def rate(self, request, user, rating_pk):
        if rating_pk is None:
            rate_form = Round0RateForm(request.POST)
        else:
            rating = get_object_or_404(Round0Rating, pk=rating_pk, created_by=user)
            rate_form = Round1RateForm(request.POST, instance=rating)

        if rate_form.is_valid():
            rating = rate_form.save(commit=False)
            rating.created_by = user
            rating.ipaddress = request.META.get('HTTP_X_REAL_IP') or request.META['REMOTE_ADDR']
            rating.save()

            if rating.decision == 'review':
                return redirect('rating:rate_round1_by_application', application_pk=rating.application.pk)
        else:
            application = rate_form.cleaned_data['application']
            context = self.get_context_data(user, application, rate_form=rate_form)
            return render(request, 'rating/round0-rate.html', context=context)

        return redirect('rating:rate_round0')


class Round1RateView(AbstractRateView):
    rate_form_class = Round1RateForm
    permission = 1
    skip_url = reverse_lazy('rating:rate_round1')

    def get(self, request, rating_pk=None):
        user = super().get_user(request)

        if rating_pk is None:
            unrated1 = Application2018.objects.get_unrated1(user).order_by('?').first()
        else:
            unrated1 = get_object_or_404(Round1Rating, pk=rating_pk, created_by=user)
            if not unrated1.application.need_rating1:
                return render(request, 'rating/cannot_rate.html', context={'user': user})

        if unrated1:
            template_name = 'rating/round1-rate.html'

            if rating_pk is None:
                context = self.get_context_data(user, unrated1)
            else:
                rate_form = Round1RateForm(instance=unrated1)
                context = self.get_context_data(user, unrated1.application, rate_form)
        else:
            template_name = 'rating/all_rated.html'
            context = {'user': user}

        return render(request, template_name, context=context)

    def rate(self, request, user, rating_pk):
        if rating_pk is None:
            rate_form = Round1RateForm(request.POST)
        else:
            rating = get_object_or_404(Round1Rating, pk=rating_pk, created_by=user)
            rate_form = Round1RateForm(request.POST, instance=rating)

        if rate_form.is_valid():
            rating = rate_form.save(commit=False)
            rating.created_by = user
            rating.ipaddress = request.META.get('HTTP_X_REAL_IP') or request.META['REMOTE_ADDR']
            rating.save()

            # "user" received as argument... also: user = super().get_user(request)
            if user.is_round_2_reviewer:
                r2review = Round2Rating.objects.create(
                    created_by = rating.created_by,
                    application = rating.application,
                    ipaddress = rating.ipaddress,
                    rating = rating.rating,
                    decision = rating.decision,
                    recommendations = rating.recommendations,
                    comments = rating.comments,
                    note = rating.note,
                )
                r2review.save()
                # print([field.name for field in rating._meta.fields])
                # >>> ['id', 'created_at', 'updated_at', 'created_by', 'application', 'ipaddress', 'rating', 'decision', 'recommendations', 'comments', 'note']

            print("RATING CREATED BY: ", rating.created_by)
        else:
            application = rate_form.cleaned_data['application']
            context = self.get_context_data(user, application, rate_form=rate_form)
            return render(request, 'rating/round1-rate.html', context=context)

        return_url = request.GET.get('return')
        if return_url:
            return redirect(return_url)
            return redirect(unquote(return_url))
        else:
            return redirect('rating:rate_round1')

        return redirect('rating:rate_round1')


class Round1RateByApplicationIdView(Round1RateView):
    def get(self, request, application_pk):
        user = super().get_user(request)

        is_okay1 = Round0Rating.objects.filter(application__pk=application_pk, created_by=user).exists()
        is_okay2 = not Round1Rating.objects.filter(application__pk=application_pk, created_by=user).exists()

        # #todo -- investigate this issue, it does happen sometimes
        # if not is_okay1 or not is_okay2:
        #     raise Http404('Something does not seem right.')

        unrated1 = get_object_or_404(Application2018, pk=application_pk)
        context = self.get_context_data(user, unrated1)
        return render(request, 'rating/round1-rate.html', context=context)

    def post(self, request, application_pk):
        user = super().get_user(request)
        if request.POST.get('choice'):
            # #fyi -- when changing status, "request.GET.get('return')" is ignored
            return self.change_status(request, user, application_pk)
        else:
            return self.rate(request, user, None)


class AbstractRound2RateView(AbstractRateView):
    permission = 2
    rate_form_class = Round2RateForm
    skip_url = reverse_lazy('rating:rate_round2')
    displayed_data = DISPLAYED_FIELDS_ROUND_2
    # displayed_data = None  # for displaying all the data

    def get_context_data(self, created_by, application, rate_form=None):
        context = super().get_context_data(created_by, application, rate_form)
        r2_ratings = application.ratings2.all()
        context.update({'r2_ratings': r2_ratings})
        r1_ratings = application.ratings1.all()
        context.update({'r1_ratings': r1_ratings})
        return context


class Round2RateView(AbstractRound2RateView):
    def get(self, request, rating_pk=None):
        user = super().get_user(request)
        context = {'user': user}
        template_name = 'rating/round2-rate.html'
        if rating_pk is None:  # new rating
            application = Application2018.objects.get_unrated2(user).order_by('?').first()
            if application:
                context = self.get_context_data(user, application)
            else:
                template_name = 'rating/all_rated.html'
        else:  # old rating
            rating = get_object_or_404(Round2Rating, pk=rating_pk, created_by=user)
            rate_form = Round2RateForm(instance=rating)
            context = self.get_context_data(user, rating.application, rate_form)

        return render(request, template_name, context=context)

    def rate(self, request, user, rating_pk):
        if rating_pk is None:
            rate_form = Round2RateForm(request.POST)
        else:
            rating = get_object_or_404(Round2Rating, pk=rating_pk, created_by=user)
            rate_form = Round2RateForm(request.POST, instance=rating)

        if rate_form.is_valid():
            rating = rate_form.save(commit=False)
            rating.created_by = user
            rating.ipaddress = request.META.get('HTTP_X_REAL_IP') or request.META['REMOTE_ADDR']
            rating.save()
        else:
            application = rate_form.cleaned_data['application']
            context = self.get_context_data(user, application, rate_form=rate_form)
            return render(request, 'rating/round2-rate.html', context=context)

        return redirect('rating:rate_round2')


class Round2RateSelectView(AbstractRound2RateView):
    def get(self, request, rating_pk):
        user = super().get_user(request)
        application = Application2018.objects.get(pk=rating_pk)

        try:
            old_rating = Round2Rating.objects.get(application=application, created_by=user)
            rate_form = Round2RateForm(instance=old_rating)
            context = self.get_context_data(user, application, rate_form)
        except Round2Rating.DoesNotExist:
            context = self.get_context_data(user, application)

        return render(request, 'rating/round2-rate.html', context=context)

    def rate(self, request, user, application_pk):
        application = Application2018.objects.get(pk=application_pk)

        try:
            old_rating = Round2Rating.objects.get(application=application, created_by=user)
            rate_form = Round2RateForm(request.POST, instance=old_rating)
        except Round2Rating.DoesNotExist:
            rate_form = Round2RateForm(request.POST)

        if rate_form.is_valid():
            rating = rate_form.save(commit=False)
            rating.created_by = self.get_user()
            rating.ipaddress = request.META.get('HTTP_X_REAL_IP') or request.META['REMOTE_ADDR']
            rating.save()
        else:
            context = self.get_context_data(user, application, rate_form=rate_form)
            return render(request, 'rating/round2-rate.html', context=context)

        return redirect('rating:previous2', rating_pk=application.pk)


class Round0Stats(AuthenticatedMixin, TemplateView):
    template_name = 'rating/stats0.html'
    permission = -1  # R0 permission removed (all reviewers should see all leaderboards)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = User.objects.annotate(finished_count0=Count('rated0')).prefetch_related('rated0')
        users = users.filter(finished_count0__gte=1).order_by('-finished_count0')[:settings.LEADERBOARD_ROUND0_MAX_DISPLAYED]
        context.update({'ranking': users})
        return context


class Round1Stats(AuthenticatedMixin, TemplateView):
    template_name = 'rating/stats1.html'
    permission = -1  # R1 permission removed (all reviewers should see all leaderboards)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = User.objects.annotate(finished_count1=Count('rated1')).prefetch_related('rated1')
        users = users.filter(finished_count1__gte=1).order_by('-finished_count1')[:settings.LEADERBOARD_ROUND1_MAX_DISPLAYED]
        context.update({'ranking': users})
        return context


class Round2Stats(AuthenticatedMixin, TemplateView):
    template_name = 'rating/stats2.html'
    permission = -1  # R2 permission removed (all reviewers should see all leaderboards)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = User.objects.annotate(
            finished_count2=Count('rated2', distinct=True),
            finished_count1=Count('rated1', distinct=True),

            # FYI: "distinct=True" is required, otherwise multiple aggregations with annotate will yield incorrect results: https://docs.djangoproject.com/en/dev/topics/db/aggregation/#combining-multiple-aggregations

            # finished_count2=(Count('rated2') - Count('rated1')), # should be possible -- see https://docs.djangoproject.com/en/dev/ref/models/expressions/#aggregate-expressions -- but it does not seem to work... see also: https://code.djangoproject.com/ticket/10060
        ).prefetch_related('rated2').prefetch_related('rated1')
        users = users.filter(finished_count2__gte=1).order_by('-finished_count2')[:settings.LEADERBOARD_ROUND2_MAX_DISPLAYED]

        # annotate the queryset with a custom calculated value (slow but we don't really care: the leaderboard is small)
        # why this is necessary: R1 reviews are copied over to R2 but we do not want to count R1 items...
        for u in users :
            u.actual_r2_reviews_count = u.finished_count2 - u.finished_count1
        users = sorted(users, key=operator.attrgetter('actual_r2_reviews_count'), reverse=True)

        context.update({'ranking': users})
        return context


class Round1PreviousRatings(AuthenticatedMixin, ListView):
    template_name = 'rating/ratings_list.html'
    permission = 1

    def get_queryset(self):
        user = self.get_user()
        return Round1Rating.objects.filter(created_by=user) # .prefetch_related('application', 'application__institution')

class AllRound1(AuthenticatedMixin, ListView):
    template_name = 'rating/application_list-round1.html'
    permission = 1

    def get_queryset(self):
        return Application2018.objects.get_all_round1() # .prefetch_related('institution')

    def get_context_data(self, **kwargs):
        user_id = self.get_user().pk
        user = User.objects.prefetch_related('rated1', 'rated1__application').get(pk=user_id)
        context = super().get_context_data(**kwargs)
        context.update({'user': user})
        return context

class AllRound2(AuthenticatedMixin, ListView):
    template_name = 'rating/application_list-round2.html'
    permission = 2

    def get_queryset(self):
        return Application2018.objects.get_all_round2() # .prefetch_related('institution')

    def get_context_data(self, **kwargs):
        user_id = self.get_user().pk
        user = User.objects.prefetch_related('rated2', 'rated2__application').get(pk=user_id)
        context = super().get_context_data(**kwargs)
        context.update({'user': user})
        return context

# loosely inspired by https://web.archive.org/web/20170704150829/https://raw.githubusercontent.com/WISVCH/dienst2/4d79c79e519cd0ed9953bd60eef288619d071f6c/post/views.py
class Round1NeedsReview(AuthenticatedMixin, FilterView):
    template_name = 'rating/round1-needs-review.html'
    permission = 1
    filterset_class = Round1NeedsReviewFilter

    def get_queryset(self):
        return Application2018.objects.get_all_round1().exclude(ratings1__created_by=self.user).order_by('citizenship') # .prefetch_related('institution') -- .select_related('sender', 'recipient', 'category')

    def get_context_data(self, **kwargs):
        user_id = self.get_user().pk
        user = User.objects.prefetch_related('rated1', 'rated1__application').get(pk=user_id)
        context = super(Round1NeedsReview, self).get_context_data(**kwargs)
        context.update({'user': user})
        return context
