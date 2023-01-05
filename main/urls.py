from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('receipt', views.receipt, name='receipt'),
    path('settings', views.settings, name='settings'),
    path('profile/<str:pk>', views.profile, name='profile'),

    path('voters', views.voters, name='voters'),
    path('voters/update/<str:pk>', views.updatevoter, name='updatevoter'),
    path('voters/delete/<str:pk>', views.deletevoter, name='deletevoter'),

    path('election/schedule', views.electionschedule, name='electionschedule'),
    path('election/schedule/update/<str:pk>', views.updateelectionschedule, name='updateelectionschedule'),
    path('election/schedule/delete/<str:pk>', views.deleteelectionschedule, name='deleteelectionschedule'),
    
    path('mainssg', views.mainssgballot, name='mainssg'),
    path('mainssg/candidates', views.mainssgcandidates, name='mainssgcandidates'),
    path('mainssg/tally', views.mainssgtally, name='mainssgtally'),
    path('mainssg/result', views.mainssgresult, name='mainssgresult'),
    path('mainssg/candidate/update/<str:pk>', views.updatemainssgcandidate, name='updatemainssgcandidate'),
    path('mainssg/candidate/delete/<str:pk>', views.deletemainssgcandidate, name='deletemainssgcandidate'),

    path('ceit/ballot', views.ceitballot, name='ceitballot'),
    path('ceit/candidates', views.ceitcandidates, name='ceitcandidates'),
    path('ceit/tally', views.ceittally, name='ceittally'),
    path('ceit/result', views.ceitresult, name='ceitresult'),
    path('ceit/candidate/update/<str:pk>', views.updateceitcandidate, name='updateceitcandidate'),
    path('ceit/candidate/delete/<str:pk>', views.deleteceitcandidate, name='deleteceitcandidate'),


    path('cte/ballot', views.cteballot, name='cteballot'),
    path('cte/candidates', views.ctecandidates, name='ctecandidates'),
    path('cte/tally', views.ctetally, name='ctetally'),
    path('cte/result', views.cteresult, name='cteresult'),
    path('cte/candidate/update/<str:pk>', views.updatectecandidate, name='updatectecandidate'),
    path('cte/candidate/delete/<str:pk>', views.deletectecandidate, name='deletectecandidate'),


    path('cas/ballot', views.casballot, name='casballot'),
    path('cas/candidates', views.cascandidates, name='cascandidates'),
    path('cas/tally', views.castally, name='castally'),
    path('cas/result', views.casresult, name='casresult'),
    path('cas/candidate/update/<str:pk>', views.updatecascandidate, name='updatecascandidate'),
    path('cas/candidate/delete/<str:pk>', views.deletecascandidate, name='deletecascandidate'),


    path('cot/ballot', views.cotballot, name='cotballot'),
    path('cot/candidates', views.cotcandidates, name='cotcandidates'),
    path('cot/tally', views.cottally, name='cottally'),
    path('cot/result', views.cotresult, name='cotresult'),
    path('cot/candidate/update/<str:pk>', views.updatecotcandidate, name='updatecotcandidate'),
    path('cot/candidate/delete/<str:pk>', views.deletecotcandidate, name='deletecotcandidate'),
    
]
