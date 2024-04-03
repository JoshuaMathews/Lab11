from django.urls import path
from . import views

urlpatterns = [
    path('', views.place_list, name='place_list'), # anything that is not defined will be redirected to this.
    path('visited', views.places_visited, name='visited'),# /visited will redirect to the user's visited page
    path('place/<int:place_pk>/was_visited/', views.place_was_visited, name='place_was_visited'), # set places to visited and let django deal with 90% of the effort.
    path('place/<int:place_pk>', views.place_details, name='place_details'), # set places to visited and let django deal with 90% of the effort.
    path('place/<int:place_pk>/delete', views.delete_place, name='delete_place')
]