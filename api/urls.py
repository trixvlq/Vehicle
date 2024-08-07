from django.urls import path
from users.views import RegistrationView, LoginView, LogoutView
from vehicles.views import CarListAddView, CarDetailView

urlpatterns = [
    path('v1/register/', RegistrationView.as_view()),
    path('v1/login/', LoginView.as_view()),
    path('v1/logout/', LogoutView.as_view()),
    path('v1/cars/', CarListAddView.as_view()),
    path('v1/car/<int:id>/', CarDetailView.as_view()),
]
