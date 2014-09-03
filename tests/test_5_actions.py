""" test doing things with keys/signatures/etc
"""
import pytest

import os
import warnings

from pgpy import PGPKey
from pgpy import PGPMessage
from pgpy import PGPSignature

class TestPGPMessage(object):
    def test_decrypt_passphrase_message(self, passmessage):
        msg = PGPMessage()
        msg.parse(passmessage)

        decmsg = msg.decrypt("QwertyUiop")

        assert isinstance(decmsg, PGPMessage)
        assert decmsg.message == bytearray(b"This is stored, literally\\!\n\n")


class TestPGPKey(object):
    def test_unlock_enckey(self):
        pytest.skip("not implemented yet")

    def test_verify_detach(self, sigf):
        # test verifying signatures in tests/testdata/signatures
        key = PGPKey()
        key.parse(sigf + '.key.asc')
        sig = PGPSignature()
        sig.parse(sigf + '.sig.asc')
        sigv = key.verify(sigf + '.subj', sig)

        assert sigv

    def test_verify_cleartext(self, ctmessage, rsakey, dsakey):
        rsa = PGPKey()
        rsa.parse(rsakey)
        dsa = PGPKey()
        dsa.parse(dsakey)

        ctmsg = PGPMessage()
        ctmsg.parse(ctmessage)

        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            assert rsa.verify(ctmsg)
            assert dsa.verify(ctmsg)

    def test_verify_onepass_signed_message(self):
        pytest.skip("not implemented yet")

    def test_verify_signed_message(self):
        pytest.skip("not implemented yet")

    def test_verify_wrongkey(self):
        # test verifying with the wrong key
        pytest.skip("not implemented yet")

    def test_verify_invalid(self):
        # test verifying an invalid signature
        pytest.skip("not implemented yet")

    def test_sign_rsa_bindoc(self, rsakey, gpg_verify):
        # test signing binary documents with RSA
        key = PGPKey()
        key.parse(rsakey)

        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            sig = key.sign('tests/testdata/lit')

        with open('tests/testdata/lit.sig', 'w') as sigf:
            sigf.write(str(sig))

        # verify with PGPy
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            assert key.verify('tests/testdata/lit', sig)

        # verify with GPG
        assert 'Good signature from' in gpg_verify('./lit', './lit.sig')

        os.remove('tests/testdata/lit.sig')

    def test_sign_dsa_bindoc(self, dsakey, gpg_verify):
        # test signing binary documents with DSA
        key = PGPKey()
        key.parse(dsakey)

        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            sig = key.sign('tests/testdata/lit')

        with open('tests/testdata/lit.sig', 'w') as sigf:
            sigf.write(str(sig))

        # verify with PGPy
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            assert key.verify('tests/testdata/lit', sig)

        # verify with GPG
        assert 'Good signature from' in gpg_verify('./lit', './lit.sig')

        os.remove('tests/testdata/lit.sig')

    def test_decrypt_rsa_message(self, rsamessage):
        key = PGPKey()
        key.parse('tests/testdata/keys/rsa.asc')

        msg = PGPMessage()
        msg.parse(rsamessage)

        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            decmsg = key.decrypt(msg)

        assert isinstance(decmsg, PGPMessage)
        assert decmsg.message == bytearray(b"This is stored, literally\\!\n\n")