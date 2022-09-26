import io
from django.shortcuts import render, redirect
from app.forms import CsvFileForm
import csv
import pydeck
import pandas as pd
from pydeck.types import String
from Pydeck_Django.settings_secret import MAPBOX_API_KEY

# Create your views here.
def index(request):
    return render(request, "index.html")

def HeatMapRender(request):
    if request.method == "POST":
        CsvForm = CsvFileForm(request.POST, request.FILES)
        if CsvForm.is_valid():
            CsvFile = io.TextIOWrapper(request.FILES.get('Csv').file, encoding='utf-8_sig')
            df = pd.read_csv(CsvFile)
            PydeckFunction(df)
            return render(request, 'DeckHtml/xxx.html')

    return render(request, "Form.html", {'FileForm': CsvFileForm})


def PydeckFunction(df):
    layer = pydeck.Layer(
        "HeatmapLayer",
        df,
        opacity=0.3,
        get_position=["lng", "lat"],
        get_weight=["weight"],
        aggregation=String('SUM'),
        colorRange=[[254, 229, 217], [252, 187, 161], [252, 146, 114], [251, 106, 74], [222, 45, 38], [165, 15, 21]],
        radiusPixels=60)

    view_state = pydeck.ViewState(
        longitude=136.90667,
        latitude=35.18028,
        zoom=8,
        min_zoom=5,
        max_zoom=14,
        pitch=0,
        bearing=0)
    r = pydeck.Deck(layers=[layer], initial_view_state=view_state, map_provider="mapbox",
                    api_keys={'mapbox': MAPBOX_API_KEY}, map_style="mapbox://styles/mapbox/dark-v10")
    r.to_html('templates/DeckHtml/xxx.html')