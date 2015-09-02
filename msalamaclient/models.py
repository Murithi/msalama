from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import smart_unicode
from django.db.models.fields import DateTimeField
from django_pandas.io import read_frame
# Create your models here.

# ============================================================================================================
from django.contrib.auth.models import AbstractUser



class UserProfile(models.Model):
    user = models.OneToOneField(User)
    dateofbirth = models.DateField()
    height = models.CharField(max_length=200)
    weight = models.CharField(max_length=200)
    IDNum = models.CharField(max_length=200)
    Residence = models.CharField(max_length=200)
    PhoneNum = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return smart_unicode(self.IDNum)

    def particulars(self):
        return u'%s %s' % (self.user.first_name, self.user.last_name)
    full_name = property(particulars)


class Vaccine(models.Model):
    vaccinename=models.CharField(max_length=200)
    vaccineIDnum=models.CharField(max_length=150)
    vaccineEdition=models.CharField(max_length=150)
    aboutVaccine=models.CharField(max_length=500)
    childVaccine=models.BooleanField(default=True)
    Lastupdate  =models.DateField(auto_now_add=False, auto_now=True)

    image = models.ImageField(upload_to="images/", null=True)
    vaccineDoseCount = models.CharField(max_length=50)
    timestamp= models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at=models.DateTimeField(auto_now_add=False, auto_now=True)
    def __unicode__(self):
        return smart_unicode(self.vaccinename)


class VaccineDose(models.Model):
    vaccine = models.ForeignKey(Vaccine)
    vaccinedose = models.CharField(max_length=150)
    vaccinedoseday = models.IntegerField()
    available = models.BooleanField()

    def __unicode__(self):
        return smart_unicode(self.vaccinedose)
    
# class VaccineSideEffect(models.Model):
#     vaccine = models.ForeignKey(Vaccine)
#     sideEffectDesc = models.CharField(max_length=80)
#
#     def __unicode__(self):
#         return smart_unicode(self.sideEffectDesc)

class SideEffectbyVaccine(models.Model):
    vaccine = models.ForeignKey(Vaccine)
    sideEffectDesc = models.CharField(max_length=80)

    def __unicode__(self):
        return smart_unicode(self.sideEffectDesc)


class PatientVaccination(models.Model):
    patient = models.ForeignKey(UserProfile)
    creationdate = DateTimeField(auto_now_add=True, auto_now=False)
    patient_vaccine = models.ForeignKey(Vaccine)
    vaccinedose = models.ForeignKey(VaccineDose)
    dateofvaccinereceiption = models.DateField()
    locationofreception = models.CharField(max_length=150, blank=True)
    
    def __unicode__(self):
        return smart_unicode(self.patient)

    def monthly_patients(self):
        dataframe = read_frame(PatientVaccination.objects.all())
        dataframe['month'] = [date.strftime('%B') for date in dataframe['dateofvaccinereceiption']]
        groups = dataframe.groupby('month')['id'].count()
        return groups

    def monthly_vaccine(self):
        dataframe = read_frame(PatientVaccination.objects.all())
        dataframe['month'] = [date.strftime('%B') for date in dataframe['dateofvaccinereceiption']]
        groups = dataframe.groupby(['month', 'patient_vaccine'])['id'].count().reset_index(name='count')
        return groups





class SideEffect(models.Model):
    patient = models.ForeignKey(UserProfile)
    vaccine = models.ForeignKey(Vaccine)
    complaint = models.CharField(max_length=600)

    def __unicode__(self):
        return smart_unicode(self.patient, self.patient)

class Appointment(models.Model):
    firstchoicedate=models.DateTimeField()
    secondchoicedate=models.DateTimeField()
    purposeofvisit=models.CharField(max_length=600)
    patient = models.ForeignKey(UserProfile)

    def __unicode__(self):
        return smart_unicode(self.patient.user.first_name, self.patient.user.last_name)

class Message(models.Model):
    patient= models.ForeignKey(UserProfile)
    messagefrom=models.CharField(max_length=150)
    messageto=models.CharField(max_length=150)
    message=models.CharField(max_length=800)
    messagesubject=models.CharField(max_length=100, blank=True)
    date= models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return smart_unicode(self.patient.user.first_name, self.patient.user.last_name)

class MessageSent(models.Model):
    patient= models.ForeignKey(UserProfile)
    message=models.CharField(max_length=800)
    messagesubject=models.CharField(max_length=100, blank=True)
    date= models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return smart_unicode(self.messagesubject)


