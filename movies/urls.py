from django.urls import path

from movies.views import MovieView, MovieViewDetail

urlpatterns = [
    path('movie', MovieView.as_view()),
    path('movie/<int:pk>', MovieViewDetail.as_view())
]
