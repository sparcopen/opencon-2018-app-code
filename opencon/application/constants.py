# #todo -- make these constants configurable via admin
# https://django-constance.readthedocs.io/en/latest/
# note that the constants below are example only (different constants were used during the application process)

R0_YESES_NEEDED = 2
# R0_NOS_NEEDED = 2
R0_RATINGS_NEEDED = 3 # changed from 2 to 3 in 2018 (this number should never be reached) -- "yes" + "no" moved the application to R1, which was undesired this year (in 2017, a single "yes" was enough to move this on)
R0_R1_NOS_TO_BLACKLIST = 2 # if this number of negative reviews are reached across R0 and R1, the application is blacklisted
MINIMUM_RATED_QUERYSET_LENGTH = 20
MAX_REVIEWS_ROUND_ONE = 2
MAX_REVIEWS_ROUND_TWO = 2
RATING_R1_LOW_THRESHOLD = 5 # 2017-07-06`06:34:08 -- changed option to 0 to prevent from being active: "This is a last resort, and isn’t as relevant this year anyways since we have R0."
NEEDED_RATING_TO_ROUND2 = 7.5
NEEDED_RATING_FOR_THIRD_REVIEW_ROUND1 = 5
NEEDED_DIFFERENCE_FOR_THIRD_REVIEW_ROUND1 = 2
APPLICATION_DEADLINE = '2018/07/14 11:59'  # YEAR/MONTH/DAY HOUR:MINUTE -- 24h format, UTC -- CAREFUL: consider using 23:59 in the last time zone on Earth, like in 2017 and 2018 -- or Hawaii time (discuss with Nicole)

# NOTE: Constants can be adjusted as needed over time, though depending on implementation changes may result in brief downtime or short temporary inconsistency while the database recalculates ("docker-compose run django python manage.py recalculate_ratings"). Default values are provided for reference.

# amusingly, there is no consensus whether "yeses" or "yesses" is the correct plural of "yes" but "yeses" is preferable
# https://web.archive.org/web/20170706034418/https://english.stackexchange.com/questions/168675/plural-of-yes
