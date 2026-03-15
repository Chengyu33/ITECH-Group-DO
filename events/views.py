from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def event_register(request, event_id):
    ...

@login_required
def create_event(request):
    ...