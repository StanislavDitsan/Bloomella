from django.urls import path
from . import views

urlpatterns = [
    path('', views.support_ticket, name='support_ticket'),
    path('success/',
         views.support_ticket_success,
         name='support_ticket_success'),
]
