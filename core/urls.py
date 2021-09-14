from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/',include('chat.urls')),
    path('auth/', include('dj_rest_auth.urls')),
    path('accounts/login/', auth_views.LoginView.as_view()),
    # path('accounts/logout/', views.logout),
    path('auth/register/', include('dj_rest_auth.registration.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)