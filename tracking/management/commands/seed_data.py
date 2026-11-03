from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import random

from tracking.models import (
    Line,
    LineSection,
    HarnessPart,
    DefectCategory,
    DefectSeverity,
    DefectLog,
    ActionDisposition,
)


class Command(BaseCommand):
    help = 'Seeds initial wiring harness master data and sample defect logs'

    def handle(self, *args, **options):
        # 1. Superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@sai.local', 'admin123')
            self.stdout.write(self.style.SUCCESS('Admin user created (admin / admin123)'))

        # 2. Master Lines
        lines_data = [
            ('LINE-CUT-01', 'Komax Auto Cutting & Stripping Line 1', LineSection.CUTTING),
            ('LINE-CRM-01', 'Applicator Semi-Auto Crimping Line 1', LineSection.CRIMPING),
            ('LINE-CRM-02', 'Applicator Semi-Auto Crimping Line 2', LineSection.CRIMPING),
            ('LINE-SUB-01', 'Jointing & Sub-Assembly Line 1', LineSection.SUB_ASSEMBLY),
            ('LINE-ASSY-01', 'Main Jig Conveyor Assembly Line 1', LineSection.FINAL_ASSEMBLY),
            ('LINE-CHK-01', 'Checker Board Electrical Inspection 1', LineSection.INSPECTION),
        ]
        created_lines = []
        for code, name, section in lines_data:
            line, _ = Line.objects.get_or_create(code=code, defaults={'name': name, 'section': section})
            created_lines.append(line)

        # 3. Master Harness Parts (Automotive Wire Harnesses)
        parts_data = [
            ('82111-BZ010', 'Avanza / Xenia Engine Compartment Wire Harness', 'Main harness connecting ECU, fusebox, and engine sensors'),
            ('82161-BZ150', 'Veloz Instrument Panel / Dashboard Harness', 'Cabin electrical harness for cluster and multimedia'),
            ('82121-BZ220', 'Rush / Terios Front Door RH Harness', 'Power window, lock actuator, and mirror harness'),
            ('82141-BZ080', 'Agya / Ayla Floor & Fuel Tank Harness', 'Chassis harness routing to fuel pump and rear lamps'),
            ('82151-BZ310', 'Raize / Rocky Roof & Headlining Harness', 'Overhead console, map lamp, and SRS airbag curtain'),
        ]
        created_parts = []
        for pnum, model, desc in parts_data:
            part, _ = HarnessPart.objects.get_or_create(part_number=pnum, defaults={'car_model': model, 'description': desc})
            created_parts.append(part)

        # 4. Master Defect Categories
        defects_data = [
            ('DEF-CRM-01', 'Terminal Crimp Loose (Crimp Height Out of Spec)', LineSection.CRIMPING, DefectSeverity.CRITICAL),
            ('DEF-CRM-02', 'Terminal Pin Bent / Deformed', LineSection.CRIMPING, DefectSeverity.MAJOR),
            ('DEF-WIR-01', 'Wire Core Strand Cut / Nicked', LineSection.CUTTING, DefectSeverity.CRITICAL),
            ('DEF-WIR-02', 'Stripping Burr / Insulation Damage', LineSection.CUTTING, DefectSeverity.MINOR),
            ('DEF-CON-01', 'Terminal Pin Back-out (Retainer Loose)', LineSection.SUB_ASSEMBLY, DefectSeverity.CRITICAL),
            ('DEF-CON-02', 'Wrong Cavity Connector Insertion', LineSection.SUB_ASSEMBLY, DefectSeverity.CRITICAL),
            ('DEF-ELC-01', 'Electrical Continuity Fail (Open Circuit)', LineSection.INSPECTION, DefectSeverity.CRITICAL),
            ('DEF-ELC-02', 'Short Circuit / Crossed Circuit', LineSection.INSPECTION, DefectSeverity.CRITICAL),
            ('DEF-TAP-01', 'Vinyl Taping Loose / Wire Exposed', LineSection.FINAL_ASSEMBLY, DefectSeverity.MINOR),
            ('DEF-DIM-01', 'Branch Wire Length Exceeds Tolerance', LineSection.FINAL_ASSEMBLY, DefectSeverity.MAJOR),
        ]
        created_defects = []
        for code, name, section, severity in defects_data:
            cat, _ = DefectCategory.objects.get_or_create(code=code, defaults={'name': name, 'section': section, 'severity': severity})
            created_defects.append(cat)

        # 5. Sample Defect Logs (for initial dashboard display)
        inspectors = ['Budi Santoso', 'Siti Rahma', 'Ahmad Fauzi', 'Dwi Lestari', 'Eko Prasetyo']
        now = timezone.now()

        if DefectLog.objects.count() < 15:
            for i in range(25):
                log_time = now - timedelta(days=random.randint(0, 4), hours=random.randint(0, 12), minutes=random.randint(0, 50))
                DefectLog.objects.create(
                    line=random.choice(created_lines),
                    harness_part=random.choice(created_parts),
                    defect_category=random.choice(created_defects),
                    shift=random.choice([1, 1, 2, 2, 3]),
                    quantity=random.choice([1, 1, 1, 2, 3, 5]),
                    action_taken=random.choice([ActionDisposition.REWORK, ActionDisposition.REWORK, ActionDisposition.SCRAP]),
                    inspector_name=random.choice(inspectors),
                    notes=random.choice([
                        'Inspeksi visual jig menunjukkan terminal miring.',
                        'Tester kontinuitas mendeteksi open circuit pada pin 4.',
                        'Kabel tergores saat proses penarikan di conveyor layout.',
                        'Crimp height dicek dengan micrometer: 1.15 mm (standar 1.25 mm).',
                        'Poka-yoke checker board mendeteksi salah urutan kabel.',
                        '',
                    ]),
                    logged_at=log_time,
                )
            self.stdout.write(self.style.SUCCESS('25 sample defect logs created.'))

        self.stdout.write(self.style.SUCCESS('Seed completed successfully!'))
