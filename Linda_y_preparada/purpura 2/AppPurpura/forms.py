from django import forms
from.models import registro

class RegistroUsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = registro
        fields = '__all__'