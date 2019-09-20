from .views import *
from django.urls import path, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from blog.views import RegistrationView, UpdateProfileView, ProfileView, CustomLoginView






urlpatterns = [
    path('', IndexView),
    path('blog/', include('blog.urls')),
    path('admin/', admin.site.urls),
    path('accounts/registration/',RegistrationView.as_view(), name="accounts_registration_url"),
    path('accounts/update/',UpdateProfileView.as_view(),name="update_profile_url"),
    path('accounts/login/',CustomLoginView.as_view(),name="login"),
    path('accounts/',include('django.contrib.auth.urls')),
    path('accounts/<str:slug>/',ProfileView.as_view(),name="profile_url"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)