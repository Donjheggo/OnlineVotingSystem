from django.contrib import admin
from .models import *

admin.site.register(votingschedule)

admin.site.register(MAINSSG_Candidate)

admin.site.register(CEIT_Candidate)

admin.site.register(CTE_Candidate)

admin.site.register(CAS_Candidate)

admin.site.register(COT_Candidate)


admin.site.register(Receipt)