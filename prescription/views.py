from django.shortcuts import render, redirect
from .models import Prescription

# Create your views here.
def homepage(request):
    if request.user.is_authenticated:
        return render(request, 'pages/homepage.html')
    else:
        return redirect('/login')


def uploadPrescription(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'pages/uploadPrescription.html')
        elif request.method == 'POST':
            image = request.FILES['prescription_image']
            obj = Prescription(uploaded_by=request.user, image=image)
            obj.save()
            return redirect('prescriptions')
    else:
        return redirect('login')

def viewPrescription(request):

    if request.user.is_authenticated:
        context = {
            'prescriptions' : Prescription.objects.all(),
        }
        return render(request, 'pages/viewPrescription.html', context=context)
    else:
        return redirect('login')

def Prescriptions(request):

    if request.user.is_authenticated:
        return render(request, 'pages/prescriptions.html')
    else:
        return redirect('login')

def Dashboard(request):

    if request.user.is_authenticated:
        return render(request, 'pages/dashboard.html')
    else:
        return redirect('login')


def singleView(request, prescription_id):
    if request.user.is_authenticated:
        context = {
            'prescription': Prescription.objects.get(id=prescription_id),
        }
        return render(request, 'pages/singleView.html', context=context)
    else:
        return redirect('login')

def annotatePrescription(request, prescription_id):
    if request.user.is_authenticated:
        context = {
            'prescription': Prescription.objects.get(id=prescription_id),
        }
        return render(request, 'annotator/via.html', context=context)
    else:
        return redirect("login")