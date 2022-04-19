from django.urls import path
from . import views as views
from .views import *
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
    path('users/', UsersAPI.users_list_create, name='users'),
    path('users/<int:id>', UsersAPI.user_get_update_delete, name='filter_update_user'),
    path('signup/', UsersAPI.sign_up,name='sign_up'),
    path('confirmAccount/', UsersAPI.confirm_sign_up,name='confirm_sign_up'),
    path('login/', UsersAPI.login_auth,name='login_auth'),
    path('trips/', TripsAPI.get_trips, name='trips'),
    path('postTrips/', TripsAPI.post_trip, name='post_trips'),
    path('trips/<int:id>',TripsAPI.trip_get_update_delete, name='trip_get_update_delete'),
    path('interests/', InterestsAPI.as_view()),
    path('translate/', AwsTranslate.translate,name='translate'),
    path('usersEmail/<str:email>', UsersAPI.get_user_by_email, name='get_user_by_email'),
    path('forgotPassword/', UsersAPI.forgot_password,name='forgot_password'),
    path('confirmForgotPassword/', UsersAPI.confirm_forgot_password,name='confirm_forgot_password'),
    path('changePassword/', UsersAPI.change_password,name='change_password'),
    path('', views.api_root),
    path('swagger/',schema_view.with_ui('swagger',cache_timeout=0),name="schema-swagger-ui"),
]