from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def welcome(request):
    return render(request, 'welcome.html')