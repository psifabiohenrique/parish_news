from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'church', 'is_staff', 'groups')  # Inclua todos os campos que você quer no formulário

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Pegue o usuário da requisição
        super().__init__(*args, **kwargs)
        if user and not user.is_superuser:
            # Filtra as igrejas para mostrar apenas a igreja do usuário logado
            self.fields['church'].queryset = user.church.objects.filter(pk=user.church.pk)