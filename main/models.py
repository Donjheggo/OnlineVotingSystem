from django.db import models
from account.models import *
import datetime
import string, secrets


def modalID_generator():
    alphabet = string.ascii_letters
    modalID = ''.join(secrets.choice(alphabet) for i in range(10))
    return modalID


class votingschedule(models.Model):
    department = models.TextField(choices=(
        ('Main','Main'),
        ('CEIT','CEIT'),
        ('CTE','CTE'),
        ('CAS','CAS'),
        ('COT','COT'),
        ), null=True)
    start = models.DateField()
    end = models.DateField()

    def __str__(self):
        return f"{self.department}"

class MAINSSG_Candidate(models.Model):
    modal_id = models.CharField(max_length=50, editable=False, default=modalID_generator)
    fullname = models.CharField(max_length=50)
    photo = models.ImageField(upload_to="candidates", blank=True)
    bio = models.TextField(null=True)
    position = models.TextField(choices=(
        ('Governor','Governor'),
        ('Vice Governor', 'Vice Governor'),
        ('Secretary','Secretary'),
        ('Treasurer','Treasurer'),
        ('Auditor','Auditor'),
        ('PIO','PIO'),
        ('Business Manager','Business Manager'),
        ('Peace Officer','Peace Officer'),
        ), null=True)
    voters = models.ManyToManyField(Account, blank=True)


    # def voterlist(self):
    #     list = self.voters
    #     converted = ','.join([str(elem) for elem in list])
    #     return converted
        
    def photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        else:
            return "/static/sb_admin/img/user.png"
    
    def __str__(self):
        return f"{self.fullname}"



class CEIT_Candidate(models.Model):
    modal_id = models.CharField(max_length=50, editable=False, default=modalID_generator)
    fullname = models.CharField(max_length=50)
    photo = models.ImageField(upload_to="candidates", blank=True)
    bio = models.TextField(null=True)
    position = models.TextField(choices=(
        ('Governor','Governor'),
        ('Vice Governor', 'Vice Governor'),
        ('Secretary','Secretary'),
        ('Treasurer','Treasurer'),
        ('Auditor','Auditor'),
        ('PIO','PIO'),
        ('Business Manager','Business Manager'),
        ('Peace Officer','Peace Officer'),
        ), null=True)
    voters = models.ManyToManyField(Account, blank=True)

        
    def photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        else:
            return "/static/sb_admin/img/user.png"


    def __str__(self):
        return f"{self.fullname}"


class CTE_Candidate(models.Model):
    modal_id = models.CharField(max_length=50, editable=False, default=modalID_generator)
    fullname = models.CharField(max_length=50)
    photo = models.ImageField(upload_to="candidates", blank=True)
    bio = models.TextField(null=True)
    position = models.TextField(choices=(
        ('Governor','Governor'),
        ('Vice Governor', 'Vice Governor'),
        ('Secretary','Secretary'),
        ('Treasurer','Treasurer'),
        ('Auditor','Auditor'),
        ('PIO','PIO'),
        ('Business Manager','Business Manager'),
        ('Peace Officer','Peace Officer'),
        ), null=True)
    voters = models.ManyToManyField(Account, blank=True)

        
    def photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        else:
            return "/static/sb_admin/img/user.png"
    
    def __str__(self):
        return f"{self.fullname}"


class CAS_Candidate(models.Model):
    modal_id = models.CharField(max_length=50, editable=False, default=modalID_generator)
    fullname = models.CharField(max_length=50)
    photo = models.ImageField(upload_to="candidates", blank=True)
    bio = models.TextField(null=True)
    position = models.TextField(choices=(
        ('Governor','Governor'),
        ('Vice Governor', 'Vice Governor'),
        ('Secretary','Secretary'),
        ('Treasurer','Treasurer'),
        ('Auditor','Auditor'),
        ('PIO','PIO'),
        ('Business Manager','Business Manager'),
        ('Peace Officer','Peace Officer'),
        ), null=True)
    voters = models.ManyToManyField(Account, blank=True)

        
    def photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        else:
            return "/static/sb_admin/img/user.png"
    
    def __str__(self):
        return f"{self.fullname}"


class COT_Candidate(models.Model):
    modal_id = models.CharField(max_length=50, editable=False, default=modalID_generator)
    fullname = models.CharField(max_length=50)
    photo = models.ImageField(upload_to="candidates", blank=True)
    bio = models.TextField(null=True)
    position = models.TextField(choices=(
        ('Governor','Governor'),
        ('Vice Governor', 'Vice Governor'),
        ('Secretary','Secretary'),
        ('Treasurer','Treasurer'),
        ('Auditor','Auditor'),
        ('PIO','PIO'),
        ('Business Manager','Business Manager'),
        ('Peace Officer','Peace Officer'),
        ), null=True)
    voters = models.ManyToManyField(Account, blank=True)

        
    def photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        else:
            return "/static/sb_admin/img/user.png"
    
    def __str__(self):
        return f"{self.fullname}"



class Receipt(models.Model):
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    department = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    governor = models.CharField(max_length=50, blank=True, null=True)
    vice_governor = models.CharField(max_length=50, blank=True, null=True)
    secretary = models.CharField(max_length=50, blank=True, null=True)
    treasurer = models.CharField(max_length=50, blank=True, null=True)
    auditor = models.CharField(max_length=50, blank=True, null=True)
    pio = models.CharField(max_length=50, blank=True, null=True)
    businessmanager = models.CharField(max_length=50, blank=True, null=True)
    peaceofficer = models.CharField(max_length=50, blank=True, null=True)

    def get_owner(self):
        return self.owner.email

    def __str__(self):
        return f"{self.owner}"