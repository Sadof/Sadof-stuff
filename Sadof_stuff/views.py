from django.urls import reverse
from django.shortcuts import render ,redirect
from django.views.generic.edit import FormView



def IndexView(request):
    return  render(request,"index.html")

