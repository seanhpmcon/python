from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
import pandas as pd
from .funcs import remove_emp, string_to_list
from .forms import UploadFileForm, BootstrapErrorList


# Create your views here.
@csrf_exempt
@api_view(['POST'])
def remove_employees(request, response):
    badge = request.data
    remove_emp(badge["badges"], request.session['ldap_name'])
    return Response(badge, status=status.HTTP_200_OK)


@csrf_exempt
def home(request):
    if request.method == 'POST':
        badges = request.POST.get('badges')
        list_of_badges = string_to_list(badges)
        for badge in list_of_badges:
            remove_emp(badge, request.session['ldap_name'])
    template = loader.get_template('home.html')
    return HttpResponse(template.render())


@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES, error_class=BootstrapErrorList)
        if form.is_valid():
            excel_file = request.FILES['file']
            data_frame = pd.read_excel(excel_file)
            return render(request, 'success.html')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

@csrf_exempt
def test(request):
    un = request.session['ldap_name']
    return render(request, 'test.html', {'un': un})