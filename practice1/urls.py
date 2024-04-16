from django.contrib import admin
from django.urls import path, include 
from django.contrib import admin
from django.conf import settings  
from django.conf.urls.static import static  
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('demo1.urls')),
    path('users/', include('django.contrib.auth.urls')), 
    path('users/', include('users.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='demo1/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='demo1/logged_out.html'), name='logout'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)