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
    path('users/',UsersAPI.users_list_create_delete,name='users'),
    path('users/<int:id>', UsersAPI.filter_updateUser),
    path('signup/',UsersAPI.sign_up,name='sign_up'),
    path('confirmAccount/',UsersAPI.confirm_sign_up,name='confirm_sign_up'),
    path('login/',UsersAPI.login_auth,name='loginAuth'),
    path('trips/',TripsAPI.get,name='trips'),
    path('postTrips/',TripsAPI.postTrip,name='post_trips'),
    path('getTrip/<int:id>',TripsAPI.get_trip_by_id),
    path('interests/',InterestsAPI.as_view()),
    path('', views.api_root),
    path('swagger/',schema_view.with_ui('swagger',cache_timeout=0),name="schema-swagger-ui"),
]