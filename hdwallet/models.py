from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.contrib.auth.models import User

class HDProfile(models.Model):

    class Meta:
        verbose_name = _("hdprofile")
        verbose_name_plural = _("hdprofiles")

    user = models.ForeignKey(User, verbose_name=_("user"))
    masterExtendedPubKey = models.TextField(_("MasterExtendedPubKey"), null=True, blank=True)
    bip32Index = models.CharField(_("BIP32Index"), max_length=256, null=True, blank=True)
    walletAddress = models.URLField(_("WalletAddress"), null=True, blank=True )


class HDProfileAdmin(admin.ModelAdmin):
    list_display = ('user','masterExtendedPubKey','bip32Index', 'walletAddress' )
    search_fields = ('user','masterExtendedPubKey','bip32Index', 'walletAddress' )

admin.site.register(HDProfile,HDProfileAdmin)

