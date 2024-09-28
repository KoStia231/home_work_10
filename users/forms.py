from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

from users.models import User


class CustomFormMixin:
    """Стилизация внешнего вида формы"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class UserRegisterForm(CustomFormMixin, UserCreationForm):
    # Наследуемся от специальной формы UserCreationForm из модуля auth
    class Meta:
        model = User
        # Указываем новую кастомную модель
        fields = ('first_name', 'email', 'password1', 'password2')
        # Меняем поля, так как исходная форма UserCreationForm
        # ссылается на поле username


class UserLoginForm(CustomFormMixin, AuthenticationForm):
    class Meta:
        model = User
        fields = ('email', 'password')


class UserProfileUpdateForm(CustomFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'phone_number',
                  'first_name', 'last_name', 'new_password'
                  )

    def __init__(self, *args, **kwargs):
        """Штука скрывает стандартное поле пароля"""
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()


class UserProfileUpdateFormManager(UserProfileUpdateForm):
    class Meta:
        model = User
        fields = ('is_active',)

