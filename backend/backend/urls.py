from django.urls import path
from . import views

urlpatterns = [
    path('episode/<int:episode_id>/', views.episode, name='episode'),
    path("search/", views.search, name="search"),
    path("get-unique-values/", views.get_unique_values, name="get_unique_values"),
]
