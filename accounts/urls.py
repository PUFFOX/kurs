from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),  # ← нова сторінка
    path('edit_profile/', views.edit_profile_view, name='edit_profile'),
    path('kursant/<int:user_id>/', views.kursant_detail_view, name='kursant_detail'),
    path('my-group/', views.my_group_view, name='my_group'),
    path('journalist/', views.journalist_dashboard, name='journalist_dashboard'),
    path('commander/', views.commander_dashboard, name='commander_dashboard'),
    path('chief/', views.chief_dashboard, name='chief_dashboard'),
    path('kursant/', views.kursant_dashboard, name='kursant_dashboard'),


    

]
