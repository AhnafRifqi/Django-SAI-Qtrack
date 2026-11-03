from django import forms
from .models import DefectLog, Line, HarnessPart, DefectCategory


class DefectLogForm(forms.ModelForm):
    class Meta:
        model = DefectLog
        fields = [
            'line',
            'harness_part',
            'defect_category',
            'shift',
            'quantity',
            'action_taken',
            'inspector_name',
            'notes',
        ]
        widgets = {
            'line': forms.Select(attrs={'class': 'form-select'}),
            'harness_part': forms.Select(attrs={'class': 'form-select'}),
            'defect_category': forms.Select(attrs={'class': 'form-select'}),
            'shift': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'value': 1}),
            'action_taken': forms.Select(attrs={'class': 'form-select'}),
            'inspector_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Operator / QC'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Catatan detail temuan atau nomor cavity...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['line'].queryset = Line.objects.filter(is_active=True)
        self.fields['harness_part'].queryset = HarnessPart.objects.filter(is_active=True)
        self.fields['defect_category'].queryset = DefectCategory.objects.all()
