from django.contrib import admin

# Register your models here.
from django.forms import ModelForm
from django_admin_json_editor import JSONEditorWidget
from leaflet.admin import LeafletGeoAdmin

from vehicles.management.commands.crawl_vehicles import import_crawler
from vehicles.models import ServiceTrackingArea, ServiceProvider, Vehicle, VehicleLocationTrack, TripEstimation, \
    Pricing, SubUrb, ReceivedSMS


class ServiceTrackingAreaAdmin(LeafletGeoAdmin):
    pass


admin.site.register(ServiceTrackingArea, ServiceTrackingAreaAdmin)


class TripEstimationAdmin(LeafletGeoAdmin):
    fields = ('duration', 'vehicle', 'updated_at', 'start_position', 'end_position', 'battery_consumption', 'price_estimation',
              'route_estimation', 'route_duration_estimation', 'route_distance_estimation', 'trip_type')
    readonly_fields = ('duration', 'vehicle', 'updated_at', 'start_position', 'end_position', 'battery_consumption',
                       'price_estimation')


admin.site.register(TripEstimation, TripEstimationAdmin)


class VehicleLocationTrackAdmin(LeafletGeoAdmin):
    pass


admin.site.register(VehicleLocationTrack, VehicleLocationTrackAdmin)


class SubUrbAdmin(LeafletGeoAdmin):
    pass


admin.site.register(SubUrb, SubUrbAdmin)


class ServiceProviderAdminForm(ModelForm):
    model = ServiceProvider

    class Meta:
        widgets = {
            'settings': JSONEditorWidget({}, collapsed=False),
        }



def authorize_service_provider(modeladmin, request, queryset):
    for service in queryset:
        crawler_cls = import_crawler(service.crawler)
        crawler = crawler_cls(service.settings)
        if "authorize" in dir(crawler):
            crawler.authorize(service.settings)
authorize_service_provider.short_description = "Start authorization fot selected service providers"


class ServiceProviderAdmin(admin.ModelAdmin):
    form = ServiceProviderAdminForm
    fields = ('name', 'crawler', 'settings', 'primary_color', 'text_color')
    actions = [authorize_service_provider]

admin.site.register(ServiceProvider, ServiceProviderAdmin)
admin.site.register(Vehicle)
admin.site.register(Pricing)

admin.site.register(ReceivedSMS)