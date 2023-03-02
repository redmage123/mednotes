from django.urls import path
from .views import FrontPageView, RegisterView, SuccessView, LoginView, LogoutView, DashboardView, ErrorView

urlpatterns = [
    path('', FrontPageView.as_view(), name='front_page'),
    path('register/', RegisterView.as_view(), name='register'),
    path('success/', SuccessView.as_view(), name='success'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('error/', ErrorView.as_view(), name='error'),
]

