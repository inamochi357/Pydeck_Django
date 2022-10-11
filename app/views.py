import io
from django.shortcuts import render, redirect
from app.forms import HeatmapCSVForm, GeojsonFileForm
import csv
import pydeck
import pandas as pd
from pydeck.types import String
from Pydeck_Django.settings_secret import MAPBOX_API_KEY
from django.shortcuts import redirect
import json


# Create your views here.
def IndexRedirectView(request):
    return redirect("index")


def index(request):
    return render(request, "index.html")


def HeatMapRenderView(request):
    if request.method == "POST":
        CsvForm = HeatmapCSVForm(request.POST, request.FILES)
        if CsvForm.is_valid():
            CsvFile = io.TextIOWrapper(request.FILES.get('Csv').file, encoding='utf-8_sig')
            df = pd.read_csv(CsvFile)
            HeatmapFunction(df)
            return render(request, 'DeckHtml/HeatmapLayer/xxx.html')
    else:
        return render(request, "Form.html", {'FileForm': HeatmapCSVForm})


def HeatmapFunction(df):
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
    r.to_html('templates/DeckHtml/HeatmapLayer/xxx.html')


def GeojsonRenderView(request):
    if request.method == "POST":
        GeojsonForm = GeojsonFileForm(request.POST, request.FILES)
        if GeojsonForm.is_valid():
            GeojsonData = request.FILES.get('Geojson')
            JsonData = json.load(GeojsonData)
            GeojsonFunction(JsonData)
            return render(request, 'DeckHtml/GeojsonLayer/xxx.html')

    else:
        return render(request, "Form.html", {'FileForm': GeojsonFileForm})


def GeojsonFunction(JsonData):
    Layer = pydeck.Layer(
        'GeoJsonLayer',
        JsonData,
        stroked=False,
        filled=True,
        getPointRadius=40,
        lineWidthMinPixels=4,
        get_line_color=[255, 255, 255],
        pickable=True
    )
    view_state = pydeck.ViewState(
        longitude=136.90667,
        latitude=35.18028,
        zoom=8,
        min_zoom=5,
        max_zoom=14,
        pitch=0,
        bearing=0)

    r = pydeck.Deck(
        layers = [Layer], initial_view_state = view_state, map_provider="mapbox",
                    api_keys={'mapbox': MAPBOX_API_KEY}, map_style="mapbox://styles/mapbox/dark-v10"
    )

    r.to_html('templates/DeckHtml/GeojsonLayer/xxx.html')