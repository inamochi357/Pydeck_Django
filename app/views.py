import io
from django.shortcuts import render, redirect
from app.forms import CsvFileForm
import csv
import pydeck
import pandas as pd
from pydeck.types import String
from Pydeck_Django.settings_secret import MAPBOX_API_KEY
from django.shortcuts import redirect


# Create your views here.
def IndexRedirectView(request): #リダイレクトビュー
    return redirect("index")


def index(request): # レイヤーの選択画面を表示
    return render(request, "index.html")


def HeatMapRender(request): #ヒートマップを選択した際のビュー
    if request.method == "POST":    # Postが行われた場合の処理
        CsvForm = CsvFileForm(request.POST, request.FILES)  #フォームを取り出し
        if CsvForm.is_valid():  #バリデーションを行いう
            CsvFile = io.TextIOWrapper(request.FILES.get('Csv').file, encoding='utf-8_sig') #Csvファイルを取り出す
            df = pd.read_csv(CsvFile)   #csvファイルをpandasのデータフレームに
            HeatmapFunction(df) #データフレームを渡しヒートマップのHTMLファイルを作成
            return render(request, 'DeckHtml/xxx.html') #作成したHTMLファイルを表示
    else:   # フォームを表示
        return render(request, "Form.html", {'FileForm': CsvFileForm})


def HeatmapFunction(df):    #ヒートマップを作成
    layer = pydeck.Layer(   #レイヤーについて定義
        "HeatmapLayer",     #ヒートマップレイヤーを指定
        df,                 #データを指定
        opacity=0.3,        #透明度
        get_position=["lng", "lat"],    #データフレームのカラムから座標を設定
        get_weight=["weight"],          #データフレームのカラムから重みを設定
        colorRange=[[254, 229, 217], [252, 187, 161], [252, 146, 114], [251, 106, 74], [222, 45, 38], [165, 15, 21]],   #ヒートマップのカラーを指定
        radiusPixels=60)    #半径を設定

    view_state = pydeck.ViewState(  #初期のマップの状態を指定
        longitude=136.90667,        #初期座標を設定
        latitude=35.18028,
        zoom=8,                     #初期のズーム設定
        min_zoom=5,                 #ズームできる最大最小を設定
        max_zoom=14,
        pitch=0,                    #マップの傾き(ピッチ角)を設定
        bearing=0)                  #東西南北どちらを向いているか角度で指定

    r = pydeck.Deck(layers=[layer], initial_view_state=view_state, map_provider="mapbox",   # APIキーの設定やマップスタイルといったHTMLの設定
                    api_keys={'mapbox': MAPBOX_API_KEY}, map_style="mapbox://styles/mapbox/dark-v10")
    r.to_html('templates/DeckHtml/xxx.html')    #HTMLに書き出し。
