"""
Application urlconfig
"""
from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^login/(?P<uuid>[0-9a-f-]{32})/$',
        views.Login.as_view(),
        name='login',
    ),
    url(
        r"^logout/$",
        views.Logout.as_view(),
        name="logout"
    ),
    url(
        r'^logged_out/$',
        views.TemplateView.as_view(template_name='rating/logged_out.html'),
        name='logged_out'
    ),

    # ROUND 0 URLs
    url(  # "R0: Rate Applications"
        r"^round0/$",
        views.Round0RateView.as_view(),
        name="rate_round0"
    ),
    url(  # "R0: Leaderboard"
        r"^stats0/$",
        views.Round0Stats.as_view(),
        name="stats0"
    ),

    # ROUND 1 URLs
    url(  # "R1: Rate Applications"
        r"^round1-by-application/(?P<application_pk>[0-9]+)/$",
        views.Round1RateByApplicationIdView.as_view(),
        name="rate_round1_by_application"
    ),
    url(  # "R1: Rate Applications"
        r"^round1/$",
        views.Round1RateView.as_view(),
        name="rate_round1"
    ),
    url( # "R1: All Applications"
        r"^all1/$",
        views.AllRound1.as_view(),
        name="all1"
    ),
    url( # R1: Filter (Needs Review)
        r"^filter1/$",
        views.Round1NeedsReview.as_view(),
        name="round1_needs_review"
    ),
    url(  # "R1: My Ratings"
        r"^old1/$",
        views.Round1PreviousRatings.as_view(),
        name="previous1"
    ),
    url(  # "R1: Leaderboard"
        r"^stats1/$",
        views.Round1Stats.as_view(),
        name="stats1"
    ),
    url(
        r"^old1/(?P<rating_pk>[0-9]+)/$",
        views.Round1RateView.as_view(),
        name="previous1"
    ),

    # ROUND 2 URLs
    url( # "R2: Rate Applications"
        r"^round2/$",
        views.Round2RateView.as_view(),
        name="rate_round2"
    ),
    url( # "R2: All Applications"
        r"^all2/$",
        views.AllRound2.as_view(),
        name="all2"
    ),
    url( # "R2: Leaderboard"
        r"^stats2/$",
        views.Round2Stats.as_view(),
        name="stats2"
    ),
    url(
        r"^old2/(?P<rating_pk>[0-9]+)/$",
        views.Round2RateSelectView.as_view(),
        name="previous2"
    ),
]
