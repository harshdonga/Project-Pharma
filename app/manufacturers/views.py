from django.shortcuts import render
from django.http import HttpResponse
import getpass
import datetime
import pkg_resources
import traceback
import sys
sys.path.insert(0, '/home/harsh/project/med_python')

from med_python.sawtooth_med.med_client import MedClient


DEFAULT_URL = 'http://127.0.0.1:8008'

def _get_keyfile(args):
    username = args
    home = os.path.expanduser("~")
    key_dir = os.path.join(home, ".sawtooth", "keys")

    return '{}/{}.priv'.format(key_dir, username)

def index(request):
    return render(request, 'index.html')

def task(request):
    options = request.POST['options']
    if options == 'med':
        return render(request, 'med.html')
    else:
        return render(request, 'transfer.html')

def medtransact(request):
    func = request.POST['func']
    medicineName = request.POST['medicineName']
    medicineID = request.POST['medicineID']
    medicineKeyContent = request.POST['medicineKeyContent']
    medicineAllContents = request.POST['medicineAllContents']
    expiryMonths = request.POST['expiryMonths']
    uname = request.POST['uname']
    wait = request.POST['wait']
    
    manufactureDate = datetime.date.today()
    expiryDate = manufactureDate + datetime.timedelta((args.expirymonths)*365/12)

    keyfile = _get_keyfile(uname)
    url = DEFAULT_URL
    
    if func == 'createMedicine':
        client = MedClient(base_url = url , keyfile= keyfile)
        if wait and wait > 0:
            response = client.createMedicine(
                medicineName,
                medicineID,
                medicineKeyContent,
                medicineAllContents,
                manufactureDate,
                expiryDate,
                stock = 0,
                wait = wait,
                auth_user = None,
                auth_password = None
            )
        else:
            response = client.createMedicine(
                medicineName,
                medicineID,
                medicineKeyContent,
                medicineAllContents,
                manufactureDate,
                expiryDate,
                stock = 0,
                auth_user = None,
                auth_password = None
            )
        print("Response : {}".format(response))


    return render(request, 'test.html', {'response': response})


