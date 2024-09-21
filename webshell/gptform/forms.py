import pandas as pd
from django import forms
from django.contrib.auth.forms import AuthenticationForm

def generate_form_from_csv(file_path):
    class DynamicForm(forms.Form):
        pass
    
    df = pd.read_excel(file_path, header=0)
    for _, row in df.iterrows():
        field_name = row['Name']
        field_type = row['Type']
        prefill = row['Prefil'] if not pd.isnull(row['Prefil']) else ""
        if field_type == 'Single Text':
            field = forms.CharField(initial=prefill)
        elif field_type == 'Date':
            field = forms.DateField(initial=prefill)
        elif field_type == 'Multi Text':
            field = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 20}), initial=prefill)
        else:
            continue
        DynamicForm.base_fields[field_name] = field

    return DynamicForm