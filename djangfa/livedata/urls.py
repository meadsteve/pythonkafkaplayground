from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:run_id>/', views.entry_list, name='entry_list'),
]