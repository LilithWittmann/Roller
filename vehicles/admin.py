from django.contrib import admin

# Register your models here.
from django.forms import ModelForm
from django_admin_json_editor import JSONEditorWidget
from leaflet.admin import LeafletGeoAdmin

from vehicles.models import ServiceTrackingArea, ServiceProvider, Vehicle, VehicleLocationTrack


class ServiceTrackingAreaAdmin(LeafletGeoAdmin):
    pass


admin.site.register(ServiceTrackingArea, ServiceTrackingAreaAdmin)


class VehicleLocationTrackAdmin(LeafletGeoAdmin):
    pass


admin.site.register(VehicleLocationTrack, VehicleLocationTrackAdmin)


class ServiceProviderAdminForm(ModelForm):
    model = ServiceProvider

    class Meta:
        widgets = {
            'settings': JSONEditorWidget({}, collapsed=False),
        }


class ServiceProviderAdmin(admin.ModelAdmin):
    form = ServiceProviderAdminForm
    fields = ('name', 'crawler', 'settings')


admin.site.register(ServiceProvider, ServiceProviderAdmin)
admin.site.register(Vehicle)
