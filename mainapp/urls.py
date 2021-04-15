from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path('movies/', views.MovieList.as_view(), name='movie_list'),
    path('movies/<int:pk>', views.MovieDetail.as_view(), name='movie_detail'),
    path('movies/<int:movie_id>/vote', views.CreateVote.as_view(),
         name='create_vote'),
    path('movies/<int:movie_id>/vote/<int:pk>', views.UpdateVote.as_view(),
         name='update_vote'),
    path('person/<int:pk>', views.PersonDetail.as_view(), name='PersonDetail'),

]
