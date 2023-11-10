from django import forms
from django.core.validators import FileExtensionValidator
from django.forms.utils import ErrorList

# This class is to instantiate a form to take in a file field.
class UploadFileForm(forms.Form):
    file = forms.FileField(validators=[FileExtensionValidator(['xlsx', 'xls'])])
    
# This class is for returning a specific error when a different file type is added.
class BootstrapErrorList(ErrorList):
    def __str__(self):
        if not self: return ''
        return ''.join([f'<div class="alert alert-danger" role="alert">{error}</div>' for error in self])