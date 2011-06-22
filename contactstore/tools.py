
import logging
import openinviter as importer

from contactstore.models import Contact
from contactstore.models import EmailInvite

def import_contacts(inviter_user, inviter_username, password):
    """Import the contacts from the user's addressbook using openinviter.

    inviter_user - the auth_user.User object that represents the importing user

    inviter_username - the email address of the user which will be
    used for addressbook download, eg: @yahoo, @msn, etc...

    password - the password for logging in to the addressbook download
    tool for the addressbook provider.

    Returns the list of contact records created (or existing) in the
    database.
    """
    logger = logging.getLogger("contactstore.tools.import_contacts")

    importer_contacts = importer.get_contacts(inviter_username, password)
    contact_list = []
    for email, name in importer_contacts:
        contact, is_created = Contact.objects.get_or_create(
            email=email,
            defaults={
                "owner": inviter_user,
                "owneremail": inviter_username,
                "name": name,
                }
            )
        contact_list.append(contact.__dict__)

    return contact_list


def make_invites(contact_ids):
    """Turn a list of contact ids into invites.

    Returns the invite data as a list of dicts.
    """
    contacts = Contact.objects.filter(id__in=contact_ids)
    invites = []
    for contact in contacts:
        invite, created = EmailInvite.objects.get_or_create(
            contact=contact,
            email_to=contact.email,
            email_from=contact.owneremail
            )
        if created:
            invite.save()
            invites.append(invite.__dict__)

    return invites

# End
