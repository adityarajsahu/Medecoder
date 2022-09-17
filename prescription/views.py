from django.shortcuts import render, redirect

# Create your views here.
def homepage(request):
    if request.user.is_authenticated:
        return render(request, 'pages/homepage.html')
    else:
        return redirect('/login')