from django import forms

class CsvFileForm(forms.Form):
    Csv = forms.FileField() #csvファイルを渡すフォームを作成
