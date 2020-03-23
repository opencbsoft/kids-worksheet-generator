from django.contrib import admin
from django.urls import path
from frontend import views

urlpatterns = [
    path('', views.index),
    path('validate/<uuid:uuid>', views.validate_email),
    path('unsubscribe/<uuid:uuid>', views.unsubscribe),
    path('admin/', admin.site.urls),
]
