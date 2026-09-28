from django.urls import path, include
from shirts import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404

urlpatterns = [
    path('', views.home, name='home'),
    
    #Error handlers
    path('handler404/', views.handler404),
    path('handler500/', views.handler500),
    
    #product detail
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
