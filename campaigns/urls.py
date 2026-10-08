from django.urls import path
from . import views

app_name = 'campaigns'

urlpatterns = [
    path('', views.campaign_list, name='list'),
    path('my-campaigns/', views.my_campaigns, name='my_campaigns'),
    path('create/', views.campaign_create, name='create'),
    path('<slug:slug>/', views.campaign_detail, name='detail'),
    path('<slug:slug>/edit/', views.campaign_edit, name='edit'),
    path('<slug:slug>/contributors/', views.campaign_contributors, name='contributors'),
    path('<slug:slug>/updates/create/', views.campaign_update_create, name='update_create'),
    path('<slug:slug>/favorite/', views.toggle_favorite, name='favorite'),
    path('favorites/', views.favorites_list, name='favorites'),
    path('creator/<str:username>/', views.creator_profile, name='creator_profile'),
    path('<slug:slug>/delete/', views.campaign_delete, name='delete'),
    path('<slug:slug>/milestones/create/', views.milestone_create, name='milestone_create'),
    path('<slug:slug>/milestones/<int:pk>/edit/', views.milestone_edit, name='milestone_edit'),
    path('<slug:slug>/milestones/<int:pk>/delete/', views.milestone_delete, name='milestone_delete'),
    
    # Comments URLs
    path('<slug:slug>/comments/add/', views.comment_add, name='comment_add'),
    path('comments/<int:pk>/reply/', views.comment_reply, name='comment_reply'),
    path('comments/<int:pk>/edit/', views.comment_edit, name='comment_edit'),
    path('comments/<int:pk>/delete/', views.comment_delete, name='comment_delete'),
    path('comments/<int:pk>/pin/', views.comment_pin, name='comment_pin'),
    path('comments/<int:pk>/report/', views.comment_report, name='comment_report'),
    
    # Analytics URL
    path('<slug:slug>/analytics/', views.campaign_analytics, name='analytics'),
]
