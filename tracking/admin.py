from django.contrib import admin
from .models import Line, HarnessPart, DefectCategory, DefectLog


@admin.register(Line)
class LineAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'section', 'is_active')
    list_filter = ('section', 'is_active')
    search_fields = ('code', 'name')


@admin.register(HarnessPart)
class HarnessPartAdmin(admin.ModelAdmin):
    list_display = ('part_number', 'car_model', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('part_number', 'car_model')


@admin.register(DefectCategory)
class DefectCategoryAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'section', 'severity')
    list_filter = ('section', 'severity')
    search_fields = ('code', 'name')


@admin.register(DefectLog)
class DefectLogAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'logged_at',
        'line',
        'harness_part',
        'defect_category',
        'shift',
        'quantity',
        'action_taken',
        'inspector_name',
    )
    list_filter = ('line', 'shift', 'action_taken', 'defect_category__severity')
    search_fields = (
        'harness_part__part_number',
        'defect_category__name',
        'inspector_name',
        'notes',
    )
    date_hierarchy = 'logged_at'
