from django.urls import path
from . import views

app_name = 'contributions'

urlpatterns = [
    path('dashboard/', views.contributor_dashboard, name='dashboard'),
    path('history/', views.contribution_list, name='list'),
    path('<int:id>/', views.contribution_detail, name='detail'),
    path('<int:id>/receipt/', views.contribution_receipt, name='receipt'),
    path('support/<slug:campaign_slug>/', views.support_campaign, name='support'),
    path('review/<int:id>/', views.review_contribution, name='review'),
    path('success/<int:id>/', views.contribution_success, name='success'),
]
