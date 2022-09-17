from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm

# Create your views here.
def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None

    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = "Invalid Credentials"
        else:
            msg = "Error Validating Form Data"
        
    context = {
        "form": form,
        "msg": msg
    }
        
    return render(request, "pages/login_page.html", context=context)

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('/login')
    msg = None
    success = None
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            msg = 'User created - please <a href="/login/">login</a>.'
            success = True
            # return redirect("/login/")
        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()
    
    context = {
        'form': form,
        'msg' : msg
    }
    return render(request, 'pages/signup_page.html', context=context)
