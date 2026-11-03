from django.test import TestCase
from django.urls import reverse
from .models import Line, HarnessPart, DefectCategory, DefectLog, LineSection, DefectSeverity, ActionDisposition


class TrackingModelTests(TestCase):
    def setUp(self):
        self.line = Line.objects.create(code='L-TEST', name='Test Line', section=LineSection.CRIMPING)
        self.part = HarnessPart.objects.create(part_number='TEST-001', car_model='Test Car')
        self.defect = DefectCategory.objects.create(
            code='D-TEST',
            name='Test Defect',
            section=LineSection.CRIMPING,
            severity=DefectSeverity.MAJOR
        )

    def test_model_creation(self):
        log = DefectLog.objects.create(
            line=self.line,
            harness_part=self.part,
            defect_category=self.defect,
            shift=1,
            quantity=2,
            action_taken=ActionDisposition.SCRAP,
            inspector_name='QC Tester'
        )
        self.assertEqual(log.quantity, 2)
        self.assertIn('L-TEST', str(log))

    def test_dashboard_view(self):
        response = self.client.get(reverse('tracking:dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_log_create_view(self):
        response = self.client.get(reverse('tracking:log_create'))
        self.assertEqual(response.status_code, 200)

    def test_log_create_post_valid(self):
        response = self.client.post(reverse('tracking:log_create'), {
            'line': self.line.id,
            'harness_part': self.part.id,
            'defect_category': self.defect.id,
            'shift': 1,
            'quantity': 3,
            'action_taken': ActionDisposition.SCRAP,
            'inspector_name': 'QC Tester',
            'notes': 'Test notes'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(DefectLog.objects.filter(quantity=3).count(), 1)
