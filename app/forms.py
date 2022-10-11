from django import forms

class HeatmapCSVForm(forms.Form):
    Csv = forms.FileField()


class GeojsonFileForm(forms.Form):
    Geojson = forms.FileField()