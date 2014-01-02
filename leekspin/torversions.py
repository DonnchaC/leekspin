# -*- coding: utf-8 -*-

"""torversions ― Parsers for Tor version numbers.

Portions of this module are directly taken from, or derived from,
:api:twisted.python.compat, and are subject to the Twisted Matrix Labs
copyright and license, in addition to the copyrights and license for the rest
of this program.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys


#: The <major>.<minor>.<micro>.<rev> version numbers for tor, taken from the
#: 'server-versions' line of a consensus file
SERVER_VERSIONS = ['0.2.2.39',
                   '0.2.3.24-rc',
                   '0.2.3.25',
                   '0.2.4.5-alpha',
                   '0.2.4.6-alpha',
                   '0.2.4.7-alpha',
                   '0.2.4.8-alpha',
                   '0.2.4.9-alpha',
                   '0.2.4.10-alpha',
                   '0.2.4.11-alpha',
                   '0.2.4.12-alpha',
                   '0.2.4.14-alpha',
                   '0.2.4.15-rc',
                   '0.2.4.16-rc',
                   '0.2.4.17-rc',
                   '0.2.4.18-rc',
                   '0.2.4.19',
                   '0.2.4.20',
                   '0.2.5.1-alpha',
                   ]

if sys.version_info < (3, 0):
    _PY3 = False
else:
    _PY3 = True


class IncomparableVersions(TypeError):
    """Two versions could not be compared."""


@comparable
class _inf(object):
    """An object that is bigger than all other objects."""
    def __cmp__(self, other):
        """Compare another object with this infinite one.

        If the other object is infinite, it wins. Otherwise, this class is
        always the winner.

        :param other: Another object.
        :rtype: int
        :returns: 0 if other is inf, 1 otherwise.
        """
        if other is _inf:
            return 0
        return 1

_inf = _inf()


def comparable(klass):
    """Class decorator that ensures support for the special C{__cmp__} method.

    On Python 2 this does nothing.

    On Python 3, C{__eq__}, C{__lt__}, etc. methods are added to the class,
    relying on C{__cmp__} to implement their comparisons.

    """
    # On Python 2, __cmp__ will just work, so no need to add extra methods:
    if not _PY3:
        return klass

    def __eq__(self, other):
        c = self.__cmp__(other)
        if c is NotImplemented:
            return c
        return c == 0

    def __ne__(self, other):
        c = self.__cmp__(other)
        if c is NotImplemented:
            return c
        return c != 0

    def __lt__(self, other):
        c = self.__cmp__(other)
        if c is NotImplemented:
            return c
        return c < 0

    def __le__(self, other):
        c = self.__cmp__(other)
        if c is NotImplemented:
            return c
        return c <= 0

    def __gt__(self, other):
        c = self.__cmp__(other)
        if c is NotImplemented:
            return c
        return c > 0

    def __ge__(self, other):
        c = self.__cmp__(other)
        if c is NotImplemented:
            return c
        return c >= 0

    klass.__lt__ = __lt__
    klass.__gt__ = __gt__
    klass.__le__ = __le__
    klass.__ge__ = __ge__
    klass.__eq__ = __eq__
    klass.__ne__ = __ne__
    return klass


@comparable
class Version(object):
    """Holds, parses, and does comparison operations for version numbers.

    :attr string major: The major version number.
    :attr string minor: The minor version number.
    :attr string micro: The micro version number.
    :attr string prerelease: Sometime, another number, though often suffixed
        with a `-`, `+`, or `#`.
    """

    def __init__(self, version, package=None):
        """Create a version object.

        Comparisons may be computed between instances of :class:`Version`s.

        :param string version: One of ``SERVER_VERSIONS``.
        :param string package: The package or program which we are creating a
            version number for, i.e. for "tor-0.2.5.1-alpha" the ``package``
            would be "tor".
        """
        if version.find('.') == -1:
            print("Version.__init__(): %r doesn't look like a version string!"
                  % version.__repr__())

        major, minor, micro, prerelease = ['' for x in xrange(4)]

        components = version.split('.')
        if len(components) > 0:
            try:
                self.prerelease = components.pop()
                self.micro      = components.pop()
                self.minor      = components.pop()
                self.major      = components.pop()
            except IndexError:
                pass

        if package:
            self.package = package

    def base(self):
        """Get the base version number (with prerelease).

        :rtype: string
        :returns: A version number, without the package/program name, and with
            the prefix (if available). For example: '0.2.5.1-alpha'.
        """
        prerelease = getPrefixedPrerelease()
        return '%d.%d.%d%s' % (self.major, self.minor, self.micro, prerelease)

    def getPrefixedPrerelease(self, separator='.'):
        """Get the prerelease string, prefixed by the separator ``prefix``.

        :param string separator: The separator to use between the rest of the
            version string and the :attr:`prerelease` string.
        :rtype: string
        :returns: The separator plus the ``prefix``, i.e. '.1-alpha'.
        """
        pre = ''
        if self.prerelease is not None:
            pre = prefix + self.prerelease
        return pre

    def __repr__(self):
        prerelease = getPrefixedPrerelease('')
        return '%s(package=%r, major=%d, minor=%d, micro=%d, prerelease=%s)' \
            % (self.__class__.__name__, str(self.package),
               self.major, self.minor, self.micro, self.prerelease)

    def __str__(self):
        """Return the package name and version in string form, i.e.
        'tor-0.2.24'.
        """
        if self.package:
            versionstr = str(self.package) + '-'
        versionstr += self.base()

    def __cmp__(self, other):
        """Compare two versions, considering major versions, minor versions,
        micro versions, then prereleases.

        A version with a prerelease is always less than a version without a
        prerelease. If both versions have prereleases, they will be included
        in the comparison.

        :type other: :class:`Version`
        :param other: Another version.
        :raise IncomparableVersions: when the package names of the versions
                                     differ.
        :returns: NotImplemented when the other object is not a Version, or
            one of -1, 0, or 1.
        """
        if not isinstance(other, self.__class__):
            return NotImplemented
        if self.package != other.package:
            raise IncomparableVersions("%r != %r"
                                       % (self.package, other.package))

        if self.prerelease is None:
            prerelease = _inf
        else:
            prerelease = self.prerelease

        if other.prerelease is None:
            otherpre = _inf
        else:
            otherpre = other.prerelease

        x = cmp((self.major,
                    self.minor,
                    self.micro,
                    prerelease),
                   (other.major,
                    other.minor,
                    other.micro,
                    otherpre))
        return x