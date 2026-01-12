from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/', views.catalog_view, name='catalog'),
    path('catalog/load-more/', views.load_more_cars, name='load_more_cars'),
    path('country/<str:country_code>/', views.country_view, name='country'),
    path('car/<int:pk>/', views.car_detail, name='car_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]

