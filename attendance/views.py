from ast import List
from typing import Any
from django.shortcuts import render
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template import loader
import pandas as pd
from .funcs import remove_emp, string_to_list, remove_excel_emp
from .forms import UploadFileForm, BootstrapErrorList


# Create your views here.
@csrf_exempt
def home(request):
    if request.method == 'POST':
        badges: str = request.POST.get('badges')
        list_of_badges: List[int] = string_to_list(badges)
        for badge in list_of_badges:
            remove_emp(badge, request.session['ldap_name'])
    template = loader.get_template('home.html')
    return HttpResponse(template.render())


@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        form: UploadFileForm = UploadFileForm(request.POST, request.FILES, error_class=BootstrapErrorList)
        if form.is_valid():
            excel_file = request.FILES['file']
            df: pd.DataFrame = pd.read_excel(excel_file)
            df.apply(remove_excel_emp, axis=1, user=request.session['ldap_name'])
            return render(request, 'success.html')
    else:
        form: UploadFileForm = UploadFileForm()
    return render(request, 'upload.html', {'form': form})