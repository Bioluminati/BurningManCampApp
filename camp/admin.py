from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin

from django.urls import get_script_prefix
from django.utils.encoding import iri_to_uri

from .models import Meal, MealShift, MealRestriction, User, UserAttendance, Bike, Inventory, BicycleMutationInventory, BikeMutationSchedule, Vehicle


class UserAttendanceAdmin(admin.ModelAdmin):
    list_filter = ('event', 'camping_this_year',
        'paid_dues', 'has_ticket', 'looking_for_ticket')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')


class MealAdmin(admin.ModelAdmin):
    list_filter = ('event', 'kind')


class BikeMutationScheduleAdmin(admin.ModelAdmin):
    list_filter = ('event',)


admin.site.register(Meal, MealAdmin)
admin.site.register(MealShift)
admin.site.register(User, UserAdmin)
admin.site.register(UserAttendance, UserAttendanceAdmin)
admin.site.register(Bike)
admin.site.register(Inventory)
admin.site.register(BicycleMutationInventory)
admin.site.register(MealRestriction)
admin.site.register(BikeMutationSchedule, BikeMutationScheduleAdmin)
admin.site.register(Vehicle)


class CustomFlatPageAdmin(FlatPageAdmin):
    def view_on_site(self, obj):
        return iri_to_uri(get_script_prefix().rstrip('/') +
                          '/pages' + obj.url)

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, CustomFlatPageAdmin)
