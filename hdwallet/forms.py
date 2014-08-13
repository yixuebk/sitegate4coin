from django.forms import *
from hdwallet.models import *
from hdwallet.utils import *



class HDWalletForm(ModelForm):
    class Meta:
        model = HDProfile
        #widgets = {'masterExtendedPubKey': TextInput(attrs={'size':128}), }
        exclude = ('user')

    def clean_masterExtendedPubKey(self):
        data = self.cleaned_data['masterExtendedPubKey']
        if len(data) != 0 :
            validate_extended_key(data)

        return data
