from import_export import resources
from .models import Application2018, Draft
from opencon.rating.models import User, Round0Rating, Round1Rating, Round2Rating

# --- export of selected fields (for google docs / spreadsheet) ---

class Application2018Resource(resources.ModelResource):
    class Meta:
        model = Application2018
        fields = 'id email created_at citizenship residence profession experience field gender engagement referred_by need_rating0 need_rating1 need_rating2 rating1 rating2 status'.split()
        # fields = ('id', 'name', 'author', 'price',)
        # exclude = ('tags',)
        # export_order = ('id', 'price', 'author', 'name',)

        # #todo -- check "orcid", resolve "status_by"

    def get_queryset(self):
        # return self._meta.model.objects.order_by('id') # sort
        return self._meta.model.objects.get_all().order_by('id') # override base QuerySet (keyword: custom model manager) to make sure objects marked as 'deleted' are also included in the export: get_all()

class DraftResource(resources.ModelResource):
    class Meta:
        model = Draft

    def get_queryset(self):
        return self._meta.model.objects.order_by('id') # sort

class UserResource(resources.ModelResource):
    class Meta:
        model = User

    def get_queryset(self):
        return self._meta.model.objects.order_by('id') # sort

class Round0RatingResource(resources.ModelResource):
    class Meta:
        model = Round0Rating
        fields = 'id decision application created_by'.split()

    def get_queryset(self):
        return self._meta.model.objects.order_by('id') # sort

class Round1RatingResource(resources.ModelResource):
    class Meta:
        model = Round1Rating
        fields = 'id rating application created_by'.split()

    def get_queryset(self):
        return self._meta.model.objects.order_by('id') # sort

class Round2RatingResource(resources.ModelResource):
    class Meta:
        model = Round2Rating

    def get_queryset(self):
        return self._meta.model.objects.order_by('id') # sort

# --- export of full tables (all fields) ---

class Application2018FullResource(resources.ModelResource):
    class Meta:
        model = Application2018

    def get_queryset(self):
        # return self._meta.model.objects.order_by('id') # sort
        return self._meta.model.objects.get_all().order_by('id') # override base QuerySet (keyword: custom model manager) to make sure objects marked as 'deleted' are also included in the export: get_all()

class DraftFullResource(resources.ModelResource):
    class Meta:
        model = Draft

    def get_queryset(self):
        return self._meta.model.objects.order_by('id') # sort

class UserFullResource(resources.ModelResource):
    class Meta:
        model = User

    def get_queryset(self):
        return self._meta.model.objects.order_by('id') # sort

class Round0RatingFullResource(resources.ModelResource):
    class Meta:
        model = Round0Rating

    def get_queryset(self):
        return self._meta.model.objects.order_by('id') # sort

class Round1RatingFullResource(resources.ModelResource):
    class Meta:
        model = Round1Rating

    def get_queryset(self):
        return self._meta.model.objects.order_by('id') # sort

class Round2RatingFullResource(resources.ModelResource):
    class Meta:
        model = Round2Rating

    def get_queryset(self):
        return self._meta.model.objects.order_by('id') # sort
