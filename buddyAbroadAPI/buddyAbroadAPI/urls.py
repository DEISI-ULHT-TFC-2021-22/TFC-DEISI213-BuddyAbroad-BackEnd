from django.urls import path
from . import views as views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views.interestsAPI_view import InterestsAPI
from .views.loginAPI_view import LoginAPI
from .views.translate_view import AwsTranslate
from .views.tripsAPI_view import TripsAPI
from .views.userAPI_view import UsersAPI
from .views.fileUpload_view import FileUpload
from .views.userTripsAPI_view import UserTripsAPI

schema_view = get_schema_view(
    openapi.Info(
        title="Buddy Abroad API",
        default_version="v1",
        description="The Backend of the app Buddy-Abroad",
        contact=openapi.Contact(email="BuddyAbroadDev@buddy.com")
    ),
    public=True,
)
urlpatterns = [
    path('users/', UsersAPI.users_list_create, name='users'),
    path('users/<int:id>', UsersAPI.user_get_update_delete, name='user_get_update_delete'),
    path('interests/', InterestsAPI.get_interests_by_categories, name='get_interests_by_categories'),
    path('signup/', LoginAPI.sign_up, name='sign_up'),
    path('confirmAccount/', LoginAPI.confirm_sign_up, name='confirm_sign_up'),
    path('login/', LoginAPI.login_auth, name='login_auth'),
    path('trips/', TripsAPI.get_trips, name='trips'),
    path('postTrip/', TripsAPI.post_trip, name='post_trip'),
    path('trips/<int:id>', TripsAPI.trip_get_update_delete, name='trip_get_update_delete'),
    path('interestPoints/', TripsAPI.interest_points_list_create, name='interest_points_list_create'),
    path('interestPoints/<int:id>', TripsAPI.interest_point_get_update_delete, name='interest_point_get_update_delete'),
    path('tripInterestPoints/<int:id>', TripsAPI.get_trip_interest_points, name='get_trip_interest_points'),
    path('userTrips/<int:id>', UserTripsAPI.user_trips_get_update_delete, name='user_trips_get_update_delete'),
    path('postUserTrips/', UserTripsAPI.post_user_trips, name='post_user_trips'),
    path('userBookings/<int:id>', UserTripsAPI.get_user_bookings, name='get_user_bookings'),
    path('tripsUserBookings/<int:id>', UserTripsAPI.get_trips_user_bookings, name='get_trips_user_bookings'),
    path('deleteUserFavourites/<int:id>', UserTripsAPI.favourite_delete, name='favourite_delete'),
    path('postUserFavourites/', UserTripsAPI.post_user_favourites, name='post_user_favourites'),
    path('getObjectFavourites/<int:id>', UserTripsAPI.get_object_favourites, name='get_object_favourites'),
    path('getTripsFavourites/<int:id>', UserTripsAPI.get_trips_favourites, name='get_trips_favourites'),
    path('translate/', AwsTranslate.translate, name='translate'),
    path('usersEmail/<str:email>', UsersAPI.get_user_by_email, name='get_user_by_email'),
    path('forgotPassword/', LoginAPI.forgot_password, name='forgot_password'),
    path('confirmForgotPassword/', LoginAPI.confirm_forgot_password, name='confirm_forgot_password'),
    path('changePassword/', LoginAPI.change_password, name='change_password'),
    path('imageUpload/', FileUpload.upload_file, name='upload_file'),
    path('tripSearch/', TripsAPI.trip_search, name='trip_search'),
    path('', UsersAPI.api_root),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name="schema-swagger-ui"),
]

