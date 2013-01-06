from django import forms

class SearchForm(forms.Form):
	query = forms.CharField(label="Enter a Location", required=True)