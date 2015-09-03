import  datetime
from django.http import JsonResponse
from django.template import RequestContext
from django.contrib import messages
from django.views.generic import ListView, FormView, View
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.db.models import Q
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from forms import SignupForm, UserProfileForm, VaccineReportForm, VaccineReceivedReportForm, MakeAppointmentForm, MessageSentForm, VaccineDoseReportForm
from models import UserProfile, PatientVaccination, VaccineDose, Vaccine, Appointment, Message, SideEffectbyVaccine


class GraphDataView(View):
    def get(self, request, *args, **kwargs):

        data_type = request.GET.get('type')
        if data_type == 'patients_graph':
            groups = PatientVaccination().monthly_patients()

            availaible_months = groups.keys()
            data = []

            months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
            for month in months:
                if month in availaible_months:
                    data.append(groups[month])
                else:
                    data.append(0)

            data = [{
                'name': 'Recipient',
                'data': ['Jan', 'Feb', 'Mar', 'April', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
            }, {
                'name': 'Number of Patients',
                'data': data
            }]

        elif data_type == 'vaccine_graph':
            groups = PatientVaccination().monthly_vaccine()

            data = []

            months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

            vaccine_dict = {}
            for vaccine in Vaccine.objects.all():
                vaccine_dict[vaccine.vaccinename] = []

            for month in months:
                for vaccine in vaccine_dict:
                    if not groups[(groups.month == month) & (groups.patient_vaccine == vaccine)]['count'].empty:
                        vaccine_dict[vaccine].append(int(groups[(groups.month == month) & (groups.patient_vaccine == vaccine)]['count']))
                    else:
                        vaccine_dict[vaccine].append(0)

            for key, value in vaccine_dict.iteritems():
                data.append({'name': key, 'data': value})

        else:
            data = []

        return JsonResponse(data, safe=False)


# Create your views here.
def login(request):
    #assert False, request
    c={}
    c.update(csrf(request))
    return render_to_response('login.html', c)


def auth_view(request):
    username=request.POST.get('username','')
    password=request.POST.get('password','')

    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
        try:
            p = UserProfile.objects.get(user__username=request.POST['username'])
        except UserProfile.DoesNotExist:
            return HttpResponseRedirect('userprofile')
        
        if p.IDNum is not None:
            request.session['user_sysID']=p.IDNum
            return HttpResponseRedirect('loggedin.html')
        else:
            return HttpResponseRedirect('userprofile')
    
        
    else:
        return HttpResponseRedirect('invalid_login.html')

def loggedin(request):
    return render_to_response('loggedin.html', {'full_name': request.session['user_sysID']})

def invalid_login(request):
    return render_to_response('invalid_login.html')

def logout(request):
    auth.logout(request)
    return render_to_response('logout.html')

class signup(FormView):
    form_class = SignupForm
    template_name='signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render_to_response(self.template_name, {'form':form}, context_instance=RequestContext(request))

    def form_valid(self, form):
        form.instance.firstname = form.cleaned_data.get('firstname')
        form.instance.lastname = form.cleaned_data.get('lastname')
        form.instance.username = form.cleaned_data.get('username')
        form.instance.email = form.cleaned_data.get('email')
        form.instance.password1 = form.cleaned_data.get('password1')
        form.save()
        return HttpResponseRedirect(reverse('signup_success'))

def signupold(request):
    if request.method=="POST":
        #assert False, request
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('signup_success'))
            # return HttpResponseRedirect('signup_success')
        else:
            args={}
            args.update(csrf(request))
            args['form'] = SignupForm()
            return render_to_response('signup.html', args)
    else:
        args={}
        args.update(csrf(request))
        args['form'] = SignupForm()
        return render_to_response('signup.html', args)


def signup_success(request):
    return render_to_response('signup_success.html')

def vaccines(request):
    return render_to_response('vaccines.html')


def childvaccines(request):
    vaccines = Vaccine.objects.all()

    return render_to_response('childvaccines.html', {'allvaccines':vaccines})

def updatevaccine(request):

        vacid = request.GET['vaccine']
        vacdoseid= request.GET['dose']

        count =PatientVaccination.objects.filter(patient__IDNum=request.session['user_sysID']).filter(patient_vaccine__id=vacid).filter(vaccinedose__vaccinedose=request.GET['dose']).count()
        if count >0:
            vaccinations = PatientVaccination.objects.filter(patient__IDNum=request.session['user_sysID']).filter(vaccinedose__vaccinedose=request.GET['dose'])

        else:
            print request.GET['dose']
            print VaccineDose.objects.filter(vaccine__id=request.GET['vaccine']).filter(vaccinedose=request.GET['dose'])
            vaccinations= VaccineDose.objects.filter(vaccine__id=request.GET['vaccine']).filter(vaccinedose=request.GET['dose'])
            vaccination = VaccineDose.objects.get(Q(vaccine__id=request.GET['vaccine']) & Q(vaccinedose=request.GET['dose']))

        print vaccinations[0]
        vaccination= vaccinations[0]
        vaccinated= count
        args={}
        args.update(csrf(request))
        args['vaccinated'] = vaccinated
        args['vaccination'] = vaccination

        return render_to_response('updatevaccine.html', args)

def updatevaccineview(request):
    patient_vaccine=Vaccine.objects.get(vaccinename=request.POST.get('patient_vaccine',''))
    vaccinedose=VaccineDose.objects.get(vaccinedose=request.POST.get('vaccinedose',''))
    locationofreception=request.POST.get('locationofreception','')
    dateofvaccinereceiption=request.POST.get('dateofvaccinereceiption','')

    PatientVaccination.objects.create(patient_vaccine=patient_vaccine, vaccinedose=vaccinedose,
                                       locationofreception = locationofreception, dateofvaccinereceiption= dateofvaccinereceiption,
                                       patient = request.user.userprofile)

    # return HttpResponseRedirect('vaccinelist')
    print patient_vaccine.id
    return HttpResponseRedirect('%s?id=%s' % (reverse('vaccinelist'), patient_vaccine.id))
    # return HttpResponseRedirect(reverse('vaccinelist', kwargs={'id':patient_vaccine.id}))



def vaccinelist(request):
    vacid = request.GET['id']

    thisvaccine = Vaccine.objects.get(id=vacid)
    #Get count of doses
    vaccdosescount = VaccineDose.objects.filter(vaccine__id=vacid).count()
    print request.session['user_sysID']
    count =PatientVaccination.objects.filter(patient__IDNum=request.session['user_sysID']).filter(patient_vaccine__id=vacid).count()
    # PatientVaccination.objects.filter(patient__IDNum=24683728).filter(patient_vaccine__id=vacid).count()
    #PERCENTAGE DOSES RECIEVED
    percentagevaccinated=0

    if count:
        if vaccdosescount:
            percentagevaccinated= int(count/float(vaccdosescount)*100)

    #ALL DOSES REQUIRED
    poliovaccinedoses  =VaccineDose.objects.filter(vaccine__id=vacid).order_by("vaccinedose")

    #DOSES RECIEVED SO FAR
    poliovaccinedosesrecieved =PatientVaccination.objects.filter(patient__IDNum=request.session['user_sysID']).filter(patient_vaccine__id=vacid)
    poliovaccinedosesrecieved_ids = [vaccine.vaccinedose.id for vaccine in poliovaccinedosesrecieved]

    lsrecieved=[]
    lspending=[]
    lista= []



    pending = [vaccine for vaccine in poliovaccinedoses if vaccine.id not in poliovaccinedosesrecieved_ids]
    received = [vaccine for vaccine in poliovaccinedoses if vaccine.id in poliovaccinedosesrecieved_ids]
    sideeffects= SideEffectbyVaccine.objects.filter(vaccine__id=vacid)


    return render_to_response('vaccinelist.html', {'percentagedose': percentagevaccinated, 'vaccinesrecieved': received, 'vaccinesrequired': pending, 'mainvaccine': thisvaccine, 'sideeffects': sideeffects, 'alldoses': poliovaccinedoses})


def polio(request):


    #Get count of doses 
    vaccdosescount = VaccineDose.objects.filter(vaccine__vaccinename='Polio Sabin Vaccine').count()
    #GET NO OF DOSES RECIEVED
    count =PatientVaccination.objects.filter(patient__IDNum=request.session['user_sysID']).filter(patient_vaccine__vaccinename='Polio Sabin Vaccine').count()
    #PERCENTAGE DOSES RECIEVED
    percentagevaccinated=0

    if count:
        if vaccdosescount:
            percentagevaccinated= int(count/float(vaccdosescount)*100)


    #ALL DOSES REQUIRED
    poliovaccinedoses  =VaccineDose.objects.filter(vaccine__vaccinename='Polio Sabin Vaccine').order_by("vaccinedose")
    #DOSES RECIEVED SO FAR
    poliovaccinedosesrecieved =PatientVaccination.objects.filter(patient__IDNum=request.session['user_sysID']).filter(patient_vaccine__vaccinename='Polio Sabin Vaccine')
    poliovaccinedosesrecieved_ids = [vaccine.vaccinedose.id for vaccine in poliovaccinedosesrecieved]


    lsrecieved=[]
    lspending=[]
    lista= []



    pending = [vaccine for vaccine in poliovaccinedoses if vaccine.id not in poliovaccinedosesrecieved_ids]
    received = [vaccine for vaccine in poliovaccinedoses if vaccine.id in poliovaccinedosesrecieved_ids]


    return render_to_response('polio.html', {'percentagedose': percentagevaccinated, 'vaccinesrecieved': received, 'vaccinesrequired': pending})


    


class LoggedInUserProfile(FormView):
    form_class = UserProfileForm
    template_name='userprofile.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render_to_response(self.template_name, {'form':form}, context_instance=RequestContext(request))

    def form_valid(self, form):
        form.instance.dateofbirth = form.cleaned_data.get('dateofbirth')
        form.instance.Height = form.cleaned_data.get('Height')
        form.instance.Weight = form.cleaned_data.get('Weight')
        form.instance.IDNum = form.cleaned_data.get('IDNum')
        form.instance.Residence = form.cleaned_data.get('Residence')
        form.instance.Phonenum = form.cleaned_data.get('Phonenum')
        form.instance.user = self.request.user
        form.save()
        return HttpResponseRedirect(reverse('signup_success'))


def userprofileold(request):
    if request.method=="POST":
        form=UserProfileForm(request.POST)

        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return HttpResponseRedirect('signup_success')
    else:
        args ={}
        args.update(csrf(request))
        args['form']=UserProfileForm()
    return render_to_response('userprofile.html', args)


class VaccineReceivedReportView(FormView):
    form_class = VaccineReceivedReportForm
    template_name = 'vaccinereceived.html'

    def form_valid(self, form):
        form.instance.vaccinedose = VaccineDose.objects.get(id=self.request.GET.get('dose'))
        form.instance.patient_vaccine = Vaccine.objects.get(id=self.request.GET.get('vaccine'))
        form.instance.patient = self.request.user.userprofile
        form.save()
        messages.success(self.request, 'Vaccine updated successfully. Thank you.')
        return HttpResponseRedirect(reverse('vaccinereceived'))



class MakeAppointmentFormView(FormView):
    form_class = MakeAppointmentForm
    template_name='appointment.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render_to_response(self.template_name, {'form':form}, context_instance=RequestContext(request))

    def form_valid(self, form):
        form.instance.firstchoicedate = form.cleaned_data.get('firstchoicedate')
        form.instance.secondchoicedate = form.cleaned_data.get('secondchoicedate')
        form.instance.purposeofvisit = form.cleaned_data.get('purposeofvisit')
        form.instance.patient = self.request.user.userprofile
        form.save()
        messages.success(self.request, 'Appointment added successfully. Thank you!')
        return HttpResponseRedirect(reverse('makeappointment'))


class SendMessageFormView(FormView):
    form_class = MessageSentForm
    template_name = 'sendmessage.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render_to_response(self.template_name, {'form':form}, context_instance=RequestContext(request))

    def form_valid(self, form):
        form.instance.message=form.cleaned_data.get('message')
        form.instance.messagesubject=form.cleaned_data.get('messagesubject')
        form.instance.patient=self.request.user.userprofile
        form.save()
        messages.success(self.request, 'Message successfully sent. Thank you, we shall get back to you')
        return HttpResponseRedirect(reverse('sendmessage'))

class AppointmentListView(ListView):
    model = Appointment
    template_name = 'appointment_list.html'

    def get_queryset(self):
        queryset = super(AppointmentListView, self).get_queryset()
        queryset = queryset.filter(patient=self.request.user.userprofile)
        return queryset


def Messages(request):
     if request.method=="GET":
        model = Message
        template_name = 'messages.html'

        # queryset= super(MessagesListView, self).get_queryset()
        queryset = Message.objects.filter(patient=request.user.userprofile)
        queryset1 = queryset.distinct('date')
        return render_to_response('messages.html', {'datehead': queryset1, 'datedmessages': queryset })


def reportvaccine(request):

    if request.method=="POST":


        form = VaccineReportForm(request.POST)

        if form.is_valid():
            form.instance.patient= UserProfile.objects.get(IDNum=request.user.userprofile)

            form.instance.vaccine= Vaccine.objects.get(vaccineIDnum = request.POST.get('Vaccine'))

            form.save()

            messages.success(request, 'Report successfully sent. Thank you.')
            return HttpResponseRedirect(reverse('reportvaccine'))

    args={}
    args.update(csrf(request))
    args['form'] = VaccineReportForm()

    return render_to_response('vaccinereport.html', args)





