from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect

# Create your views here.

@csrf_exempt
def login(request):
    if request.method == 'POST':
        pass
    if request.GET.get('login'):
        fail = True
    else:
        fail = False
    return render(request, 'login.html', {'fail': fail})

@csrf_exempt
def logout(request):
    del request.session['ldap_name']
    return redirect('/auth/login')