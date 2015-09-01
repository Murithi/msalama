from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from bootstrap3_datetime.widgets import DateTimePicker
from .models import Vaccine, UserProfile, SideEffect, PatientVaccination, Appointment, Message, MessageSent


class SignupForm(UserCreationForm):
    """User Creation form that uses bootrasp CSS"""
    firstname= forms.CharField(label=("First Name"), max_length=120,
                               widget=forms.TextInput({
                                   'class':'form-control',
                                   'placeholder':'Nelson'}))      
     
    lastname= forms.CharField(label=("Last Name"), max_length=120,
                               widget=forms.TextInput({
                                   'class':'form-control',
                                   'placeholder':'Mandela'}))
    username = forms.CharField(label=("Username"), max_length=120,
                               widget=forms.TextInput({
                                   'class':'form-control',
                                   'placeholder':'Username'}))
    email= forms.EmailField(label=("Email Address"), max_length=120,
                               widget=forms.TextInput({
                                   'class':'form-control',
                                   'placeholder':'nmandela@gmail.com'}))
    password1 = forms.CharField(label=("Password"),
                                widget=forms.widgets.PasswordInput({
                                   'class':'form-control',
                                   'placeholder':'Password'}))
    password2 = forms.CharField(label=("Password confirmation"), 
                                widget=forms.widgets.PasswordInput({
                                   'class':'form-control',
                                   'placeholder':'Password (again)'}),
                                help_text=("Enter the same password as above, for verification."))
    
    class Meta:
        model=User
        fields=('firstname', 'lastname', 'username', 'email', 'password1', 'password2')
    
    def clean(self):
        """
        Verifies that the values entered into the password fields match
        NOTE: Errors wil appear in 'non_field_errors()'' because it applies to more than one field.
        """
        cleaned_data=super(SignupForm, self).clean()
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Passwords don't match. Please enter both fields again")
            return self.cleaned_data
        
    def save(self, commit=True):
        user=super(UserCreationForm, self).save(commit=False)
        user.email=self.cleaned_data['email']
        user.username=self.cleaned_data['username']
        user.first_name =self.cleaned_data['firstname']
        user.last_name = self.cleaned_data['lastname']
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    

class UserProfileForm(forms.ModelForm):
    dateofbirth = forms.DateField(widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False}))
    Height= forms.CharField(label=("Height in Centimeters"), max_length=120,
                               widget=forms.TextInput({
                                   'class':'form-control',
                                   'placeholder':'167'})) 
    Weight= forms.CharField(label=("Weight in Kgs"), max_length=120,
                               widget=forms.TextInput({
                                   'class':'form-control',
                                   'placeholder':'67'})) 
    
    IDNum= forms.CharField(label=("ID Number"), max_length=120,
                               widget=forms.TextInput({ 
                                   'class':'form-control',
                                   'placeholder':'ID Number'}))
    Residence= forms.CharField(label=("Place of Residence"), max_length=120, 
                               widget=forms.TextInput({
                                   'class':'form-control',
                                   'placeholder':'Residence'}))
    Phonenum= forms.CharField(label=("Phone Number"), max_length=120,
                               widget=forms.TextInput({
                                   'class':'form-control',
                                   'placeholder':'Phone Number'}))
    
    
    
    
    class Meta:
        model = UserProfile
        fields=('dateofbirth', 'Height', 'Weight', 'IDNum',
                  'Residence', 'Phonenum')
    
class VaccineReportForm(forms.ModelForm):
    Vaccine = forms.ModelChoiceField(queryset=Vaccine.objects.all())
    complaint = forms.CharField(widget=forms.Textarea(attrs={'cols':30, 'rows':15, 'class':'form-control'}))
    
    class Meta:
        model = SideEffect
        fields=('Vaccine', 'complaint')

class VaccineReceivedReportForm(forms.ModelForm):
    dateofvaccinereceiption =  forms.DateField(widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False}))
    locationofreception = forms.CharField(label=("Location of Vaccine Reception"), max_length=120,
                               widget=forms.TextInput({
                                   'class':'form-control',
                                   'placeholder':'KNH'}))
    class Meta:
        model = PatientVaccination
        fields=('dateofvaccinereceiption', 'locationofreception')

class VaccineDoseReportForm(forms.ModelForm):
    patient_vaccine =forms.CharField(label=("Vaccine:"), max_length=120,
                               widget=forms.TextInput({
                                   'class':'form-control',
                                   'placeholder':'Vaccine', 'readonly':'readonly'}))
    vaccinedose = forms.CharField(label=("Vaccine Dose"), max_length=120,
                               widget=forms.TextInput({
                                   'class':'form-control',
                                   'placeholder':'Vaccine Dose',
                                   'readonly':'readonly'
                               }))
    dateofvaccinereceiption =  forms.DateField(widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False}))
    locationofreception = forms.CharField(label=("Location of Vaccine Reception"), max_length=120,
                               widget=forms.TextInput({
                                   'class':'form-control',
                                   'placeholder':'KNH'}))
    class Meta:
        model = PatientVaccination
        fields=('patient_vaccine', 'vaccinedose','dateofvaccinereceiption', 'locationofreception')

class MakeAppointmentForm(forms.ModelForm):

    firstchoicedate=forms.DateTimeField(label=("First Choice Date & Time"), widget=DateTimePicker(options={"format": "YYYY-MM-DD  HH:mm",
                                       "pickTime": True}))
    secondchoicedate=forms.DateTimeField(label=("Alternative Date & Time "), widget=DateTimePicker(options={"format": "YYYY-MM-DD  HH:mm",
                                       "pickTime": True}))
    purposeofvisit= forms.CharField(label=("Appointment Details"), widget=forms.Textarea(attrs={'cols':10, 'rows':5, 'class':'form-control'}))

    class Meta:
        model= Appointment
        fields=('purposeofvisit','firstchoicedate','secondchoicedate')

class MessagesViewForm(forms.ModelForm):

    messagefrom=forms.CharField(max_length=150)
    messageto=forms.CharField(max_length=150)
    message=forms.CharField(max_length=800)

    class Meta:
        model = Message
        exclude=()

class MessageSentForm(forms.ModelForm):
    message=forms.Textarea(attrs={'cols':10, 'rows':5})
    messagesubject= forms.CharField(label=("Message To"), max_length=120, widget=forms.TextInput())

    class Meta:
        model = MessageSent
        exclude=('patient',)

