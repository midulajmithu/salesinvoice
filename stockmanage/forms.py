from django import forms
from .models import P_S_Info

class P_S_InfoForm(forms.ModelForm):
    class Meta:
        model = P_S_Info
        fields = [
            'SorP', 'date', 'mr_mh_no', 'item', 'unit_of_measure', 
            'quantity', 'supplier_name', 'project_no', 'invoice_no'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'quantity': forms.NumberInput(attrs={'placeholder': 'Enter a number'}),
        }

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity is None:
            raise forms.ValidationError("Quantity is required.")
        return quantity