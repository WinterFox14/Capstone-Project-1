from django.urls import path
from .views import *

urlpatterns = [
    path('api/energy/send/', EnergyInputAPI.as_view()),
    path('api/blockchain/', BlockchainExplorerAPI.as_view()),
    path('api/chain/validate/', ChainValidateAPI.as_view()),
    path('api/user/dashboard/', UserEnergyDashboardAPI.as_view()),
]
