from django.urls import path

from planets.views import PlanetView, PlanetViewDetail

urlpatterns = [
    path('planet', PlanetView.as_view()),
    path('planet/<int:pk>', PlanetViewDetail.as_view())
]
