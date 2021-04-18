from django import forms
from django.contrib.auth import get_user_model

from qanda.models import Question, Answer

User = get_user_model()


class QuestionForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        disabled=True,
        widget=forms.HiddenInput
    )

    class Meta:
        model = Question
        fields = ['title', 'question', 'user']


class AnswerForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        disabled=True,
        widget=forms.HiddenInput
    )

    question = forms.ModelChoiceField(
        queryset=Question.objects.all(),
        disabled=True,
        widget=forms.HiddenInput
    )

    class Meta:
        model = Answer
        fields = ['answer', 'user', 'question']


class AnswerAcceptanceForm(forms.ModelForm):
    accepted = forms.BooleanField(
        widget=forms.HiddenInput, required=False
    )

    class Meta:
        model = Answer
        fields = ['accepted', ]
