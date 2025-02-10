from django.contrib.auth.forms import UserCreationForm
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import PasswordResetForm
import logging

logger = logging.getLogger(__name__)

class DebugPasswordResetForm(PasswordResetForm):
    def save(self, *args, **kwargs):
        # Log the email from the form
        email = self.cleaned_data.get('email')
        users = list(self.get_users(email))
        logger.debug("Password reset requested for email: %s", email)
        logger.debug("Found %d user(s) for that email.", len(users))
        # Continue with the normal save, which sends the email if users exist.
        return super().save(*args, **kwargs)
class CustomErrorList(ErrorList):
    def __str__(self):
        if not self:
            return ''
        return mark_safe(''.join([
            f'<div class="alert alert-danger" role="alert">{e}</div>' for e in self]))
class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__ (*args, **kwargs)
        for fieldname in ['username', 'password1',
        'password2']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs.update(
                {'class': 'form-control'}
            )