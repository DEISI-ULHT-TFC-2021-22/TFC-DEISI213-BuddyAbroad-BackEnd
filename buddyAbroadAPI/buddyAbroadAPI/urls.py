from django.urls import path
from . import views as views
from .views import *
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title = "Buddy Abroad API",
        default_version="v1",
        description="The Backend of the app Buddy-Abroad",
        contact=openapi.Contact(email="BuddyAbroadDev@buddy.com")
    ),
    public=True,
)
urlpatterns = [
    path('users/',Users.as_view(),name='users'),
    path('createUser/',Users.create_user,name='createUser'),
    path('confirmAccount/',Users.confirm_sign_up,name='confirm_sign_up'),
    path('login/',Users.login_auth,name='loginAuth'),
    path('trips/',TripsAPI.get,name='trips'),
    path('postTrips/',TripsAPI.postTrip,name='post_trips'),
    path('postTripsDetails/',TripsAPI.postTripDetails,name='post_trips_details'),
    path('getTrip/<int:id>',TripsAPI.get_trip_by_id),
    path('', views.api_root),
    path('swagger/',schema_view.with_ui('swagger',cache_timeout=0),name="schema-swagger-ui"),
]