from django.db import models
from django.utils import timezone


class LineSection(models.TextChoices):
    CUTTING = 'CUTTING', 'Cutting & Stripping'
    CRIMPING = 'CRIMPING', 'Terminal Crimping'
    SUB_ASSEMBLY = 'SUB_ASSEMBLY', 'Sub-Assembly & Jointing'
    FINAL_ASSEMBLY = 'FINAL_ASSEMBLY', 'Final Assembly / Layout'
    INSPECTION = 'INSPECTION', 'Electrical & Visual Inspection'


class DefectSeverity(models.TextChoices):
    MINOR = 'MINOR', 'Minor'
    MAJOR = 'MAJOR', 'Major'
    CRITICAL = 'CRITICAL', 'Critical'


class ActionDisposition(models.TextChoices):
    SCRAP = 'SCRAP', 'Scrap (Discard)'
    REWORK = 'REWORK', 'Rework (Fix)'


class Line(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    section = models.CharField(
        max_length=30,
        choices=LineSection.choices,
        default=LineSection.FINAL_ASSEMBLY
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name}"


class HarnessPart(models.Model):
    part_number = models.CharField(max_length=50, unique=True)
    car_model = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['part_number']

    def __str__(self):
        return f"{self.part_number} ({self.car_model})"


class DefectCategory(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=120)
    section = models.CharField(
        max_length=30,
        choices=LineSection.choices,
        default=LineSection.INSPECTION
    )
    severity = models.CharField(
        max_length=20,
        choices=DefectSeverity.choices,
        default=DefectSeverity.MAJOR
    )

    class Meta:
        verbose_name_plural = 'Defect Categories'
        ordering = ['section', 'code']

    def __str__(self):
        return f"[{self.code}] {self.name} ({self.get_severity_display()})"


class DefectLog(models.Model):
    SHIFT_CHOICES = [
        (1, 'Shift 1 (07:00 - 15:30)'),
        (2, 'Shift 2 (15:30 - 23:30)'),
        (3, 'Shift 3 (23:30 - 07:00)'),
    ]

    line = models.ForeignKey(
        Line,
        on_delete=models.PROTECT,
        related_name='defect_logs'
    )
    harness_part = models.ForeignKey(
        HarnessPart,
        on_delete=models.PROTECT,
        related_name='defect_logs'
    )
    defect_category = models.ForeignKey(
        DefectCategory,
        on_delete=models.PROTECT,
        related_name='defect_logs'
    )
    shift = models.PositiveSmallIntegerField(choices=SHIFT_CHOICES, default=1)
    quantity = models.PositiveIntegerField(default=1)
    action_taken = models.CharField(
        max_length=20,
        choices=ActionDisposition.choices,
        default=ActionDisposition.REWORK
    )
    inspector_name = models.CharField(max_length=100)
    notes = models.TextField(blank=True)
    logged_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-logged_at']

    def __str__(self):
        return (
            f"Log #{self.pk or '-'} | {self.line.code} | "
            f"{self.defect_category.name} (Qty: {self.quantity})"
        )
