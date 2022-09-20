from django import forms

class CsvFileForm(forms.Form):
    Csv = forms.FileField()
