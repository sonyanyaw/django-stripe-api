from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main'),
    path('item/<int:id>/', views.item_details_view, name='item-detail'),
    path('buy/<int:id>/', views.checkout_session_view, name='buy-item'),

    path('order/<int:id>/', views.order_detail_view, name='order-detail'),
    path('order/<int:id>/buy/', views.order_checkout_view, name='buy-order'),
    
    path('success/', views.success_view, name='success'),
    path('cancel/', views.cancel_view, name='cancel'),
]
