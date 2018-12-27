from django.shortcuts import render
from django.http.response import HttpResponse

# Create your views here.
def ctf_main(request):
    return render(request, 'main/main.html')