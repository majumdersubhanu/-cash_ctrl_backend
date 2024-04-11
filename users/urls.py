from django.conf.urls.static import static
from django.urls import path

from cash_ctrl import settings
from .views import UserRegistrationView, UserLoginView, UserDetailUpdateView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('user/update/', UserDetailUpdateView.as_view(), name='user-detail-update'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
