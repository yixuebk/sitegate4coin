import random,time,string
import smtplib
from email.mime.text import MIMEText
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render_to_response, HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from django.db.models import Sum,F
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from hdwallet.models import *
from hdwallet.forms import *
from hdwallet.utils import *


from bip32utils import *


@login_required
def hdwallet_display_master_pubkey(request):

    username=request.user

    u = get_object_or_404(User, username=username)
    hdpList = HDProfile.objects.filter(user=u)
    if hdpList.count() == 0 :
      return HttpResponseRedirect(reverse('hdwallet-new-from-js')) 
      
    hdp = hdpList[0]
    masterPubKeyStr=str(hdp.masterExtendedPubKey) 
    thirdLevelIndex=long(hdp.bip32Index) 

    childKey={}
    childKey["masterPubKey"]=masterPubKeyStr
    childKey["index"]=thirdLevelIndex
 
    return render_to_response('hdwallet_display_cur_pubkey.html',
            {'ChildKey':childKey},
            context_instance=RequestContext(request))


@login_required
def hdwallet_display_nxt_pubkey(request):

    #masterPubKeyStr = "xpub661MyMwAqRbcFtXgS5sYJABqqG9YLmC4Q1Rdap9gSE8NqtwybGhePY2gZ29ESFjqJoCu1Rupje8YtGqsefD265TMg7usUDFdp6W1EGMcet8" 

    username=request.user
    childKey=next_pub_address(username)

    return render_to_response('hdwallet_display_nxt_pubkey.html',
            {'ChildKey':childKey},
            context_instance=RequestContext(request))

# privatekey generate from server side, as a backup, not currently used, lming 2014/06/21
@login_required
def hdwallet_new_from_server(request):

    #entropy = "000102030405060708090A0B0C0D0E0F"
    entropy = ''.join(random.choice(string.hexdigits) for n in xrange(32))
    masterPrivate=BIP32Key.fromEntropy(entropy, public=False)
    masterPubKeyStr = masterPrivate.ExtendedKey(private=False,encoded=True)
    firstLevelIndex=775
    thirdLevelIndex=5
    #child=masterPrivate.ChildKey(i)
    child=masterPrivate.ChildKey(firstLevelIndex).ChildKey(0).ChildKey(thirdLevelIndex)
    childExtendedPubKey = child.ExtendedKey(private=False,encoded=True)
    childPubKey = child.PublicKey().encode('hex')
    childKey={}
    childKey["masterPubKey"]=masterPubKeyStr
    childKey["extendedPubKey"]=childExtendedPubKey
    childKey["PubKey"]=childPubKey
    childKey["index"]=thirdLevelIndex
    return render_to_response('hdwallet_display_nxt_pubkey.html',
            {'ChildKey':childKey},
            context_instance=RequestContext(request))


# privatekey generate from client side javascript, lming 2014/06/22
@login_required
def hdwallet_new_from_js(request):

    return render_to_response('hdwallet_new_from_js.html',
            context_instance=RequestContext(request))



@login_required
def hdwallet_save_to_profile(request):

    username=request.user

    u = get_object_or_404(User, username=username)

    masterPubKeyStr = "" 
    if 'bip32_pub_source_key' in request.POST and request.POST['bip32_pub_source_key']:
        masterPubKeyStr = request.POST['bip32_pub_source_key'] 

    validate_extended_key(masterPubKeyStr)

    hdpList = HDProfile.objects.filter(user=u)
    if hdpList.count() == 0 :
        hdp = HDProfile()
        hdp.user=u
        hdp.masterExtendedPubKey=masterPubKeyStr
        hdp.bip32Index=0
        hdp.save() 
    else :
        hdp=hdpList[0]
        hdp.masterExtendedPubKey=masterPubKeyStr
        hdp.bip32Index=0
        hdp.save() 
         

    return HttpResponseRedirect(reverse('hdwallet-display-master-pubkey'))



@login_required
def hdwallet_edit_hdprofile(request,template_name = 'edit_hdprofile.html'):

    username=request.user
    u = get_object_or_404(User, username=username)

    hdpList = HDProfile.objects.filter(user=u)

    textDict = {"formtitle":"Edit", "buttontitle":"Save"}

    if request.method == 'POST':
      if ( hdpList.count() == 0 ) : # new profile
        newForm = HDWalletForm(request.POST)
      else : # profile exists, replace it
        newForm = HDWalletForm(request.POST,instance=hdpList[0])

      if newForm.is_valid():
        f = newForm.save(commit=False)
        f.user = request.user
        f.save()


        return HttpResponseRedirect(reverse('hdwallet-display-master-pubkey'))
      else : # if form not validated
        return render_to_response(template_name, {'textDict':textDict,'form':newForm} ,context_instance=RequestContext(request))

    else : # first pass 
      if ( hdpList.count() == 0 ) : # new profile
        postform = HDWalletForm()
      else :                        # edit existing profile
        postform = HDWalletForm(instance=hdpList[0])

    return render_to_response(template_name, {'textDict':textDict,'form':postform} ,context_instance=RequestContext(request))


