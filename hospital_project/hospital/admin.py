from django.contrib import admin
from .models import Doctor, Patient, Visit, Service, CustomUser
from django.contrib.auth.admin import UserAdmin

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'specialty', 'phone')
    search_fields = ('name', 'specialty')

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'date_of_birth', 'phone')
    search_fields = ('name', 'phone')

@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('id', 'doctor', 'patient', 'date')
    list_filter = ('doctor', 'date')
    search_fields = ('doctor__name', 'patient__name')
    filter_horizontal = ('services',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'cost')
    search_fields = ('name',)

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ["username", "email", "role", "is_staff"]
    fieldsets = UserAdmin.fieldsets + (
        ("Дополнительная информация", {"fields": ("role",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Дополнительная информация", {"fields": ("role",)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)