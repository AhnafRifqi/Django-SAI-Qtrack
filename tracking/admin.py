from django.contrib import admin
from django.utils.html import format_html
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
        'display_logged_at',
        'display_line',
        'display_harness_part',
        'display_defect_category',
        'shift',
        'quantity',
        'display_action_taken',
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
    list_per_page = 25

    @admin.display(description='Waktu', ordering='logged_at')
    def display_logged_at(self, obj):
        return obj.logged_at.strftime('%d/%m/%Y %H:%M')

    @admin.display(description='Line', ordering='line__code')
    def display_line(self, obj):
        return format_html('<span title="{}"><strong>{}</strong></span>', obj.line.name, obj.line.code)

    @admin.display(description='Harness Part', ordering='harness_part__part_number')
    def display_harness_part(self, obj):
        car = obj.harness_part.car_model.split('/')[0].strip() if '/' in obj.harness_part.car_model else obj.harness_part.car_model
        return format_html(
            '<strong>{}</strong><br><small style="color: #94a3b8;">{}</small>',
            obj.harness_part.part_number,
            car[:28]
        )

    @admin.display(description='Defect Category', ordering='defect_category__name')
    def display_defect_category(self, obj):
        return format_html(
            '<span title="{code} - {name}">{name}</span>',
            code=obj.defect_category.code,
            name=obj.defect_category.name
        )

    @admin.display(description='Action', ordering='action_taken')
    def display_action_taken(self, obj):
        if obj.action_taken == 'SCRAP':
            return format_html(
                '<span style="background: #dc2626; color: #ffffff; padding: 2px 8px; border-radius: 9999px; font-weight: 600; font-size: 11px;">SCRAP</span>'
            )
        return format_html(
            '<span style="background: #eab308; color: #000000; padding: 2px 8px; border-radius: 9999px; font-weight: 600; font-size: 11px;">REWORK</span>'
        )

