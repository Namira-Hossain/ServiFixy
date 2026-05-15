from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=[
        ('customer', 'Customer'),
        ('worker', 'Worker'),
    ])
    phone = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea)
    profile_image = forms.ImageField(required=False)
    nid = forms.CharField(max_length=20, required=False)
    nid_image = forms.ImageField(required=False)
    is_female = forms.BooleanField(required=False)
    # worker only
    experience = forms.IntegerField(required=False)
    pricing = forms.DecimalField(
        required=False,
        max_digits=8,
        decimal_places=2
    )

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)