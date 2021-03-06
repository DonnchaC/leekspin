# -*- coding: utf-8 -*-

"""const - Constants.

.. data:: Constant (enum)

   The following are constant strings used within Tor and OpenSSL to
   facilitate conversion between formats. Most are the ``-----BEGIN …-----``
   and ``-----END …-----`` lines in PEM encoded keys and signatures.

   ================== =====================================================
   Constant           Description
   ================== =====================================================
   TOR_BEGIN_KEY      Found at the beginning of a public key
   TOR_END_KEY        Found at the end of a public key
   TOR_BEGIN_SK       Found at the beginning of a private key
   TOR_END_SK         Found at the end of a private key
   TOR_BEGIN_SIG      Found at the beginning of a signature
   TOR_END_SIG        Found at the end of a signature
   OPENSSL_BEGIN_KEY  Found at the beginning of all OpenSSL-generated keys
   OPENSSL_END_KEY    Found at the end of all OpenSSL-generated keys
   OPENSSL_BEGIN_CERT Found at the beginning of all OpenSSL-generated certs
   OPENSSL_END_CERT   Found at the end of all OpenSSL-generated certs
   ================== =====================================================

"""

from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals


#: Strings found in PEM-encoded objects created by Tor
TOR_BEGIN_KEY = b"-----BEGIN RSA PUBLIC KEY-----"
TOR_END_KEY   = b"-----END RSA PUBLIC KEY-----"
TOR_BEGIN_SK  = b"-----BEGIN RSA PRIVATE KEY-----"
TOR_END_SK    = b"-----END RSA PRIVATE KEY-----"
TOR_BEGIN_SIG = b"-----BEGIN SIGNATURE-----"
TOR_END_SIG   = b"-----END SIGNATURE-----"

#: Tokens for ``@type [bridge-]server-descriptor``s
TOKEN_SIGNING_KEY = b"signing-key\n"
TOKEN_ONION_KEY = b"onion-key\n"
TOKEN_ROUTER_SIGNATURE = b"router-signature\n"

#: Strings found in PEM-encoded objects created by OpenSSL
OPENSSL_BEGIN_KEY  = b"-----BEGIN PRIVATE KEY-----"
OPENSSL_END_KEY    = b"-----END PRIVATE KEY-----"
OPENSSL_BEGIN_CERT = b"-----BEGIN CERTIFICATE-----"
OPENSSL_END_CERT   = b"-----END CERTIFICATE-----"

