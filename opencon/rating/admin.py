from django.contrib import admin
from .models import User, Round1Rating, Round2Rating, Round0Rating

from import_export import resources
from import_export.admin import ImportExportModelAdmin


class Round0RatingResource(resources.ModelResource):

    class Meta:
        model = Round0Rating
        # id, created_at, updated_at, created_by, application, ipaddress, decision, comments
        fields = "id created_by application decision comments".split()
        skip_unchanged = True
        report_skipped = True


class Round1RatingResource(resources.ModelResource):

    class Meta:
        model = Round1Rating
        # id, created_at, updated_at, created_by, application, ipaddress, rating, decision, recommendations, comments, note
        fields = "id created_by application rating decision recommendations comments note".split()
        skip_unchanged = True
        report_skipped = True


class Round2RatingResource(resources.ModelResource):

    class Meta:
        model = Round2Rating
        # id, created_at, updated_at, created_by, application, ipaddress, rating, decision, recommendations, comments, note
        fields = "id created_by application rating decision recommendations comments note".split()
        skip_unchanged = True
        report_skipped = True


class UserResource(resources.ModelResource):

    class Meta:
        model = User
        skip_unchanged = True
        report_skipped = True


@admin.register(Round0Rating)
class Round0RatingAdmin(ImportExportModelAdmin): # Round0RatingAdmin(ImportExportModelAdmin, admin.ModelAdmin)
    list_display = ['id', 'created_by', 'application', 'get_application__email', 'decision', 'created_at']
    list_per_page = 500  # pagination
    search_fields = ('application__first_name', 'application__last_name', 'application__email', )

    resource_class = Round0RatingResource # django-import-export resource

    def get_application__email(self, obj):
        return obj.application.email
    get_application__email.admin_order_field  = 'application__email'  # Allows column order sorting
    get_application__email.short_description = 'Application E-mail'  # Renames column head


@admin.register(Round1Rating)
class Round1RatingAdmin(ImportExportModelAdmin):
    list_display = ('id', 'created_by', 'application', 'get_application__email', 'rating', 'created_at')
    list_per_page = 500  # pagination
    search_fields = ('application__first_name', 'application__last_name', 'application__email', )

    resource_class = Round1RatingResource # django-import-export resource

    def get_application__email(self, obj):
        return obj.application.email
    get_application__email.admin_order_field  = 'application__email'  # Allows column order sorting
    get_application__email.short_description = 'Application E-mail'  # Renames column head


@admin.register(Round2Rating)
class Round2RatingAdmin(ImportExportModelAdmin):
    list_display = ('id', 'created_by', 'application', 'get_application__email', 'rating', 'created_at')
    list_per_page = 500  # pagination
    search_fields = ('application__first_name', 'application__last_name', 'application__email', )

    resource_class = Round2RatingResource # django-import-export resource

    def get_application__email(self, obj):
        return obj.application.email
    get_application__email.admin_order_field  = 'application__email'  # Allows column order sorting
    get_application__email.short_description = 'Application E-mail'  # Renames column head


@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    list_display = ('nick', 'email', 'first_name', 'last_name', 'organizer', 'invitation_sent', 'disabled_at')
    list_per_page = 500  # pagination
    search_fields = ('nick', 'email', 'first_name', 'last_name', )

    resource_class = UserResource # django-import-export resource
