from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'index.html')

def task(request):
    options = request.POST['options']
    if options == 'med':
        return render(request, 'med.html')
    else:
        return render(request, 'transfer.html')

def medtransact(request):
    medicineName = request.POST['medicineName']
    medicineName = request.POST['medicineId']
    medicineName = request.POST['medicineKeyContent']
    medicineName = request.POST['medicineAllContents']
    medicineName = request.POST['ExpiryMonths']
