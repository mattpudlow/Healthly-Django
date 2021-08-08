from django.urls import path, include
from .views import HospitalDataView, CustomAuthToken, is_user_authenticated
from .views import (
    HospitalDataViewSet, CostDataViewSet, ProcedureViewSet,
    AllHospitalsView, AllCostDataView, get_hospital_by_id
)
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('procedure', ProcedureViewSet)
router.register('cost-data', CostDataViewSet)
router.register('', HospitalDataViewSet)


urlpatterns = [
    path('hospitaldata', HospitalDataView.as_view()),
    path('register/', include('rest_auth.registration.urls')),
    path('token-obtain/', CustomAuthToken.as_view(), name="token-auth"),
    path('is-authenticated/', is_user_authenticated, name="is-authenticated"),
    path('', include(router.urls)),
    path('cost/all-cost-data/', AllCostDataView.as_view()),
    path('hospitals/all-hospitals/', AllHospitalsView.as_view()),
    path('hospitals/get-hospital/<int:id>/', get_hospital_by_id)
]
