from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import CreateView, DetailView, UpdateView, \
    DayArchiveView, RedirectView

from qanda.forms import QuestionForm, AnswerAcceptanceForm, AnswerForm
from qanda.models import Question, Answer


class AskQuestionView(LoginRequiredMixin, CreateView):
    form_class = QuestionForm
    template_name = 'qanda/ask.html'

    def get_initial(self):
        return {'user': self.request.user.id}

    def form_valid(self, form):
        action = self.request.POST.get('action')
        if action == 'SAVE':
            return super().form_valid(form)
        elif action == 'PREVIEW':
            preview = Question(
                question=form.cleaned_data['question'],
                title=form.cleaned_data['title']
            )
            context = self.get_context_data(preview=preview)
            return self.render_to_response(context=context)
        return HttpResponseBadRequest()


class QuestionDetailView(DetailView):
    model = Question

    ACCEPT_FORM = AnswerAcceptanceForm(initial={'accepted': True})
    REJECT_FORM = AnswerAcceptanceForm(initial={'accepted': False})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {'answer_form': AnswerForm(
                initial={
                    'user': self.request.user.id,
                    'question': self.object.id
                })
            })
        if self.object.can_accept_answer(self.request.user):
            context.update(
                {
                    'accept_form': self.ACCEPT_FORM,
                    'reject_form': self.REJECT_FORM,
                }
            )
        return context


class CreateAnswerView(LoginRequiredMixin, CreateView):
    form_class = AnswerForm
    template_name = 'qanda/create_answer.html'

    def get_initial(self):
        return {'user': self.request.user.id,
                'question': self.get_question().id}

    def get_question(self):
        return Question.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs,
                                        question=self.get_question())

    def get_success_url(self):
        return self.object.question.get_absolute_url()

    def form_valid(self, form):
        action = self.request.POST.get('action')
        if action == 'SAVE':
            return super().form_valid(form)
        elif action == 'PREVIEW':
            context = self.get_context_data(
                preview=form.cleaned_data['answer']
            )
            return self.render_to_response(context=context)
        return HttpResponseBadRequest()


class UpdateAnswerAcceptance(LoginRequiredMixin, UpdateView):
    form_class = AnswerAcceptanceForm
    queryset = Answer.objects.all()

    def get_success_url(self):
        return self.object.question.get_absolute_url()

    def form_invalid(self, form):
        return redirect(self.object.question.get_absolute_url())


class DailyQuestionList(DayArchiveView):
    queryset = Question.objects.all()
    date_field = 'created'
    month_format = '%m'
    allow_empty = True
    # template_name = 'qanda/question_archive_day.html'


class TodayQuestionList(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        today = timezone.now()
        return reverse('qanda:daily_questions', kwargs={
            'year': today.year,
            'month': today.month,
            'day': today.day,
        })
