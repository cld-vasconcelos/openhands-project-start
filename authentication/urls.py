from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (CustomTokenObtainPairView, LogoutView, PasswordResetConfirmView,
                   PasswordResetView, SocialLoginView, UserViewSet)

router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/confirm/<str:uid>/<str:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('social-login/', SocialLoginView.as_view(), name='social_login'),
] + router.urls
