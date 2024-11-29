from django.contrib import admin

# Register your models here.

from .models import Paslauga, AutomobilioModelis, AutomobilisKlientas, Uzsakymas, UzsakymoEilute


class UzsakymoEiluteInline(admin.TabularInline):
    model = UzsakymoEilute
    extra = 1

class UzsakymasAdmin(admin.ModelAdmin):
    list_display = ('automobilis', 'data', 'statusas')
    inlines = [UzsakymoEiluteInline]


class AutomobilisKlientasAdmin(admin.ModelAdmin):
    list_display = ('klientas', 'modelis', 'valstybinis_nr', 'vin_kodas')
    list_filter = ('klientas', 'modelis')
    search_fields = ('valstybinis_nr', 'vin_kodas')

class PaslaugaAdmin(admin.ModelAdmin):
    list_display = ('pavadinimas', 'kaina')

class AutomobilioModelisAdmin(admin.ModelAdmin):
    list_display = ('marke', 'modelis', 'metai', 'variklis')

admin.site.register(Paslauga, PaslaugaAdmin)
admin.site.register(AutomobilioModelis, AutomobilioModelisAdmin)
admin.site.register(AutomobilisKlientas, AutomobilisKlientasAdmin)
admin.site.register(Uzsakymas, UzsakymasAdmin)
admin.site.register(UzsakymoEilute)