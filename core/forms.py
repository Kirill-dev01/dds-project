from django import forms
from .models import Transaction, Category


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['created_date', 'status', 'type',
                  'category', 'subcategory', 'amount', 'comment']
        widgets = {
            'created_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make fields required as per the task
        self.fields['status'].required = True
        self.fields['type'].required = True
        self.fields['category'].required = True
        self.fields['subcategory'].required = True
        self.fields['amount'].required = True
