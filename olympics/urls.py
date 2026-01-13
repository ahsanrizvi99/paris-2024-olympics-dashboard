from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('athletes/', views.athletes_list, name='athletes_list'),
    path('athletes/visualize/graph/', views.athletes_by_country_graph, name='athletes_by_country_graph'),
    path('athletes/visualization/', views.athletes_visualization, name='athletes_visualization'),
    path('events/', views.events_list, name='events_list'),
    path('events/visualization/', views.events_visualization, name='events_visualization'),
    path('medals/', views.medals_list, name='medals_list'),
    path('medals/visualization/', views.medals_visualization, name='medals_visualization'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('export/athletes/csv/', views.export_athletes_csv, name='export_athletes_csv'),
    path('export/events/csv/', views.export_events_csv, name='export_events_csv'),
    path('export/medals/csv/', views.export_medals_csv, name='export_medals_csv'),
    path('export/athletes/pdf/', views.export_athletes_pdf, name='export_athletes_pdf'),
    path('export/events/pdf/', views.export_events_pdf, name='export_events_pdf'),
    path('export/medals/pdf/', views.export_medals_pdf, name='export_medals_pdf'),
    path('export/athletes/pdf/', views.export_athletes_pdf, name='export_athletes_pdf'),
    path('export/events/pdf/', views.export_events_pdf, name='export_events_pdf'),
    path('export/medals/pdf/', views.export_medals_pdf, name='export_medals_pdf'),
]
 