from django.shortcuts import render, redirect

# Create your views here.
def homepage(request):
    if request.user.is_authenticated:
        return render(request, 'pages/homepage.html')
    else:
        return redirect('/login')


def uploadPrescription(request):

    if request.user.is_authenticated:
        return render(request, 'pages/uploadPrescription.html')
    else:
        return redirect('login')

def viewPrescription(request):

    if request.user.is_authenticated:
        return render(request, 'pages/viewPrescription.html')
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