from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('past/', views.past, name='past'),
    path('delete/<list_id>', views.delete, name='delete'),
    # path('login/', views.login, name='login'),
    # path('logout/', views.logout, name='logout'),
]