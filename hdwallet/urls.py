from django.conf.urls.defaults import *
from views import *


urlpatterns = patterns("",
    url(r'^$', hdwallet_display_master_pubkey, name='hdwallet-display-master-pubkey'),
    url(r'^nxtkey/$', hdwallet_display_nxt_pubkey, name='hdwallet-display-nxt-pubkey'),
    url(r'^savetoprofile/$', hdwallet_save_to_profile, name='hdwallet-save-to-profile'),
    #url(r'^newfromserver/$', hdwallet_new_from_server, name='hdwallet-new-from-server'),
    url(r'^newfromjs/$', hdwallet_new_from_js,   name='hdwallet-new-from-js'),
    url(r'^edithdp/$', hdwallet_edit_hdprofile, name='hdwallet-edit-hdprofile'),
)
