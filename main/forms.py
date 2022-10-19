from django import forms
from pkg_resources import require
from .models import *

class CEIT_CandidatesForm(forms.ModelForm):
   class Meta:
      model = CEIT_Candidate
      exclude = ('voters',)
      fields = ('fullname', 'photo', 'bio', 'position')
      position_choices = (
        ('Governor','Governor'),
        ('Vice_Governor', 'Vice Governor'),
        ('Secretary','Secretary'),
        ('Treasurer','Treasurer'),
        ('Auditor','Auditor'),
        ('PIO','PIO'),
        ('Business_Manager','Business Manager'),
        ('Peace_Officer','Peace Officer'),
      )
      widgets = {
         'photo': forms.FileInput(attrs={'type': 'file'}),
         'fullname':forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder':'Full name' }),
         'bio':forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Tell us about yourself and your motto' }),
         'position':forms.Select(choices=position_choices,attrs={'class': 'form-control', 'placeholder':'Position' }),
      }

class CTE_CandidatesForm(forms.ModelForm):
   class Meta:
      model = CTE_Candidate
      exclude = ('voters',)
      fields = ('fullname', 'photo', 'bio', 'position')
      position_choices = (
        ('Governor','Governor'),
        ('Vice_Governor', 'Vice Governor'),
        ('Secretary','Secretary'),
        ('Treasurer','Treasurer'),
        ('Auditor','Auditor'),
        ('PIO','PIO'),
        ('Business_Manager','Business Manager'),
        ('Peace_Officer','Peace Officer'),
      )
      widgets = {
         'photo': forms.FileInput(attrs={'type': 'file'}),
         'fullname':forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder':'Full name' }),
         'bio':forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Tell us about yourself and your motto' }),
         'position':forms.Select(choices=position_choices,attrs={'class': 'form-control', 'placeholder':'Position' }),
      }



class CAS_CandidatesForm(forms.ModelForm):
   class Meta:
      model = CAS_Candidate
      exclude = ('voters',)
      fields = ('fullname', 'photo', 'bio', 'position')
      position_choices = (
        ('Governor','Governor'),
        ('Vice_Governor', 'Vice Governor'),
        ('Secretary','Secretary'),
        ('Treasurer','Treasurer'),
        ('Auditor','Auditor'),
        ('PIO','PIO'),
        ('Business_Manager','Business Manager'),
        ('Peace_Officer','Peace Officer'),
      )
      widgets = {
         'photo': forms.FileInput(attrs={'type': 'file'}),
         'fullname':forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder':'Full name' }),
         'bio':forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Tell us about yourself and your motto' }),
         'position':forms.Select(choices=position_choices,attrs={'class': 'form-control', 'placeholder':'Position' }),
      }


class COT_CandidatesForm(forms.ModelForm):
   class Meta:
      model = COT_Candidate
      exclude = ('voters',)
      fields = ('fullname', 'photo', 'bio', 'position')
      position_choices = (
        ('Governor','Governor'),
        ('Vice_Governor', 'Vice Governor'),
        ('Secretary','Secretary'),
        ('Treasurer','Treasurer'),
        ('Auditor','Auditor'),
        ('PIO','PIO'),
        ('Business_Manager','Business Manager'),
        ('Peace_Officer','Peace Officer'),
      )
      widgets = {
         'photo': forms.FileInput(attrs={'type': 'file'}),
         'fullname':forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder':'Full name' }),
         'bio':forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Tell us about yourself and your motto' }),
         'position':forms.Select(choices=position_choices,attrs={'class': 'form-control', 'placeholder':'Position' }),
      }


class MAINSSG_CandidatesForm(forms.ModelForm):
   class Meta:
      model = MAINSSG_Candidate
      exclude = ('voters',)
      fields = ('fullname', 'photo', 'bio', 'position')
      position_choices = (
        ('Governor','Governor'),
        ('Vice_Governor', 'Vice Governor'),
        ('Secretary','Secretary'),
        ('Treasurer','Treasurer'),
        ('Auditor','Auditor'),
        ('PIO','PIO'),
        ('Business_Manager','Business Manager'),
        ('Peace_Officer','Peace Officer'),
      )
      widgets = {
         'photo': forms.FileInput(attrs={'type': 'file'}),
         'fullname':forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder':'Full name' }),
         'bio':forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Tell us about yourself and your motto' }),
         'position':forms.Select(choices=position_choices,attrs={'class': 'form-control', 'placeholder':'Position' }),
      }


class ScheduleForm(forms.ModelForm):
   class Meta:
      model = votingschedule
      fields = ('department', 'start', 'end')
      widgets = {
         'department':forms.Select(attrs={'class': 'form-control' }),
         'start':forms.TextInput(attrs={'type': 'date','class': 'form-control' }),
         'end':forms.TextInput(attrs={'type': 'date','class': 'form-control' }),
      }


class UpdateScheduleForm(forms.ModelForm):
   class Meta:
      model = votingschedule
      exclude = ('department',)
      fields = ('start', 'end')
      widgets = {
         'start':forms.TextInput(attrs={'type': 'date','class': 'form-control' }),
         'end':forms.TextInput(attrs={'type': 'date','class': 'form-control' }),
      }


