from .views import upload_csv, get_filtered_data
from django.urls import path

urlpatterns = [
    path('upload_csv/', upload_csv, name='upload_csv'),
    path('get_filtered_data/', get_filtered_data, name='get_filtered_data'),
]