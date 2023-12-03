from django.urls import path
from . import views

app_name = 'ip_ranges'

urlpatterns = [
    path('', views.ip_range_list, name='ip_range_list'),
    path('/create', views.ip_range_create, name='ip_range_create'),
    path('/<int:pk>', views.ip_range_detail, name='ip_range_detail'),
    path('/<int:pk>/update', views.ip_range_update, name='ip_range_update'),
    path('/<int:pk>/delete', views.ip_range_delete, name='ip_range_delete'),
    path('/turn', views.ip_restrict_turn, name='ip_restrict_turn')
]