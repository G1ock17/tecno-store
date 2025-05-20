# forms.py
from django import forms
from .models import Order

from django import forms
from .models import Category


class ProductFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'] = forms.ModelChoiceField(
            queryset=Category.objects.filter(parent__isnull=True),
            required=False,
            label="Основная категория"
        )
        self.fields['subcategory'] = forms.ModelChoiceField(
            queryset=Category.objects.none(),
            required=False,
            label="Подкатегория"
        )

        if 'category' in self.data:
            try:
                parent_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = Category.objects.filter(
                    parent_id=parent_id
                )
            except (ValueError, TypeError):
                pass
