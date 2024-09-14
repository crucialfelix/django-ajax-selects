from django import forms
from django.shortcuts import render

from ajax_select.fields import AutoCompleteField


class SearchForm(forms.Form):
    q = AutoCompleteField(
        "cliche",
        required=True,
        help_text="Enter a few words, search using autocomplete...",
        label="Select a cliché about cats",
        attrs={"size": 100},
    )


def search_form(request):
    context = {}
    if "q" in request.GET:
        context["entered"] = request.GET.get("q")
    initial = {"q": "out of the bag"}
    form = SearchForm(initial=initial)
    context["form"] = form
    return render(request, "example/search_form.html", context)
