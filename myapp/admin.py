from django.contrib import admin
from myapp.models import (
    Farm,
    SubFarm,
    Deforestation,
    ERDA,
)
# Register your models here.

class FarmAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'region', 'municipio', 'departamento')
    search_fields = ('name','owner')


class SubFarmAdmin(admin.ModelAdmin):
    list_display = ('id', 'farm', 'sub_name', 'technical', 'map_date', 'region', 'nom_pol', 'area_pol', 'latitude', 'longitude')
    list_filter = ('technical',)
    search_fields = ('farm',)


class DeforestationAdmin(admin.ModelAdmin):
    list_display = ('id', 'sub_farm', 'level', 'fase')
    search_fields = ('sub_farm',)


class ERDAAdmin(admin.ModelAdmin):
    list_display = ('id', 'sub_farm', 'risk')
    search_fields = ('sub_farm',)
    list_filter = ('risk',)


admin.site.register(Farm, FarmAdmin)
admin.site.register(SubFarm, SubFarmAdmin)
admin.site.register(Deforestation, DeforestationAdmin)
admin.site.register(ERDA, ERDAAdmin)