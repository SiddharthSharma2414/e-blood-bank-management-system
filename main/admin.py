from django.contrib import admin
from django.utils.html import format_html
from .models import BloodRequest, BloodStock, Donor


def colored_status(obj):
    if obj.status == "Approved":
        color = "green"
    elif obj.status == "Completed":
        color = "red"
    else:
        color = "orange"

    return format_html(
        '<span style="color:{}; font-weight:bold;">{}</span>',
        color,
        obj.status
    )

colored_status.short_description = "Status"


def mark_approved(modeladmin, request, queryset):
    queryset.update(status="Approved")

mark_approved.short_description = "Mark selected as Approved"


def mark_completed(modeladmin, request, queryset):
    queryset.update(status="Completed")

mark_completed.short_description = "Mark selected as Completed"


# ===== BLOOD REQUEST ADMIN =====
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = (
        'blood_group',
        'city',
        'quantity',
        'contact',
        'request_date',
        'colored_status'
    )

    list_filter = ('status', 'city', 'blood_group')
    search_fields = ('blood_group', 'city', 'contact')
    ordering = ('-request_date',)

    readonly_fields = ('request_date',)

    actions = [mark_approved, mark_completed]

    def colored_status(self, obj):
        return colored_status(obj)


# ===== BLOOD STOCK ADMIN =====
class BloodStockAdmin(admin.ModelAdmin):
    list_display = ('blood_group', 'units', 'city')
    search_fields = ('blood_group', 'city')


# ===== DONOR ADMIN =====
class DonorAdmin(admin.ModelAdmin):
    list_display = ('name', 'blood_group', 'phone', 'age')
    search_fields = ('name', 'blood_group', 'phone')


# ===== REGISTER MODELS =====
admin.site.register(BloodRequest, BloodRequestAdmin)
admin.site.register(BloodStock, BloodStockAdmin)
admin.site.register(Donor, DonorAdmin)