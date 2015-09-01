from django.contrib import admin

# Register your models here.
from .models import UserProfile, Vaccine, VaccineDose, PatientVaccination, SideEffect, Appointment, Message, MessageSent, SideEffectbyVaccine


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'IDNum', 'Residence', 'PhoneNum', 'dateofbirth')
    class Meta:
        model=UserProfile

admin.site.register(UserProfile, UserProfileAdmin)


class VaccineAdmin(admin.ModelAdmin):
    list_display = ('vaccineIDnum', 'vaccinename', 'image', 'vaccineEdition', 'vaccineDoseCount', 'Lastupdate', 'aboutVaccine', 'childVaccine')
    list_filter = ('Lastupdate',)
    list_editable = ('vaccineEdition', 'image',  'vaccineDoseCount', 'aboutVaccine', 'childVaccine')
    search_fields = ('vaccinename', 'vaccineEdition')
    can_delete = True

    class Meta:
        model=Vaccine

admin.site.register(Vaccine, VaccineAdmin)


class vaccinedoseAdmin(admin.ModelAdmin):
    list_display = ('vaccine', 'vaccinedose', 'vaccinedoseday', 'available',)
    search_fields = ( 'vaccinedose',)
    list_editable = ('vaccinedose', 'vaccinedoseday','available',)
    class Meta:
        model=VaccineDose

admin.site.register(VaccineDose, vaccinedoseAdmin)


class PatientVaccinationAdmin(admin.ModelAdmin):
    list_display = ('patient', 'creationdate', 'patient_vaccine', 'vaccinedose', 'dateofvaccinereceiption',
                    'locationofreception')

    class Meta:
        model = PatientVaccination

admin.site.register(PatientVaccination, PatientVaccinationAdmin)

class SideEffectAdmin(admin.ModelAdmin):


    class Meta:
        model=SideEffect

admin.site.register(SideEffect, SideEffectAdmin)

class SideEffectbyVaccineAdmin(admin.ModelAdmin):
    list_display = ('vaccine', 'sideEffectDesc')
    class Meta:
        model=SideEffectbyVaccine

admin.site.register(SideEffectbyVaccine, SideEffectbyVaccineAdmin)
class AppointmentAdmin(admin.ModelAdmin):
    class Meta:
        model=Appointment

admin.site.register(Appointment, AppointmentAdmin)

class MessageAdmin(admin.ModelAdmin):
    class Meta:
        model=Message

admin.site.register(Message, MessageAdmin)

class MessageSentAdmin(admin.ModelAdmin):
    class Meta:
        model=MessageSent

admin.site.register(MessageSent, MessageSentAdmin)