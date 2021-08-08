from django.shortcuts import render
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny 
from .serializers import HospitalDataSerializer
from .models import HospitalData
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import pagination, generics
from rest_framework.decorators import api_view, permission_classes, action

from .models import CostData, HospitalData, Procedure
from .serializers import (
    CostDataSerializer, HospitalDataSerializer, ProcedureSerializer,
    CostDataFilter, HospitalDataFilter
)

# Create your views here.
class HospitalDataView(generics.ListAPIView):
    queryset = HospitalData.objects.all()
    serializer_class = HospitalDataSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def is_user_authenticated(request):
    user = request.user

    if user.is_authenticated == False:
        allow = False
    else:
        allow = True

    return Response({'is_authenticated': allow})
    

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class CustomPagination(pagination.PageNumberPagination):
    # Changed from 1,000 - this only affects the amount of
    # auto-suggest lines you receive from the search bar
    page_size = 10

    def get_paginated_response(self, data):
        return Response({
            'links': {
               'next': self.get_next_link(),
               'previous': self.get_previous_link()
            },
            #'count': self.page.paginator.count,
            #'total_pages': self.page.paginator.num_pages,
            'results': data
        })


class HospitalDataViewSet(viewsets.ModelViewSet):
    queryset = HospitalData.objects.all()
    serializer_class = HospitalDataSerializer
    filter_class = HospitalDataFilter


@api_view(('GET',))
def get_hospital_by_id(request, id):
    try:
        hospital = HospitalData.objects.get(facility_id=id)
    except:
        return Response('No hospital found')
    serializer = HospitalDataSerializer(hospital)

    return Response(serializer.data)


class AllHospitalsView(generics.ListAPIView):
    queryset = HospitalData.objects.all()
    serializer_class = HospitalDataSerializer
    pagination_class = CustomPagination


class CostDataViewSet(viewsets.ModelViewSet):
    queryset = CostData.objects.all()
    serializer_class = CostDataSerializer
    filter_class = CostDataFilter


class AllCostDataView(generics.ListAPIView):
    queryset = CostData.objects.all()
    serializer_class = CostDataSerializer
    pagination_class = CustomPagination
    filter_class = CostDataFilter


class ProcedureViewSet(viewsets.ModelViewSet):
    queryset = Procedure.objects.all()
    serializer_class = ProcedureSerializer

    def create(self, request):
        user = request.user
        params = request.data

        description = params['cost']
        hospital = params['hospital']
        procedure_cost = float(params['procedure_cost'])
        insurance_provider = params['insurance_provider']
        insurance_subplan = params['insurance_subplan']

        cost_object = CostData.objects.filter(description=description)[0]
        hospital_object = HospitalData.objects.filter(facility_name=hospital)[0]
        objects_exists = Procedure.objects.all().count() != 0

        if objects_exists:
            procedure_id = Procedure.objects.first().submission_id + 1
        else:
            procedure_id = 0

        procedure, created = Procedure.objects.get_or_create(
            submission_id=procedure_id,
            user=user, hospital=hospital_object, cost=cost_object, procedure_cost=procedure_cost,
            insurance_provider=insurance_provider, insurance_subplan=insurance_subplan
        )
        procedure.save()

        serializer = ProcedureSerializer(procedure)
        return Response(serializer.data)
