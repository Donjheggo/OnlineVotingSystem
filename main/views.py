from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *
from account.models import *
from .forms import *
from django.db.models import F
import sweetify
from account.forms import *
from main.decorators import *
import datetime


def landingpage(request):
    return render(request, 'landingpage/landingpage.html')  


@login_required(login_url='login')
def home(request):
    context = {
        'title': 'Home'
    }
    return render(request, 'main/home.html', context)

@login_required(login_url='login')
@verified_or_superuser
@receipt_exist
def receipt(request):
    context = {
        'title': 'Receipt',
        'receipts': Receipt.objects.filter(owner=request.user)

    }
    return render(request, 'main/receipt.html', context)

@user_passes_test(lambda u: u.is_superuser)
def voters(request):
    context = {
        'title': 'Voters',
        'voters': Account.objects.filter(is_superuser=False)
    }
    return render(request, 'main/voters.html', context)


@user_passes_test(lambda u: u.is_superuser)
def updatevoter(request, pk):
    voter = Account.objects.get(id=pk)
    voterform = RegistrationForm(instance=voter)
    if request.method == 'POST':
        voterform = RegistrationForm(request.POST, instance=voter)
        if voterform.is_valid():
            voterform.save()
            return HttpResponseRedirect(reverse('voters'))

    context = {
        'title': 'Update Voter',
        'voter': voter,
        'form': voterform,
    }
    
    return render(request, 'main/voterupdate.html', context)



@user_passes_test(lambda u: u.is_superuser)
def deletevoter(request, pk):
    voter = Account.objects.get(id=pk)
    context = {
        'title': 'Delete Voter',
        'voter': voter,
    }
    if request.method == 'POST':
        voter.delete()
        return HttpResponseRedirect(reverse('voters'))
    return render(request, 'main/voterdelete.html', context)



@login_required(login_url='login')
@verified_or_superuser
def profile(request, pk):
    profile = Account.objects.get(id=pk)
    student_form = UpdateProfileForm(instance=profile)
    if request.method == 'POST':
        student_form = UpdateProfileForm(request.POST, instance=profile)
        password1 = request.POST['password']
        password2 = request.POST['password2']
        if password1 != password2:
            print("password does not match")
            sweetify.error(request, 'Password does not match!')
            return HttpResponseRedirect(request.path_info)
        elif student_form.is_valid():
            student_form.save()
            sweetify.success(request, 'Updated Successfully')
            return HttpResponseRedirect(reverse('login'))
        else: 
            sweetify.error(request, 'Invalid Credentials!')
            return HttpResponseRedirect(request.path_info)
    context = {
        'title': 'Profile',
        'student_form': student_form,
        'profile': profile,
    }
    return render(request, 'main/profile.html', context)


@user_passes_test(lambda u: u.is_superuser)
def electionschedule(request):
    schedule_form = ScheduleForm()
    if request.method == 'POST':
        schedule_form = ScheduleForm(request.POST)
        if schedule_form.is_valid():
            schedule_form.save()
            return HttpResponseRedirect(reverse('electionschedule'))
    context = {
        'title': 'Schedule',
        'schedule': votingschedule.objects.all(),
        'schedule_form': schedule_form,
    }
    return render(request, 'main/electionschedule.html', context)


@user_passes_test(lambda u: u.is_superuser)
def updateelectionschedule(request, pk):
    schedule = votingschedule.objects.get(id=pk)
    schedule_form = UpdateScheduleForm(instance=schedule)
    context = {
        'title': 'Update Schedule',
        'schedule': schedule,
        'schedule_form': schedule_form
    }
    if request.method == 'POST':
        schedule_form = UpdateScheduleForm(request.POST, instance=schedule)
        if schedule_form.is_valid():
            schedule_form.save()
            return HttpResponseRedirect(reverse('electionschedule'))
    return render(request, 'main/updateelectionschedule.html', context)


@user_passes_test(lambda u: u.is_superuser)
def deleteelectionschedule(request, pk):
    schedule = votingschedule.objects.get(id=pk)
    context = {
        'title': 'Delete Shedule',
        'schedule': schedule,
    }
    if request.method == 'POST':
        schedule.delete()
        return HttpResponseRedirect(reverse('electionschedule'))
    return render(request, 'main/deleteschedule.html', context)


@user_passes_test(lambda u: u.is_superuser)
def dashboard(request):
    mainssgcandidates =  MAINSSG_Candidate.objects.all().count()
    ceitcandidates = CEIT_Candidate.objects.all().count()
    ctecandidates = CTE_Candidate.objects.all().count()
    cascandidates = CAS_Candidate.objects.all().count()
    cotcandidates = COT_Candidate.objects.all().count()
    totalcandidates = mainssgcandidates + ceitcandidates + ctecandidates + cascandidates + cotcandidates
    voted_department = Account.objects.filter(voted_department=True).count()
    voted_main = Account.objects.filter(voted_main=True).count()
    context = {
        'title': 'Dashboard',

        'totalcandidates': totalcandidates,

        'mainssg': MAINSSG_Candidate.objects.all(),
        'mainssgcandidates': mainssgcandidates,

        'ceit': CEIT_Candidate.objects.all(),
        'ceitcandidates': ceitcandidates,

        'cte': CTE_Candidate.objects.all(),
        'ctecandidates': ctecandidates,

        'cas': CAS_Candidate.objects.all(),
        'cascandidates': cascandidates,

        'cot': COT_Candidate.objects.all(),
        'cotcandidates': cotcandidates,
        
        'registered': Account.objects.filter(is_superuser=False).count(),
        'voted': voted_department + voted_main,
    }
    return render(request, 'main/dashboard.html', context)



############################################################################################################

@user_passes_test(lambda u: u.is_superuser)
def ceitcandidates(request):
    candidate_form = CEIT_CandidatesForm()
    if request.method == 'POST':
        candidate_form = CEIT_CandidatesForm(request.POST, request.FILES)
        if candidate_form.is_valid():
            candidate_form.save()
            return HttpResponseRedirect(reverse("ceitcandidates"))

    context = {
        'title': 'CEIT Candidates',
        'form': candidate_form,
        'ceit': CEIT_Candidate.objects.all()
    }
    return render(request, 'main/ceitcandidates.html', context) 

@user_passes_test(lambda u: u.is_superuser)
def updateceitcandidate(request, pk):
    candidate = CEIT_Candidate.objects.get(id=pk)
    candidate_form = CEIT_CandidatesForm(instance=candidate)
    context = {
                'title': 'Update CEIT Candidate',
                'candidate_form': candidate_form
    }
    if request.method == 'POST':
        candidate_form = CEIT_CandidatesForm(request.POST, request.FILES, instance=candidate)
        if candidate_form.is_valid():
            candidate_form.save()
            return HttpResponseRedirect(reverse('ceitcandidates'))
    return render(request, 'main/ceitupdatecandidate.html', context)


@user_passes_test(lambda u: u.is_superuser)
def deleteceitcandidate(request, pk):
    ceitcandidate = CEIT_Candidate.objects.get(id=pk)
    context = {
        'title': 'Delete CEIT Candidate',
        'ceitcandidate': ceitcandidate,
    }
    if request.method == 'POST':
        ceitcandidate.delete()
        return HttpResponseRedirect(reverse('ceitcandidates'))

    return render(request, 'main/ceitdeletecandidate.html', context)



@user_passes_test(lambda u: u.is_superuser)
def ceittally(request):
    context = {
        'title': 'CEIT Tally',
        'ceit': CEIT_Candidate.objects.all(),
    }
    return render(request, 'main/ceittally.html', context)


@user_passes_test(lambda u: u.is_superuser)
def ceitresult(request):
    context = {
        'title': 'CEIT Result',
        'governor': CEIT_Candidate.objects.filter(position='Governor'),
        'vicegovernor': CEIT_Candidate.objects.filter(position='Vice Governor'),
        'secretary': CEIT_Candidate.objects.filter(position='Secretary'),
        'treasurer': CEIT_Candidate.objects.filter(position='Treasurer'),
        'auditor': CEIT_Candidate.objects.filter(position='Auditor'),
        'pio': CEIT_Candidate.objects.filter(position='PIO'),
        'businessmanager': CEIT_Candidate.objects.filter(position='Business Manager'),
        'peaceofficer': CEIT_Candidate.objects.filter(position='Peace Officer'),
    }
    return render(request, 'main/ceitresult.html', context)



@login_required(login_url='login')
@verified_or_superuser
@ceit_voter_or_superuser
@department_not_voted_or_superuser
@ceit_schedule_or_superuser
def ceitballot(request):
    context = {
        'title': 'CEIT Ballot',
        'governor': CEIT_Candidate.objects.filter(position='Governor'),
        'vicegovernor': CEIT_Candidate.objects.filter(position='Vice Governor'),
        'secretary': CEIT_Candidate.objects.filter(position='Secretary'),
        'treasurer': CEIT_Candidate.objects.filter(position='Treasurer'),
        'auditor': CEIT_Candidate.objects.filter(position='Auditor'),
        'pio': CEIT_Candidate.objects.filter(position='PIO'),
        'businessmanager': CEIT_Candidate.objects.filter(position='Business Manager'),
        'peaceofficer': CEIT_Candidate.objects.filter(position='Peace Officer'),
    }
    if request.method == 'POST':
        voter = request.user
        voter.voted_department = True
        voter.save()
        sweetify.success(request, 'Vote Submitted!')


    ###### GOVERNOR ######
    try: 
        request.POST['governor']
        voted_governor = request.POST["governor"]
        g_voted = CEIT_Candidate.objects.get(fullname=voted_governor)
        g_voters = g_voted.voters
        g_voters.add(voter)
        receipt = Receipt.objects.get(owner=voter, department='CEIT')
        receipt.governor = voted_governor
        receipt.save()

    except:
        print("No selected Governor")
    

    ###### VICE GOVERNOR ######
    try:
        voted_vicegovernor = request.POST["vicegovernor"]
        vg_voted = CEIT_Candidate.objects.get(fullname=voted_vicegovernor)
        vg_voters = vg_voted.voters
        vg_voters.add(voter)
        receipt = Receipt.objects.get(owner=voter, department='CEIT')
        receipt.vice_governor = voted_vicegovernor
        receipt.save()


    except:
        print("No selected Vice Governor")


        ###### Secretary ######
    try:
        voted_secretary = request.POST["secretary"]
        s_voted = CEIT_Candidate.objects.get(fullname=voted_secretary)
        s_voters = s_voted.voters
        s_voters.add(voter)
        receipt = Receipt.objects.get(owner=voter, department='CEIT')
        receipt.secretary = voted_secretary
        receipt.save()


    except:
        print("No selected Secretary")


            ###### Treasurer ######
    try:
        voted_treasurer = request.POST["treasurer"]
        t_voted = CEIT_Candidate.objects.get(fullname=voted_treasurer)
        t_voters = t_voted.voters
        t_voters.add(voter)
        receipt = Receipt.objects.get(owner=voter, department='CEIT')
        receipt.treasurer = voted_treasurer
        receipt.save()
        
    except:
        print("No selected Treasurer")


            ###### Auditor ######
    try:
        voted_auditor = request.POST["auditor"]
        a_voted = CEIT_Candidate.objects.get(fullname=voted_auditor)
        a_voters = a_voted.voters
        a_voters.add(voter)
        receipt = Receipt.objects.get(owner=voter, department='CEIT')
        receipt.auditor = voted_auditor
        receipt.save()
        
    except:
        print("No selected Auditor")


            ###### PIO ######
    try:
        voted_pio = request.POST["pio"]
        p_voted = CEIT_Candidate.objects.get(fullname=voted_pio)
        p_voters = p_voted.voters
        p_voters.add(voter)
        receipt = Receipt.objects.get(owner=voter, department='CEIT')
        receipt.pio = voted_pio
        receipt.save()
        
    except:
        print("No selected PIO")


            ###### Business Manager ######
    try:
        voted_buss = request.POST["businessmanager"]
        b_voted = CEIT_Candidate.objects.get(fullname=voted_buss)
        b_voters = b_voted.voters
        b_voters.add(voter)
        receipt = Receipt.objects.get(owner=voter, department='CEIT')
        receipt.businessmanager = voted_buss
        receipt.save()
        
    except:
        print("No selected Business Manager")

    
            ###### Peace Officer ######
    try:
        voted_peace = request.POST["peaceofficer"]
        p_voted = CEIT_Candidate.objects.get(fullname=voted_peace)
        p_voters = p_voted.voters
        p_voters.add(voter)
        receipt = Receipt.objects.get(owner=voter, department='CEIT')
        receipt.peaceofficer = voted_peace
        receipt.save()
        return HttpResponseRedirect(reverse('receipt'))
        
    except:
        print("No selected Peace Officer")


    return render(request, 'main/ceitballot.html', context)
    



#################################################  CTE   ##################################################

@user_passes_test(lambda u: u.is_superuser)
def ctecandidates(request):
    candidate_form = CTE_CandidatesForm()
    if request.method == 'POST':
        candidate_form = CTE_CandidatesForm(request.POST, request.FILES)
        if candidate_form.is_valid():
            candidate_form.save()
            return HttpResponseRedirect(reverse("ctecandidates"))

    context = {
        'title': 'CTE Candidates',
        'form': candidate_form,
        'cte': CTE_Candidate.objects.all()
    }
    return render(request, 'main/ctecandidates.html', context)

@user_passes_test(lambda u: u.is_superuser)
def updatectecandidate(request, pk):
    candidate = CTE_Candidate.objects.get(id=pk)
    candidate_form = CTE_CandidatesForm(instance=candidate)
    context = {
        'title': 'Update CTE Candidate',
        'candidate_form': candidate_form
    }
    if request.method == 'POST':
        candidate_form = CTE_CandidatesForm(request.POST, request.FILES, instance=candidate)
        if candidate_form.is_valid():
            candidate_form.save()
            return HttpResponseRedirect(reverse('ctecandidates'))
    return render(request, 'main/cteupdatecandidate.html', context)


@user_passes_test(lambda u: u.is_superuser)
def deletectecandidate(request, pk):
    ctecandidate = CTE_Candidate.objects.get(id=pk)
    context = {
        'title': 'Delete CTE Candidate',
      'ctecandidate': ctecandidate,
    }
    if request.method == 'POST':
        ctecandidate.delete()
        return HttpResponseRedirect(reverse('ctecandidates'))

    return render(request, 'main/ctedeletecandidate.html', context)



@user_passes_test(lambda u: u.is_superuser)
def ctetally(request):
    context = {
        'title': 'CTE Tally',
        'cte': CTE_Candidate.objects.all(),
    }
    return render(request, 'main/ctetally.html', context)


@user_passes_test(lambda u: u.is_superuser)
def cteresult(request):
    context = {
        'governor': CTE_Candidate.objects.filter(position='Governor'),
        'vicegovernor': CTE_Candidate.objects.filter(position='Vice Governor'),
        'secretary': CTE_Candidate.objects.filter(position='Secretary'),
        'treasurer': CTE_Candidate.objects.filter(position='Treasurer'),
        'auditor': CTE_Candidate.objects.filter(position='Auditor'),
        'pio': CTE_Candidate.objects.filter(position='PIO'),
        'businessmanager': CTE_Candidate.objects.filter(position='Business Manager'),
        'peaceofficer': CTE_Candidate.objects.filter(position='Peace Officer'),
    }
    return render(request, 'main/cteresult.html', context)



@login_required(login_url='login')
@verified_or_superuser
@cte_voter_or_superuser
@department_not_voted_or_superuser
@cte_schedule_or_superuser
def cteballot(request):
    context = {
        'title': 'CTE Ballot',
        'governor': CTE_Candidate.objects.filter(position='Governor'),
        'vicegovernor': CTE_Candidate.objects.filter(position='Vice Governor'),
        'secretary': CTE_Candidate.objects.filter(position='Secretary'),
        'treasurer': CTE_Candidate.objects.filter(position='Treasurer'),
        'auditor': CTE_Candidate.objects.filter(position='Auditor'),
        'pio': CTE_Candidate.objects.filter(position='PIO'),
        'businessmanager': CTE_Candidate.objects.filter(position='Business Manager'),
        'peaceofficer': CTE_Candidate.objects.filter(position='Peace Officer'),
    }
    if request.method == 'POST':
        voter = request.user
        voter.voted_department = True
        voter.save()
        sweetify.success(request, 'Vote Submitted!')
        

    ###### GOVERNOR ######
    try: 
        request.POST['governor']
        voted_governor = request.POST["governor"]
        g_voted = CTE_Candidate.objects.get(fullname=voted_governor)
        g_voters = g_voted.voters
        g_voters.add(voter)
        receipt = Receipt.objects.get(owner=voter, department='CTE')
        receipt.governor = voted_governor
        receipt.save()

    except:
        print("No selected Governor")
    

    ###### VICE GOVERNOR ######
    try:
        voted_vicegovernor = request.POST["vicegovernor"]
        vg_voted = CTE_Candidate.objects.get(fullname=voted_vicegovernor)
        vg_voters = vg_voted.voters
        vg_voters.add(voter)
        receipt = Receipt.objects.get(owner=voter, department='CTE')
        receipt.vice_governor = voted_vicegovernor
        receipt.save()


    except:
        print("No selected Vice Governor")


        ###### Secretary ######
    try:
        voted_secretary = request.POST["secretary"]
        s_voted = CTE_Candidate.objects.get(fullname=voted_secretary)
        s_voters = s_voted.voters
        s_voters.add(voter)
        receipt = Receipt.objects.get(owner=voter, department='CTE')
        receipt.secretary = voted_secretary
        receipt.save()


    except:
        print("No selected Secretary")


            ###### Treasurer ######
    try:
        voted_treasurer = request.POST["treasurer"]
        t_voted = CTE_Candidate.objects.get(fullname=voted_treasurer)
        t_voters = t_voted.voters
        t_voters.add(voter)
        receipt = Receipt.objects.get(owner=voter, department='CTE')
        receipt.treasurer = voted_treasurer
        receipt.save()
        
    except:
        print("No selected Treasurer")


            ###### Auditor ######
    try:
        voted_auditor = request.POST["auditor"]
        a_voted = CTE_Candidate.objects.get(fullname=voted_auditor)
        a_voters = a_voted.voters
        a_voters.add(voter)
        receipt = Receipt.objects.get(owner=voter, department='CTE')
        receipt.auditor = voted_auditor
        receipt.save()
        
    except:
        print("No selected Auditor")


            ###### PIO ######
    try:
        voted_pio = request.POST["pio"]
        p_voted = CTE_Candidate.objects.get(fullname=voted_pio)
        p_voters = p_voted.voters
        p_voters.add(voter)
        receipt = Receipt.objects.get(owner=voter, department='CTE')
        receipt.pio = voted_pio
        receipt.save()
        
    except:
        print("No selected PIO")


            ###### Business Manager ######
    try:
        voted_buss = request.POST["businessmanager"]
        b_voted = CTE_Candidate.objects.get(fullname=voted_buss)
        b_voters = b_voted.voters
        b_voters.add(voter)
        receipt = Receipt.objects.get(owner=voter, department='CTE')
        receipt.businessmanager = voted_buss
        receipt.save()
        
    except:
        print("No selected Business Manager")

    
            ###### Peace Officer ######
    try:
        voted_peace = request.POST["peaceofficer"]
        p_voted = CTE_Candidate.objects.get(fullname=voted_peace)
        p_voters = p_voted.voters
        p_voters.add(voter)
        receipt = Receipt.objects.get(owner=voter, department='CTE')
        receipt.peaceofficer = voted_peace
        receipt.save()
        return HttpResponseRedirect(reverse('receipt'))
        
    except:
        print("No selected Peace Officer")


    return render(request, 'main/cteballot.html', context)







########################################################       ###########################################################


@user_passes_test(lambda u: u.is_superuser)
def cascandidates(request):
    candidate_form = CAS_CandidatesForm()
    if request.method == 'POST':
        candidate_form = CAS_CandidatesForm(request.POST, request.FILES)
        if candidate_form.is_valid():
            candidate_form.save()
            return HttpResponseRedirect(reverse("cascandidates"))

    context = {
        'title': 'CAS Candidates',
        'form': candidate_form,
        'cas': CAS_Candidate.objects.all()
    }
    return render(request, 'main/cascandidates.html', context)



@user_passes_test(lambda u: u.is_superuser)
def updatecascandidate(request, pk):
    candidate = CAS_Candidate.objects.get(id=pk)
    candidate_form = CAS_CandidatesForm(instance=candidate)
    context = {
        'title': 'Update CAS Candidate',
        'candidate_form': candidate_form
    }
    if request.method == 'POST':
        candidate_form = CAS_CandidatesForm(request.POST, request.FILES, instance=candidate)
        if candidate_form.is_valid():
            candidate_form.save()
            return HttpResponseRedirect(reverse('cascandidates'))
    return render(request, 'main/casupdatecandidate.html', context)


@user_passes_test(lambda u: u.is_superuser)
def deletecascandidate(request, pk):
    cascandidate = CAS_Candidate.objects.get(id=pk)
    context = {
        'title': 'Delete CAS Candidate',
      'cascandidate': cascandidate,
    }
    if request.method == 'POST':
        cascandidate.delete()
        return HttpResponseRedirect(reverse('cascandidates'))

    return render(request, 'main/casdeletecandidate.html', context)


@user_passes_test(lambda u: u.is_superuser)
def castally(request):
    context = {
        'title': 'CAS Tally',
        'cas': CAS_Candidate.objects.all(),
    }
    return render(request, 'main/castally.html', context)


@user_passes_test(lambda u: u.is_superuser)
def casresult(request):
    context = {
        'title': 'CAS Result',
        'governor': CAS_Candidate.objects.filter(position='Governor'),
        'vicegovernor': CAS_Candidate.objects.filter(position='Vice Governor'),
        'secretary': CAS_Candidate.objects.filter(position='Secretary'),
        'treasurer': CAS_Candidate.objects.filter(position='Treasurer'),
        'auditor': CAS_Candidate.objects.filter(position='Auditor'),
        'pio': CAS_Candidate.objects.filter(position='PIO'),
        'businessmanager': CAS_Candidate.objects.filter(position='Business Manager'),
        'peaceofficer': CAS_Candidate.objects.filter(position='Peace Officer'),
    }
    return render(request, 'main/casresult.html', context)



@login_required(login_url='login')
@verified_or_superuser
@cas_voter_or_superuser
@department_not_voted_or_superuser
@cas_schedule_or_superuser
def casballot(request):
    context = {
        'title': 'CAS Ballot',
        'governor': CAS_Candidate.objects.filter(position='Governor'),
        'vicegovernor': CAS_Candidate.objects.filter(position='Vice Governor'),
        'secretary': CAS_Candidate.objects.filter(position='Secretary'),
        'treasurer': CAS_Candidate.objects.filter(position='Treasurer'),
        'auditor': CAS_Candidate.objects.filter(position='Auditor'),
        'pio': CAS_Candidate.objects.filter(position='PIO'),
        'businessmanager': CAS_Candidate.objects.filter(position='Business Manager'),
        'peaceofficer': CAS_Candidate.objects.filter(position='Peace Officer'),
    }
    if request.method == 'POST':
        voter = request.user
        voter.voted_department = True
        voter.save()
        sweetify.success(request, 'Vote Submitted!')
        

    ###### GOVERNOR ######
    try: 
        request.POST['governor']
        voted_governor = request.POST["governor"]
        g_voted = CAS_Candidate.objects.get(fullname=voted_governor)
        g_voters = g_voted.voters
        g_voters.add(voter)
        receipt = Receipt.objects.get(owner=voter, department='CAS')
        receipt.governor = voted_governor
        receipt.save()

    except:
        print("No selected Governor")
    

    ###### VICE GOVERNOR ######
    try:
        voted_vicegovernor = request.POST["vicegovernor"]
        vg_voted = CAS_Candidate.objects.get(fullname=voted_vicegovernor)
        vg_voters = vg_voted.voters
        vg_voters.add(voter)
        receipt = Receipt.objects.get(owner=voter, department='CAS')
        receipt.vice_governor = voted_vicegovernor
        receipt.save()


    except:
        print("No selected Vice Governor")


        ###### Secretary ######
    try:
        voted_secretary = request.POST["secretary"]
        s_voted = CAS_Candidate.objects.get(fullname=voted_secretary)
        s_voters = s_voted.voters
        s_voters.add(voter)
        receipt = Receipt.objects.get(owner=voter, department='CAS')
        receipt.secretary = voted_secretary
        receipt.save()


    except:
        print("No selected Secretary")


            ###### Treasurer ######
    try:
        voted_treasurer = request.POST["treasurer"]
        t_voted = CAS_Candidate.objects.get(fullname=voted_treasurer)
        t_voters = t_voted.voters
        t_voters.add(voter)
        receipt = Receipt.objects.get(owner=voter, department='CAS')
        receipt.treasurer = voted_treasurer
        receipt.save()
        
    except:
        print("No selected Treasurer")


            ###### Auditor ######
    try:
        voted_auditor = request.POST["auditor"]
        a_voted = CAS_Candidate.objects.get(fullname=voted_auditor)
        a_voters = a_voted.voters
        a_voters.add(voter)
        receipt = Receipt.objects.get(owner=voter, department='CAS')
        receipt.auditor = voted_auditor
        receipt.save()
        
    except:
        print("No selected Auditor")


            ###### PIO ######
    try:
        voted_pio = request.POST["pio"]
        p_voted = CAS_Candidate.objects.get(fullname=voted_pio)
        p_voters = p_voted.voters
        p_voters.add(voter)
        receipt = Receipt.objects.get(owner=voter, department='CAS')
        receipt.pio = voted_pio
        receipt.save()
        
    except:
        print("No selected PIO")


            ###### Business Manager ######
    try:
        voted_buss = request.POST["businessmanager"]
        b_voted = CAS_Candidate.objects.get(fullname=voted_buss)
        b_voters = b_voted.voters
        b_voters.add(voter)
        receipt = Receipt.objects.get(owner=voter, department='CAS')
        receipt.businessmanager = voted_buss
        receipt.save()
        
    except:
        print("No selected Business Manager")

    
            ###### Peace Officer ######
    try:
        voted_peace = request.POST["peaceofficer"]
        p_voted = CAS_Candidate.objects.get(fullname=voted_peace)
        p_voters = p_voted.voters
        p_voters.add(voter)
        receipt = Receipt.objects.get(owner=voter, department='CAS')
        receipt.peaceofficer = voted_peace
        receipt.save()
        return HttpResponseRedirect(reverse('receipt'))
        
    except:
        print("No selected Peace Officer")
    

    return render(request, 'main/casballot.html', context)




###############################################################################################################################################################


@user_passes_test(lambda u: u.is_superuser)
def cotcandidates(request):
    candidate_form = COT_CandidatesForm()
    if request.method == 'POST':
        candidate_form = COT_CandidatesForm(request.POST, request.FILES)
        if candidate_form.is_valid():
            candidate_form.save()
            return HttpResponseRedirect(reverse("cotcandidates"))

    context = {
        'title': 'COT Candidates',
        'form': candidate_form,
        'cot': COT_Candidate.objects.all()
    }
    return render(request, 'main/cotcandidates.html', context)


@user_passes_test(lambda u: u.is_superuser)
def updatecotcandidate(request, pk):
    candidate = COT_Candidate.objects.get(id=pk)
    candidate_form = COT_CandidatesForm(instance=candidate)
    context = {
        'title': 'Update COT Candidate',
        'candidate_form': candidate_form
    }
    if request.method == 'POST':
        candidate_form = COT_CandidatesForm(request.POST, request.FILES, instance=candidate)
        if candidate_form.is_valid():
            candidate_form.save()
            return HttpResponseRedirect(reverse('cotcandidates'))
    return render(request, 'main/cotupdatecandidate.html', context)


@user_passes_test(lambda u: u.is_superuser)
def deletecotcandidate(request, pk):
    cotcandidate = COT_Candidate.objects.get(id=pk)
    context = {
        'title': 'Delete COT Candidate',
        'cotcandidate': cotcandidate,
    }
    if request.method == 'POST':
        cotcandidate.delete()
        return HttpResponseRedirect(reverse('cotcandidates'))

    return render(request, 'main/cotdeletecandidate.html', context)



@user_passes_test(lambda u: u.is_superuser)
def cottally(request):
    context = {
        'title': 'COT Tally',
        'cot': COT_Candidate.objects.all(),
    }
    return render(request, 'main/cottally.html', context)


@user_passes_test(lambda u: u.is_superuser)
def cotresult(request):
    context = {
        'title': 'COT Result',
        'governor': COT_Candidate.objects.filter(position='Governor'),
        'vicegovernor': COT_Candidate.objects.filter(position='Vice Governor'),
        'secretary': COT_Candidate.objects.filter(position='Secretary'),
        'treasurer': COT_Candidate.objects.filter(position='Treasurer'),
        'auditor': COT_Candidate.objects.filter(position='Auditor'),
        'pio': COT_Candidate.objects.filter(position='PIO'),
        'businessmanager': COT_Candidate.objects.filter(position='Business Manager'),
        'peaceofficer': COT_Candidate.objects.filter(position='Peace Officer'),
    }
    return render(request, 'main/cotresult.html', context)



@login_required(login_url='login')
@verified_or_superuser
@cot_voter_or_superuser
@department_not_voted_or_superuser
@cot_schedule_or_superuser
def cotballot(request):
    context = {
        'title': 'COT Ballot',
        'governor': COT_Candidate.objects.filter(position='Governor'),
        'vicegovernor': COT_Candidate.objects.filter(position='Vice Governor'),
        'secretary': COT_Candidate.objects.filter(position='Secretary'),
        'treasurer': COT_Candidate.objects.filter(position='Treasurer'),
        'auditor': COT_Candidate.objects.filter(position='Auditor'),
        'pio': COT_Candidate.objects.filter(position='PIO'),
        'businessmanager': COT_Candidate.objects.filter(position='Business Manager'),
        'peaceofficer': COT_Candidate.objects.filter(position='Peace Officer'),
    }
    if request.method == 'POST':
        voter = request.user
        voter.voted_department = True
        voter.save()
        sweetify.success(request, 'Vote Submitted!')      
        

    ###### GOVERNOR ######
    try: 
        request.POST['governor']
        voted_governor = request.POST["governor"]
        g_voted = COT_Candidate.objects.get(fullname=voted_governor)
        g_voters = g_voted.voters
        g_voters.add(voter)
        receipt = Receipt.objects.get(owner=voter, department="COT")
        receipt.governor = voted_governor
        receipt.save()

    except:
        print("No selected Governor")
    

    ###### VICE GOVERNOR ######
    try:
        voted_vicegovernor = request.POST["vicegovernor"]
        vg_voted = COT_Candidate.objects.get(fullname=voted_vicegovernor)
        vg_voters = vg_voted.voters
        vg_voters.add(voter)
        receipt = Receipt.objects.get(owner=voter, department="COT")
        receipt.vice_governor = voted_vicegovernor
        receipt.save()


    except:
        print("No selected Vice Governor")


        ###### Secretary ######
    try:
        voted_secretary = request.POST["secretary"]
        s_voted = COT_Candidate.objects.get(fullname=voted_secretary)
        s_voters = s_voted.voters
        s_voters.add(voter)
        receipt = Receipt.objects.get(owner=voter, department="COT")
        receipt.secretary = voted_secretary
        receipt.save()


    except:
        print("No selected Secretary")


            ###### Treasurer ######
    try:
        voted_treasurer = request.POST["treasurer"]
        t_voted = COT_Candidate.objects.get(fullname=voted_treasurer)
        t_voters = t_voted.voters
        t_voters.add(voter)
        receipt = Receipt.objects.get(owner=voter, department="COT")
        receipt.treasurer = voted_treasurer
        receipt.save()
        
    except:
        print("No selected Treasurer")


            ###### Auditor ######
    try:
        voted_auditor = request.POST["auditor"]
        a_voted = COT_Candidate.objects.get(fullname=voted_auditor)
        a_voters = a_voted.voters
        a_voters.add(voter)
        receipt = Receipt.objects.get(owner=voter, department="COT")
        receipt.auditor = voted_auditor
        receipt.save()
        
    except:
        print("No selected Auditor")


            ###### PIO ######
    try:
        voted_pio = request.POST["pio"]
        p_voted = COT_Candidate.objects.get(fullname=voted_pio)
        p_voters = p_voted.voters
        p_voters.add(voter)
        receipt = Receipt.objects.get(owner=voter, department="COT")
        receipt.pio = voted_pio
        receipt.save()
        
    except:
        print("No selected PIO")


            ###### Business Manager ######
    try:
        voted_buss = request.POST["businessmanager"]
        b_voted = COT_Candidate.objects.get(fullname=voted_buss)
        b_voters = b_voted.voters
        b_voters.add(voter)
        receipt = Receipt.objects.get(owner=voter, department="COT")
        receipt.businessmanager = voted_buss
        receipt.save()
        
    except:
        print("No selected Business Manager")

    
            ###### Peace Officer ######
    try:
        voted_peace = request.POST["peaceofficer"]
        p_voted = COT_Candidate.objects.get(fullname=voted_peace)
        p_voters = p_voted.voters
        p_voters.add(voter)
        receipt = Receipt.objects.get(owner=voter, department="COT")
        receipt.peaceofficer = voted_peace
        receipt.save()
        return HttpResponseRedirect(reverse('receipt'))
        
    except:
        print("No selected Peace Officer")


    return render(request, 'main/cotballot.html', context)



###############################################################################################################################################################

@user_passes_test(lambda u: u.is_superuser)
def mainssgcandidates(request):
    candidate_form = MAINSSG_CandidatesForm()
    if request.method == 'POST':
        candidate_form = MAINSSG_CandidatesForm(request.POST, request.FILES)
        if candidate_form.is_valid():
            candidate_form.save()
            return HttpResponseRedirect(reverse("mainssgcandidates"))

    context = {
        'title': 'Main SSG Candidates',
        'form': candidate_form,
        'mainssg': MAINSSG_Candidate.objects.all()
    }
    return render(request, 'main/mainssgcandidates.html', context)


@user_passes_test(lambda u: u.is_superuser)
def updatemainssgcandidate(request, pk):
    candidate = MAINSSG_Candidate.objects.get(id=pk)
    candidate_form = MAINSSG_CandidatesForm(instance=candidate)
    context = {
                'title': 'Update Main SSG Candidate',
                'candidate_form': candidate_form
    }
    if request.method == 'POST':
        candidate_form = MAINSSG_CandidatesForm(request.POST, request.FILES, instance=candidate)
        if candidate_form.is_valid():
            candidate_form.save()
            return HttpResponseRedirect(reverse('mainssgcandidates'))
    return render(request, 'main/mainssgupdatecandidate.html', context)


@user_passes_test(lambda u: u.is_superuser)
def deletemainssgcandidate(request, pk):
    mainssgcandidate = MAINSSG_Candidate.objects.get(id=pk)
    context = {
        'title': 'Delete Main SSG Candidate',
      'mainssgcandidate': mainssgcandidate,
    }
    if request.method == 'POST':
        mainssgcandidate.delete()
        return HttpResponseRedirect(reverse('mainssgcandidates'))

    return render(request, 'main/mainssgeletecandidate.html', context)



@user_passes_test(lambda u: u.is_superuser)
def mainssgtally(request):
    context = {
        'title': 'Main SSG Tally',
        'mainssg': MAINSSG_Candidate.objects.all(),
    }
    return render(request, 'main/mainssgtally.html', context)


@user_passes_test(lambda u: u.is_superuser)
def mainssgresult(request):
    context = {
        'title': 'Main SSG Result',
        'governor': MAINSSG_Candidate.objects.filter(position='Governor'),
        'vicegovernor': MAINSSG_Candidate.objects.filter(position='Vice Governor'),
        'secretary': MAINSSG_Candidate.objects.filter(position='Secretary'),
        'treasurer': MAINSSG_Candidate.objects.filter(position='Treasurer'),
        'auditor': MAINSSG_Candidate.objects.filter(position='Auditor'),
        'pio': MAINSSG_Candidate.objects.filter(position='PIO'),
        'businessmanager': MAINSSG_Candidate.objects.filter(position='Business Manager'),
        'peaceofficer': MAINSSG_Candidate.objects.filter(position='Peace Officer'),
    }
    return render(request, 'main/mainssgresult.html', context)



@login_required(login_url='login')
@verified_or_superuser
@main_schedule_or_superuser
@main_not_voted_or_superuser
def mainssgballot(request):
    context = {
        'title': 'Main SSG Ballot',
        'governor': MAINSSG_Candidate.objects.filter(position='Governor'),
        'vicegovernor': MAINSSG_Candidate.objects.filter(position='Vice Governor'),
        'secretary': MAINSSG_Candidate.objects.filter(position='Secretary'),
        'treasurer': MAINSSG_Candidate.objects.filter(position='Treasurer'),
        'auditor': MAINSSG_Candidate.objects.filter(position='Auditor'),
        'pio': MAINSSG_Candidate.objects.filter(position='PIO'),
        'businessmanager': MAINSSG_Candidate.objects.filter(position='Business Manager'),
        'peaceofficer': MAINSSG_Candidate.objects.filter(position='Peace Officer'),
    }
    if request.method == 'POST':
        voter = request.user
        voter.voted_main = True
        voter.save()
        sweetify.success(request, 'Vote Submitted!')
        
        

     ###### GOVERNOR ######
    try: 
        request.POST['governor']
        voted_governor = request.POST["governor"]
        g_voted = MAINSSG_Candidate.objects.get(fullname=voted_governor)
        g_voters = g_voted.voters
        g_voters.add(voter)
        receipt = Receipt.objects.get(owner=voter, department='Main Branch')
        receipt.governor = voted_governor
        receipt.save()

    except:
        print("No selected Governor")
    

    ###### VICE GOVERNOR ######
    try:
        voted_vicegovernor = request.POST["vicegovernor"]
        vg_voted = MAINSSG_Candidate.objects.get(fullname=voted_vicegovernor)
        vg_voters = vg_voted.voters
        vg_voters.add(voter)
        receipt = Receipt.objects.get(owner=voter, department='Main Branch')
        receipt.vice_governor = voted_vicegovernor
        receipt.save()


    except:
        print("No selected Vice Governor")


        ###### Secretary ######
    try:
        voted_secretary = request.POST["secretary"]
        s_voted = MAINSSG_Candidate.objects.get(fullname=voted_secretary)
        s_voters = s_voted.voters
        s_voters.add(voter)
        receipt = Receipt.objects.get(owner=voter, department='Main Branch')
        receipt.secretary = voted_secretary
        receipt.save()


    except:
        print("No selected Secretary")


            ###### Treasurer ######
    try:
        voted_treasurer = request.POST["treasurer"]
        t_voted = MAINSSG_Candidate.objects.get(fullname=voted_treasurer)
        t_voters = t_voted.voters
        t_voters.add(voter)
        receipt = Receipt.objects.get(owner=voter, department='Main Branch')
        receipt.treasurer = voted_treasurer
        receipt.save()
        
    except:
        print("No selected Treasurer")


            ###### Auditor ######
    try:
        voted_auditor = request.POST["auditor"]
        a_voted = MAINSSG_Candidate.objects.get(fullname=voted_auditor)
        a_voters = a_voted.voters
        a_voters.add(voter)
        receipt = Receipt.objects.get(owner=voter, department='Main Branch')
        receipt.auditor = voted_auditor
        receipt.save()
        
    except:
        print("No selected Auditor")


            ###### PIO ######
    try:
        voted_pio = request.POST["pio"]
        p_voted = MAINSSG_Candidate.objects.get(fullname=voted_pio)
        p_voters = p_voted.voters
        p_voters.add(voter)
        receipt = Receipt.objects.get(owner=voter, department='Main Branch')
        receipt.pio = voted_pio
        receipt.save()
        
    except:
        print("No selected PIO")


            ###### Business Manager ######
    try:
        voted_buss = request.POST["businessmanager"]
        b_voted = MAINSSG_Candidate.objects.get(fullname=voted_buss)
        b_voters = b_voted.voters
        b_voters.add(voter)
        receipt = Receipt.objects.get(owner=voter, department='Main Branch')
        receipt.businessmanager = voted_buss
        receipt.save()
        
    except:
        print("No selected Business Manager")

    
            ###### Peace Officer ######
    try:
        voted_peace = request.POST["peaceofficer"]
        p_voted = MAINSSG_Candidate.objects.get(fullname=voted_peace)
        p_voters = p_voted.voters
        p_voters.add(voter)
        receipt = Receipt.objects.get(owner=voter, department='Main Branch')
        receipt.peaceofficer = voted_peace
        receipt.save()
        return HttpResponseRedirect(reverse('receipt'))
        
    except:
        print("No selected Peace Officer")


    return render(request, 'main/mainssgballot.html', context)


@user_passes_test(lambda u: u.is_superuser)
def settings(request):
    if request.method == 'POST':
        ### MAIN ####
        try:
            reset_main = request.POST['reset_main']
            candidates = MAINSSG_Candidate.objects.all()
            for candidate in candidates:
                candidate.voters.clear()
            sweetify.toast(request, 'Main SSG Election successfully reset!')
        except:
            print('Cannot Reset Main Branch')
        try:
            delete_main = request.POST['delete_main']
            candidates = MAINSSG_Candidate.objects.all()
            for candidate in candidates:
                candidate.delete()
            sweetify.toast(request, 'Main SSG Candidates successfully deleted!')
        except:
            print('Cannot Reset Main Branch')

        
        ### CEIT ####

        try:
            reset_ceit = request.POST['reset_ceit']
            candidates = CEIT_Candidate.objects.all()
            for candidate in candidates:
                candidate.voters.clear()
            sweetify.toast(request, 'CEIT Election successfully reset!')
        except:
            print('Cannot Reset CEIT Department')
        try:
            delete_ceit = request.POST['delete_ceit']
            candidates = CEIT_Candidate.objects.all()
            for candidate in candidates:
                candidate.delete()
            sweetify.toast(request, 'CEIT Candidates successfully deleted!')
        except:
            print('Cannot Reset CEIT Department')


        
        ### CTE ####

        try:
            reset_cte = request.POST['reset_cte']
            candidates = CTE_Candidate.objects.all()
            for candidate in candidates:
                candidate.voters.clear()
            sweetify.toast(request, 'CTE Election successfully reset!')
        except:
            print('Cannot Reset CTE Department')
        try:
            delete_cte = request.POST['delete_cte']
            candidates = CTE_Candidate.objects.all()
            for candidate in candidates:
                candidate.delete()
            sweetify.toast(request, 'CTE Candidates successfully deleted!')
        except:
            print('Cannot Reset CTE Department')


        
        ### CAS ####

        try:
            reset_cas = request.POST['reset_cas']
            candidates = CAS_Candidate.objects.all()
            for candidate in candidates:
                candidate.voters.clear()
            sweetify.toast(request, 'CAS Election successfully reset!')
        except:
            print('Cannot Reset CAS Department')
        try:
            delete_cas = request.POST['delete_cas']
            candidates = CAS_Candidate.objects.all()
            for candidate in candidates:
                candidate.delete()
            sweetify.toast(request, 'CAS Candidates successfully deleted!')
        except:
            print('Cannot Reset CAS Department')

        
        ### COT ####
        
        try:
            reset_cot = request.POST['reset_cot']
            candidates = COT_Candidate.objects.all()
            for candidate in candidates:
                candidate.voters.clear()
            sweetify.toast(request, 'COT Election successfully reset!')
        except:
            print('Cannot Reset COT Department')
        try:
            delete_cot = request.POST['delete_cot']
            candidates = COT_Candidate.objects.all()
            for candidate in candidates:
                candidate.delete()
            sweetify.toast(request, 'COT Candidates successfully deleted!')
        except:
            print('Cannot Reset COT Department')
        

    context = {
        'title': 'Settings'
    }
    return render(request, 'main/settings.html', context)