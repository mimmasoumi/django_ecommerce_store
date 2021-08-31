from django.urls import path
from .views import LoginView, LogoutView, RegisterView

app_name = 'account'

urlpatterns = [
    path('login/', LoginView.as_view(), ),
    path('logout/', LogoutView.as_view()),
    path('register/', RegisterView.as_view())
]
