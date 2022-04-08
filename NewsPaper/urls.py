from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    #path('news/', include('news.urls')),  не удалил на случай изменений в будущем
    path('', include('news.urls')),
    path('auth/', include('allauth.urls')),
    path('accounts/', include('allauth.urls')),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    #path('appointment/', include('appointment.urls')),
    path('appointments/', include(('appointment.urls', 'appointments'), namespace='appointments')),
    ]

