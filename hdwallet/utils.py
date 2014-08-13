from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from bip32utils import *

from hdwallet.models import *

EX_MAIN_PRIVATE = '0488ade4'.decode('hex') # Version string for mainnet extended private keys
EX_MAIN_PUBLIC  = '0488b21e'.decode('hex') # Version string for mainnet extended public keys



# given a username return publickey
# use m/775/0/i
# return childKey
def next_pub_address(username):

    firstLevelIndex=775
    childKey={}
    u = get_object_or_404(User, username=username)
    hdp = get_object_or_404(HDProfile, user=u)
    masterPubKeyStr=str(hdp.masterExtendedPubKey)
    validate_extended_key(masterPubKeyStr)
    masterPubKey=BIP32Key.fromExtendedKey(masterPubKeyStr)

    thirdLevelIndex=long(hdp.bip32Index)
    thirdLevelIndexStr=str(thirdLevelIndex+5)
    hdp.bip32Index=thirdLevelIndexStr
    hdp.save()

    child=masterPubKey.ChildKey(firstLevelIndex).ChildKey(0).ChildKey(thirdLevelIndex)
    childExtendedPubKey = child.ExtendedKey(private=False,encoded=True)
    childPubKey = child.PublicKey().encode('hex')
    childKey["masterPubKey"]=masterPubKeyStr
    childKey["extendedPubKey"]=childExtendedPubKey
    childKey["PubKey"]=childPubKey
    childKey["index"]=thirdLevelIndex

    return childKey


def validate_extended_key(xkey):
        # Sanity checks
        raw = Base58.check_decode(xkey)
        if len(raw) != 78:
            raise ValueError("extended key format wrong length")


        # Verify address version/type
        version = raw[:4]
        if version == EX_MAIN_PRIVATE:
            keytype = 'xprv'
        elif version == EX_MAIN_PUBLIC:
            keytype = 'xpub'
        else:
            raise ValueError("unknown extended key version")

