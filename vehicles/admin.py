from django.contrib import admin

# Register your models here.
from django.forms import ModelForm
from django_admin_json_editor import JSONEditorWidget
from leaflet.admin import LeafletGeoAdmin

from vehicles.models import ServiceTrackingArea, ServiceProvider, Vehicle, VehicleLocationTrack, TripEstimation, \
    Pricing, SubUrb


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


class ServiceProviderAdmin(admin.ModelAdmin):
    form = ServiceProviderAdminForm
    fields = ('name', 'crawler', 'settings', 'primary_color', 'text_color')


admin.site.register(ServiceProvider, ServiceProviderAdmin)
admin.site.register(Vehicle)
admin.site.register(Pricing)
