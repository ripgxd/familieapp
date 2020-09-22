from .models import Surname, RelationType, FamillieList
from django.contrib.gis import admin


@admin.register(Surname)
class SurnameAdmin(admin.ModelAdmin):
    list_display = ('surname',)


@admin.register(RelationType)
class RelationTypeAdmin(admin.ModelAdmin):
    list_display = ('relation',)


@admin.register(FamillieList)
class FamilieListAdmin(admin.OSMGeoAdmin):
    list_display = ('surname', 'relation', 'name', 'date', 'address', 'point')

