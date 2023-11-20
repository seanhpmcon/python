from ast import Dict, List
from typing import Any
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template import loader
import pandas as pd
from .funcs import remove_emp, string_to_list, remove_excel_emp, remove_by_clock, get_areas, enroll_emp, upload_enrollf
from .forms import UploadFileForm, BootstrapErrorList


# Create your views here.
#unenrollment
@csrf_exempt
def input_unenroll(request):
    if request.method == 'POST':
        badges: str = request.POST.get('badges')
        list_of_badges: List[int] = string_to_list(badges)
        for badge in list_of_badges:
            remove_emp(badge, request.session['ldap_name'])
    template: Any = loader.get_template('home.html')
    return HttpResponse(template.render())


@csrf_exempt
def upload_unenroll(request):
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


@csrf_exempt
def clock_unenroll(request):
    if request.method == 'POST':
        clock: str = request.POST.get('clock')
        remove_by_clock(int(clock))
    clocks: Dict[int, str] = get_areas()
    return render(request, 'clock_unenroll.html', {'clocks': clocks})


#enrollment
@csrf_exempt
def emp_enroll(request):
    if request.method == 'POST':
        badges: str = request.POST.get('badges')
        enroll_emp(badges)
    template: Any = loader.get_template('emp_enroll.html')
    return HttpResponse(template.render())

@csrf_exempt
def upload_enroll(request):
    if request.method == 'POST':
        form: UploadFileForm = UploadFileForm(request.POST, request.FILES, error_class=BootstrapErrorList)
        if form.is_valid():
            excel_file = request.FILES['file']
            df: pd.DataFrame = pd.read_excel(excel_file)
            upload_enrollf(df)
            return render(request, 'success.html')
    else:
        form: UploadFileForm = UploadFileForm()
    return render(request, 'upload_enroll.html', {'form': form})