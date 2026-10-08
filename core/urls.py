from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('notifications/', views.notifications_list, name='notifications'),
    path('notifications/read/<int:id>/', views.mark_notification_read, name='mark_read'),
    path('notifications/read-all/', views.mark_all_read, name='mark_all_read'),
]
