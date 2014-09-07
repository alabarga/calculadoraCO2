from django.contrib import admin
from django.contrib.contenttypes.generic import GenericTabularInline
from co2.models import * 

admin.site.register(Unidad)
admin.site.register(Recurso)
admin.site.register(Medida)
admin.site.register(TipoVehiculo)
admin.site.register(TipoLocal)
admin.site.register(Vehiculo)
admin.site.register(UserProfile)

class ConsumoInline(GenericTabularInline):
    model = Consumo
    extra = 0
    related_lookup_fields = {
        'generic': [['content_type', 'object_id']],
    }

class VehiculoInline(admin.TabularInline):
    model = Vehiculo
    extra = 0

class LocalInline(admin.TabularInline):
    model = Local
    extra = 0

class LocalAdmin(admin.ModelAdmin):
    inlines = [ConsumoInline]

#admin.site.register(Local)
admin.site.register(Local, LocalAdmin)

class EntidadAdmin(admin.ModelAdmin):
    inlines = [VehiculoInline, LocalInline]

#admin.site.register(Entidad)
admin.site.register(Entidad, EntidadAdmin)


class ConsumoOptions(admin.ModelAdmin):
    # define the related_lookup_fields
    related_lookup_fields = {
        'generic': [['content_type', 'object_id']],
    }

admin.site.register(Consumo,ConsumoOptions)