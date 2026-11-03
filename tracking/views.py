from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta

from .models import DefectLog, Line, HarnessPart, DefectCategory, ActionDisposition, DefectSeverity
from .forms import DefectLogForm


def dashboard_view(request):
    days_filter = int(request.GET.get('days', 7))
    line_filter = request.GET.get('line', '')
    shift_filter = request.GET.get('shift', '')

    today = timezone.localdate()

    # Rekapitulasi scrap hari ini (Real-Time Shopfloor Metric)
    today_stats = DefectLog.objects.filter(logged_at__date=today).aggregate(
        today_total=Sum('quantity'),
        today_scrap=Sum('quantity', filter=Q(action_taken=ActionDisposition.SCRAP)),
        today_rework=Sum('quantity', filter=Q(action_taken=ActionDisposition.REWORK)),
    )
    today_scrap = today_stats['today_scrap'] or 0
    today_total = today_stats['today_total'] or 0

    # Queryset berdasarkan filter waktu dan lini/shift
    since_date = timezone.now() - timedelta(days=days_filter)
    logs_qs = DefectLog.objects.filter(logged_at__gte=since_date)

    if line_filter:
        logs_qs = logs_qs.filter(line__code=line_filter)
    if shift_filter:
        logs_qs = logs_qs.filter(shift=int(shift_filter))

    # Agregasi totals menggunakan Sum dan Count
    totals = logs_qs.aggregate(
        total_items=Sum('quantity'),
        total_logs=Count('id'),
        total_scrap=Sum('quantity', filter=Q(action_taken=ActionDisposition.SCRAP)),
        total_rework=Sum('quantity', filter=Q(action_taken=ActionDisposition.REWORK)),
        total_critical=Sum('quantity', filter=Q(defect_category__severity=DefectSeverity.CRITICAL)),
    )

    # Top 5 Defect menggunakan annotate Sum dan Count
    top_defects = (
        DefectCategory.objects.filter(defect_logs__in=logs_qs)
        .annotate(
            total_qty=Sum('defect_logs__quantity'),
            incident_count=Count('defect_logs')
        )
        .order_by('-total_qty')[:5]
    )

    # Distribusi defect per lini produksi
    line_distribution = (
        Line.objects.filter(defect_logs__in=logs_qs)
        .annotate(
            total_qty=Sum('defect_logs__quantity'),
            log_count=Count('defect_logs')
        )
        .order_by('-total_qty')
    )

    recent_logs = logs_qs.select_related('line', 'harness_part', 'defect_category')[:12]

    context = {
        'today_scrap': today_scrap,
        'today_total': today_total,
        'totals': totals,
        'top_defects': top_defects,
        'line_distribution': line_distribution,
        'recent_logs': recent_logs,
        'lines': Line.objects.filter(is_active=True),
        'days_filter': days_filter,
        'selected_line': line_filter,
        'selected_shift': shift_filter,
    }
    return render(request, 'tracking/dashboard.html', context)


def log_create_view(request):
    if request.method == 'POST':
        form = DefectLogForm(request.POST)
        if form.is_valid():
            log = form.save()
            messages.success(
                request,
                f"Defect berhasil dicatat untuk {log.line.code} ({log.defect_category.name})!"
            )
            return redirect('tracking:log_create')
    else:
        form = DefectLogForm()

    recent_entries = DefectLog.objects.select_related('line', 'harness_part', 'defect_category')[:5]

    context = {
        'form': form,
        'recent_entries': recent_entries,
    }
    return render(request, 'tracking/log_create.html', context)


def log_list_view(request):
    logs = DefectLog.objects.select_related('line', 'harness_part', 'defect_category')

    line_filter = request.GET.get('line', '')
    shift_filter = request.GET.get('shift', '')
    action_filter = request.GET.get('action', '')

    if line_filter:
        logs = logs.filter(line__code=line_filter)
    if shift_filter:
        logs = logs.filter(shift=int(shift_filter))
    if action_filter:
        logs = logs.filter(action_taken=action_filter)

    context = {
        'logs': logs[:50],
        'lines': Line.objects.filter(is_active=True),
        'selected_line': line_filter,
        'selected_shift': shift_filter,
        'selected_action': action_filter,
    }
    return render(request, 'tracking/log_list.html', context)
