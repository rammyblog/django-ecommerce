from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('payment/<int:order_id>/', views.payment_process_again, name='process_again'),
    path('process/', views.payment_process, name='process'),
    
    path('done/<int:order_id>/', views.payment_done, name='done'),
    path('canceled/<int:order_id>/', views.payment_canceled, name='canceled'),
]