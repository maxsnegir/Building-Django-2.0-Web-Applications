from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic

from .forms import VoteForm, MovieImageForm
from .models import Movie, Person, Vote


class MovieList(generic.ListView):
    model = Movie
    paginate_by = 1


class MovieDetail(generic.DetailView):
    model = Movie
    queryset = Movie.objects.all_with_related_persons_and_scores()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:

            vote = Vote.objects.get_vote_or_unsaved_blank_vote(
                movie=self.object,
                user=self.request.user)
            if vote.id:
                vote_form_url = reverse('main:update_vote', kwargs={
                    'movie_id': self.object.id, 'pk': vote.id
                })
            else:
                vote_form_url = reverse('main:create_vote', kwargs={
                    'movie_id': self.object.id
                })
            vote_form = VoteForm(instance=vote)
            context['vote_form'] = vote_form
            context['vote_form_url'] = vote_form_url
            context['image_form'] = MovieImageForm()

        return context


class PersonDetail(generic.DetailView):
    model = Person
    queryset = Person.objects.all_with_prefetch_movies()


class CreateVote(LoginRequiredMixin, generic.CreateView):
    form_class = VoteForm

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user.id
        initial['movie'] = self.kwargs['movie_id']
        return initial

    def get_success_url(self):
        movie_id = self.object.movie.id
        return reverse('main:movie_detail', kwargs={'pk': movie_id})

    def render_to_response(self, context, **response_kwargs):
        movie_id = context['object'].id
        movie_detail = reverse('main:movie_detail', kwargs={'pk': movie_id})
        return redirect(movie_detail)


class UpdateVote(LoginRequiredMixin, generic.UpdateView):
    form_class = VoteForm
    queryset = Vote.objects.all()

    def get_object(self, queryset=None):
        vote = super().get_object(queryset)
        user = self.request.user
        if vote.user != user:
            raise PermissionDenied('cannot change another user vote')
        return vote

    def get_success_url(self):
        movie_id = self.object.movie.id
        return reverse('main:movie_detail', kwargs={'pk': movie_id})

    def render_to_response(self, context, **response_kwargs):
        movie_id = context['object'].id
        movie_detail_url = reverse('main:movie_detail',
                                   kwargs={'pk': movie_id})
        return redirect(movie_detail_url)


class MovieImageUploadView(LoginRequiredMixin, generic.CreateView):
    form_class = MovieImageForm

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user
        initial['movie'] = self.kwargs['movie_id']
        return initial

    def get_success_url(self):
        movie_id = self.kwargs['movie_id']
        movie_detail_url = reverse('main:movie_detail',
                                   kwargs={'pk': movie_id})
        return movie_detail_url

    def render_to_response(self, context, **response_kwargs):
        movie_id = self.kwargs['movie_id']
        movie_detail_url = reverse('main:movie_detail',
                                   kwargs={'pk': movie_id})
        return redirect(movie_detail_url)


class TopMovies(generic.ListView):
    model = Movie
    queryset = Movie.objects.top_movies(limit=10)
    template_name = 'mainapp/top_movies_list.html'