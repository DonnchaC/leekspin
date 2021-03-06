# -*- coding: utf-8 -*-

"""Main leekspin module for generating descriptors and writing to disk.

.. authors:: Isis Lovecruft <isis@torproject.org> 0xA3ADB67A2CDB8B35
             Matthew Finkel <sysrqb@torproject.org>
.. licence:: see LICENSE file for licensing details
.. copyright:: (c) 2013-2014 The Tor Project, Inc.
               (c) 2013-2014 Isis Lovecruft
               (c) 2013-2014 Matthew Finkel
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import binascii


def generateBridgeNetstatus(nickname, idkey_digest, server_desc_digest,
                            timestamp, ipv4, orport, ipv6=None, dirport=None,
                            flags='Fast Guard Running Stable Valid',
                            bandwidth_line=None):
    """Generate an ``@type bridge network-status 1.0`` document (unsigned).

    This function will generate a networkstatus document for a bridge relay,
    similar to the following::

        r StingilyScampers Wdtrb4h8QVqqbDH4gMmVnAn2nYg 1BEVkVjixzVMFu7OK46GklhYtkg 2014-08-06 20:40:21 39.102.19.106 36286 0
        a [72be:7d50:9c91:1170:2bf9:d760:bee1:66e1]:36286
        s Fast Guard Running Stable Valid
        w Bandwidth=1481409
        p reject 1-65535

    :param str nickname: The router's nickname.
    :param string idkey_digest: The SHA-1 digest of the router's public identity
        key.
    :param str server_desc_digest: The SHA-1 digest of the router's
        ``@type [bridge-]server-descriptor``, before the descriptor is signed.
    :param str timestamp: An ISO 8601 timestamp, with a space as the separator.
    """
    idkey_b64  = binascii.b2a_base64(idkey_digest)
    idb64      = str(idkey_b64).strip().rstrip('==')
    server_b64 = binascii.b2a_base64(server_desc_digest)
    srvb64     = str(server_b64).strip().rstrip('==')

    if bandwidth_line is not None:
        bw = int(bandwidth_line.split()[-1]) / 1024  # The 'observed' value
    dirport = dirport if dirport else 0

    doc = []
    doc.append(b"r %s %s %s %s %s %s %d"
               % (nickname, idb64, srvb64, timestamp, ipv4, orport, dirport))
    if ipv6 is not None:
        doc.append(b"a [%s]:%s" % (ipv6, orport - 1))

    doc.append(b"s %s" % flags)
    doc.append(b"w Bandwidth=%s" % bw)
    doc.append(b"p reject 1-65535\n")

    netstatusDoc = b'\n'.join(doc)
    return netstatusDoc
