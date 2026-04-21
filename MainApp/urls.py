from django.urls import path
from . import views

# ⚠️ Common mistake: putting 'skill/new/' AFTER 'skill/<int:pk>/' would cause Django
# to try to match "new" as a pk integer and fail. Always put specific paths before dynamic ones.
urlpatterns = [
    path('', views.landing, name='landing'),
    path('skills/', views.SkillListView.as_view(), name='skill-list'),
    path('skill/new/', views.SkillCreateView.as_view(), name='skill-create'),
    path('skill/<int:pk>/', views.SkillDetailView.as_view(), name='skill-detail'),
    path('skill/<int:pk>/edit/', views.SkillUpdateView.as_view(), name='skill-update'),
    path('skill/<int:pk>/delete/', views.SkillDeleteView.as_view(), name='skill-delete'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('register/', views.register, name='register'),
    path('user/<str:username>/', views.user_profile, name='user-profile'),
    path('skill/<int:pk>/book/', views.book_appointment, name='book-appointment'),
    path('appointments/', views.appointments, name='appointments'),
    path('appointments/<int:pk>/<str:action>/', views.appointment_action, name='appointment-action'),
    path('notifications/', views.notifications, name='notifications'),
]
