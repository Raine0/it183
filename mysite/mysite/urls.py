from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from blog import views
from django.contrib.auth import views as auth_views # Import auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('blog/', include('blog.urls')), # Updated include # New URL pattern
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'), # Add login url
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'), # Add logout url
    path('api/', include('api.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

settings.LOGIN_REDIRECT_URL = '/blog/'