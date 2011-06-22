#!/usr/bin/env python


"""A python wrapper around openinviter.

This is designed to be called by python libraries but there is a
simple command line interface as well.


Command Line

call this like:

 python invitecmd.py username@hotmail.com password

and it will contact hotmail with openinviter and print the contacts it pulled down.


Test Help

if you call get_contacts with test_mode=True then you get the extra
addresses (those in TEST_LINES) that help assert things.
"""

from subprocess import Popen
from subprocess import PIPE
from os.path import join as joinpath
from os.path import dirname
import re

class ImporterException(Exception):
    """An exception to indicate some problem with the importer."""
    pass

class LoginException(ImporterException):
    """Indicates a failure to authorize"""
    pass

class UnsupportedImporterException(ImporterException):
    """We don't support this provider"""
    pass

EMAIL = re.compile("[^']+@[A-Za-z.-]+")

TEST_LINES = (
    "nic@one,",
    "nic@woomeduplicate.com,nic",       # help assert that you can't have duplicates
    "nic@woomeduplicate.com,nicholas",
    "asadlkqjcbqjbk",                   # help assert you can't get less than 2 parts
    ",blah",                            # help assert you can't get non-emails
    )

def _get_contact_iter(provider, email, password, test_mode=False):
    path = joinpath(dirname(__file__), "php", "script.php")
    proc = Popen([
            "php",
            path,
            email,
            password,
            provider
            ], stdout=PIPE, stderr=PIPE)
    pid = proc.pid
    stdout, stderr, = proc.communicate()
    if stdout.startswith("error:"):
        error = stdout.split("error:")[1].strip()
        if error == "login error":
            raise LoginException("login error pid=%s email=%s" % (pid, email))
        else:
            raise ImporterException(error)

    # Otherwise we have some addressses
    lines = stdout.split("\n")
    if test_mode:
        lines += TEST_LINES

    emails = {}
    for line in lines:
        parts = line.split(",")
        if len(parts) > 0:
            email = parts[0]
            if EMAIL.match(email):
                if emails.get(email, None):
                    continue
                emails[email] = parts
                yield email, " ".join(parts[1:])
    return


_DOMAIN_RE = re.compile("[^@]+@(?P<provider>[^.]+)\\..*")
_PROVIDER_MAP = {
    "googlemail": 'gmail',
    "gmail": "gmail",
    "yahoo": "yahoo",
    "hotmail": "hotmail",
    "live": "hotmail",
    "msn": "msn",
    "aol": "aol",
}

def get_contacts(email, password, test_mode=False):
    """The contacts list is a unique list of contacts.

    Each contact is a pair of emailaddress, contact detail (usuaully name).

    The contacts are unique by email address. The first contact found
    with the email address is used.

    This python wrapper manages a mapping of domain parts to provider
    names. The domain part being the first part of the domain name
    after the @ in the email parameter.
    """
    domain = _DOMAIN_RE.match(email)
    if domain:
        domain_name = domain.group("provider")
        try:
            provider = _PROVIDER_MAP.get(domain_name)
        except KeyError, e:
            raise UnsupportedImporterException(e)
        else:
            addresses = list(_get_contact_iter(provider, email, password, test_mode))
            return addresses

try:
    import contactstore_TESTS
except Exception, e:
    TESTS = []
else:
    TESTS = contactstore_TESTS.TESTS

import sys
def main():
    if sys.argv[1:]:
        if len(sys.argv[1:]) != 2:
            print >>sys.stderr, "Wrong args - use: providername email password"
        else:
            print "%s %s\n" % (
                sys.argv[1], 
                get_contacts(*sys.argv[1:])
                )
        return

    for a in TESTS:
        try:
            print "%s %s\n" % (a["username"], get_contacts(a["username"], a["password"]))
        except Exception, e:
            print e

if __name__ == "__main__":
    main()

# End
