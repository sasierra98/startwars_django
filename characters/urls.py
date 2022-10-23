from django.urls import path

from characters.views import PeopleView, PeopleViewDetail

urlpatterns = [
    path('people', PeopleView.as_view()),
    path('people/<int:pk>', PeopleViewDetail.as_view())
]
