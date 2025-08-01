from django.contrib import admin
from .models import Membership, MembershipPlan
# Register your models here.
admin.site.register(Membership)
admin.site.register(MembershipPlan)