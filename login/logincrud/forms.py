from django import forms
from .models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

class UserForm(forms.ModelForm):
    """duplicate email id and employee_id"""
    def clean_employee_id(self):
        print("employee_id hitted")
        employee_id = self.cleaned_data.get("employee_id")
        if employee_id and User.objects.filter(employee_id = employee_id).exclude(id=self.instance.pk or 0).exists():
            raise ValidationError("Employee Id already exists")
        return employee_id
    def clean_email_id(self):
        print("email_id hitted ")
        email_id = self.cleaned_data.get("email_id")
        if email_id and User.objects.filter(email_id=email_id).exclude(id=self.instance.pk or 0).exists():
            raise ValidationError("This email is already exists")
        return email_id
    class Meta:
        model = User
        fields = ['user_role','user_name','department','email_id','is_active','is_locked','employee_id','designation','mobile_number','remarks1','remarks2']
    email_regex = RegexValidator(regex=r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    string_regex =  RegexValidator(regex=r'^[a-zA-Z]+(?:\s[a-zA-Z]+)*$', message="Some special characters like (~!#^`'$|{}<>*) are not allowed.")
    mobile_validate = RegexValidator(regex=r'^(\+\d{1,3})?\d{10}$',message='Enter a valid 10-digit mobile number')
    id_regex = RegexValidator(regex=r'([A-Za-z0-9]+[.-_])',message='enter valid id')
    user_name = forms.CharField(
        max_length=100,
        validators=[string_regex]
        )
    email_id = forms.EmailField(
        max_length = 300,
        validators = [email_regex]
    )
    employee_id = forms.CharField(
        max_length=200,
        validators = [id_regex]
    )
    mobile_number = forms.CharField(
        max_length=12,
        validators=[mobile_validate]
    )
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['user_name'].initial = ''
        self.fields['employee_id'].initial = ''
        self.fields['email_id'].initial = ''
        self.fields['mobile_number'].initial = ''


class ImageUploadForm(forms.Form):
    image = forms.ImageField()

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if not image.content_type.startswith('image/'):
                raise forms.ValidationError('Invalid file type. Only images are allowed.')
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Image file too large ( > 5MB ).')
        return image

"""def clean_email_id(self):
    email_id = self.cleaned_data.get("email_id")
    if email_id and User.objects.filter(email_id=email_id).exclude(id=self.instance.pk or 0).exists():
        raise ValidationError("This email is already in use. Please choose a different one.")
    return email_id

def clean_employee_id(self):
    employee_id = self.cleaned_data.get("employee_id")
    if employee_id and User.objects.filter(employee_id=employee_id).exclude(id=self.instance.pk or 0).exists():
        raise ValidationError("Employee ID already exists.")
    return employee_id
"""

