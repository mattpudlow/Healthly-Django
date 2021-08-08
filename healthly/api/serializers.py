from rest_framework import serializers
from .models import HospitalData
import rest_framework_filters as filters
from .models import CostData, HospitalData, Procedure

class HospitalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalData
        fields = (
        'id', 
        'code', 
        'host', 
        'guest_can_pause', 
        'votes_to_skip', 
        'created_at'
        )


class HospitalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalData
        fields = ('index', 'facility_name', 'city', 'state', 'zip_code')
        read_only_fields = fields


class CostDataSerializer(serializers.ModelSerializer):
    #facility_iden = serializers.ReadOnlyField(source='hospital_data.facility_id', read_only=True)
    cost_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = CostData
        fields = (
            'index',
            'cost_count',
            'facility_id',
            'facility_procedure_id',
            'procedure_cost',
            'description',
            )
        read_only_fields = fields


class ProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedure
        fields = '__all__'


class HospitalDataFilter(filters.FilterSet):
    class Meta:
        model = HospitalData
        fields = {
            'facility_id': ['exact'], 'facility_name': ['icontains'], 
            'city': ['icontains'], 'state':  ['istartswith'], 'zip_code': ['startswith']
        } 


class CostDataFilter(filters.FilterSet):
    class Meta:
        model = CostData
        fields = {
           'description': ['icontains'], 'procedure_cost': ['icontains']
        } 


