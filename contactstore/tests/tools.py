import logging
from django.contrib.auth.models import User
from datetime import datetime

def _make_names(prefix):
    """Make unique username and email address"""
    logger = logging.getLogger('contactstore.tests._make_names')

    if len(prefix) > 5:
        raise ValueError('Username prefix is too long')

    d = datetime.now()
    dlst = (str(d.year)[2:], d.month, d.day, d.hour, d.minute, d.second, str(d.microsecond)[:2])
    username = "%s_%s%02d%02d%02d%02d%02d%s" % ((prefix,) + dlst)
    try:
        User.objects.get(username__iexact=username)
        logger.debug("Already found username for %s..." % username)
        prefix = "%sB" % prefix
        username = "%s_%s%02d%02d%02d%02d%02d%s" % ((prefix,) + dlst)
        logger.debug("Username changed to %s..." % username)
    except User.DoesNotExist:
        pass

    return username

IMPORTER_PASSWORD="secret"

def _make_user():
    importing, _ = User.objects.get_or_create(
        username='ff',
        email='ff@example.com',
        )
    importing.set_password(IMPORTER_PASSWORD)
    importing.save()
    return importing

# End
