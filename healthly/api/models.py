from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
class HospitalData(models.Model):
    code = models.CharField(max_length=8, default="", unique=True)
    host = models.CharField(max_length=50, unique=True)
    guest_can_pause = models.BooleanField(null=False, default=False)
    votes_to_skip = models.IntegerField(null=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class HospitalData(models.Model):
    index = models.BigIntegerField(blank=False, null=False, primary_key=True)
    facility_id = models.TextField(db_column='Facility_ID', blank=True, null=False)  # Field name made lowercase.
    facility_name = models.CharField(db_column='Facility_Name', max_length=80, blank=True, null=True)  # Field name made lowercase.
    address = models.TextField(db_column='Address', blank=True, null=True)  # Field name made lowercase.
    city = models.TextField(db_column='City', blank=True, null=True)  # Field name made lowercase.
    state = models.TextField(db_column='State', blank=True, null=True)  # Field name made lowercase.
    zip_code = models.BigIntegerField(db_column='ZIP_Code', blank=True, null=True)  # Field name made lowercase.
    county_name = models.TextField(db_column='County_Name', blank=True, null=True)  # Field name made lowercase.
    phone_number = models.TextField(db_column='Phone_Number', blank=True, null=True)  # Field name made lowercase.
    hospital_type = models.TextField(db_column='Hospital_Type', blank=True, null=True)  # Field name made lowercase.
    hospital_ownership = models.TextField(db_column='Hospital_Ownership', blank=True, null=True)  # Field name made lowercase.
    emergency_services = models.TextField(db_column='Emergency_Services', blank=True, null=True)  # Field name made lowercase.
    meets_criteria_for_promoting_interoperability_of_ehrs = models.TextField(db_column='Meets_criteria_for_promoting_interoperability_of_EHRs', blank=True, null=True)  # Field name made lowercase.
    hospital_overall_rating = models.TextField(db_column='Hospital_Overall_Rating', blank=True, null=True)  # Field name made lowercase.
    mortality_national_comparison = models.TextField(db_column='Mortality_National_Comparison', blank=True, null=True)  # Field name made lowercase.
    safety_of_care_national_comparison = models.TextField(db_column='Safety_of_Care_National_Comparison', blank=True, null=True)  # Field name made lowercase.
    readmission_national_comparison = models.TextField(db_column='Readmission_National_Comparison', blank=True, null=True)  # Field name made lowercase.
    patient_experience_national_comparison = models.TextField(db_column='Patient_Experience_National_Comparison', blank=True, null=True)  # Field name made lowercase.
    effectiveness_of_care_national_comparison = models.TextField(db_column='Effectiveness_of_Care_National_Comparison', blank=True, null=True)  # Field name made lowercase.
    timeliness_of_care_national_comparison = models.TextField(db_column='Timeliness_of_Care_National_Comparison', blank=True, null=True)  # Field name made lowercase.
    efficient_use_of_medical_imaging_national_comparison = models.TextField(db_column='Efficient_Use_of_Medical_Imaging_National_Comparison', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'hospital_data'

    def __str__(self):
        return self.facility_name


class CostData(models.Model):
    # facility_id = models.CharField(db_column='Facility_ID', max_length=225)  # Field name made lowercase.
    facility_model = models.ForeignKey(HospitalData, db_column='Facility_Model', related_name='facility_object', blank=True, null=False, on_delete=models.PROTECT)
    facility_id = models.ForeignKey('HospitalData', db_column='Facility_ID', primary_key=False, blank=True, null=False, on_delete=models.PROTECT)
    procedure_source = models.CharField(db_column='Procedure_Source', max_length=225, blank=True, null=True)  # Field name made lowercase.
    procedure_id = models.CharField(db_column='Procedure_ID', max_length=225)  # Field name made lowercase.
    procedure_cost = models.CharField(db_column='Procedure_Cost', max_length=225, blank=True, null=True)  # Field name made lowercase.
    facility_procedure_id = models.CharField(db_column='Facility_Procedure_ID', primary_key=True, max_length=225)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=225, blank=True, null=True)  # Field name made lowercase.
    year = models.CharField(db_column='Year', max_length=45)  # Field name made lowercase.
    index = models.CharField(max_length=225, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cost_data'
        unique_together = (('facility_id', 'facility_procedure_id', 'procedure_id', 'year'),)
    
    def __str__(self):
        return self.description


class Procedure(models.Model):
    submission_id = models.BigIntegerField(primary_key=True, db_column='submission_id')
    user = models.ForeignKey(User, db_column='user', blank=True, null=True, on_delete=models.CASCADE)
    hospital = models.ForeignKey(HospitalData, db_column='hospital', blank=True, null=True, on_delete=models.CASCADE)
    cost = models.ForeignKey(CostData, db_column='cost', blank=True, null=True, on_delete=models.CASCADE)
    insurance_provider = models.CharField(max_length=100, db_column='insurance_provider', blank=True, null=True,)
    insurance_subplan = models.CharField(max_length=100, db_column='insurance_subplan', blank=True, null=True,)
    procedure_cost = models.FloatField(db_column='procedure_cost')
    timestamp = models.DateTimeField(default=timezone.now, db_column='timestamp')

    class Meta:
        ordering = ['-timestamp']
        db_table = 'procedure_submissions'
