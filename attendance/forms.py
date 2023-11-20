from typing import Self
from django import forms
from ast import Dict, List, Tuple
from django.core.validators import FileExtensionValidator
from django.forms.utils import ErrorList
from django.forms import FileInput
from .funcs import get_areas

# This class is to instantiate a form to take in a file field.
class UploadFileForm(forms.Form):
    file = forms.FileField(validators=[FileExtensionValidator(['xlsx', 'xls'])], widget=FileInput(attrs={'placeholder': 'Name', 'style': 'width: 300px;', 'class': 'form-control'}))
    
# This class is for returning a specific error when a different file type is added.
class BootstrapErrorList(ErrorList):
    def __str__(self):
        if not self: 
            return ''
        return ''.join([f'<div class="alert alert-danger" role="alert">{error}</div>' for error in self])
    
# Choices
class UploadClockForm(forms.Form):
    def clocks():
        clock_dict: Dict[int, str] = get_areas()
        clock_list: List[Tuple[any]] = [(k, v) for k, v in clock_dict.items()]
        return clock_list
    
    clock = forms.ChoiceField(choices=clocks)
    file = forms.FileField(validators=[FileExtensionValidator(['xlsx', 'xls'])], widget=FileInput(attrs={'placeholder': 'Name', 'style': 'width: 300px;', 'class': 'form-control'}))