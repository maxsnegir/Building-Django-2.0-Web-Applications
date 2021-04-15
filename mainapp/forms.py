from django import forms
from django.contrib.auth import get_user_model

from .models import Movie, Vote

User = get_user_model()


class VoteForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        widget=forms.HiddenInput,
        queryset=User.objects.all(),
        disabled=True
    )

    movie = forms.ModelChoiceField(
        widget=forms.HiddenInput,
        queryset=Movie.objects.all(),
        disabled=True
    )

    value = forms.ChoiceField(
        label='Vote', widget=forms.RadioSelect, choices=Vote.VALUE_CHOICES,
    )

    class Meta:
        model = Vote
        fields = '__all__'
