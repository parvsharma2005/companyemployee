from django.urls import path
from .views import *


urlpatterns = [
    path(
        '',
        companyListCreateView.as_view(),
        name='company-list-create'
    ),

    path(
        'company/<uuid:id>/',
        companyDetailUpdateView.as_view(),
        name='company-detail'
    ),
]