from django.db import models
from django.contrib.auth import models as auth_models
from datetime import datetime

class Contact(models.Model):
    """A contact you might import into the database."""

    created = models.DateTimeField(
        default=datetime.now,
        help_text="when the contact was created (when it was imported)"
        )

    owner = models.ForeignKey(
        auth_models.User, related_name='mycontacts',
        help_text="the person who invited this contact"
        ) 

    owneremail = models.EmailField(
        help_text="the email of the person who invited this contact, might not be the email we have in auth_user"
        ) 

    email = models.EmailField(help_text="this contact's email address")

    name = models.CharField(
        max_length=1028, blank=True, null=True,
        help_text="this contact's name from the importer"
        )

    can_resend = models.BooleanField(
        default=False,
        help_text="can you resend to the contact"
        )

    invite_sent = models.BooleanField(
        default=False,
        help_text="has the invite been sent"
        )

    manually_added = models.BooleanField(
        default=False,
        help_text="this was manually added as opposed to being imported"
        )

    origin = models.CharField(
        max_length=32, null=True,
        help_text="where the contact was first imported from, eg: yahoo"
        ) 

    filled_profile = models.ForeignKey(
        auth_models.User, null=True, blank=True,
        help_text="the associated profile that results from an invite"
        ) 

    class Meta:
        # Email should only appear once for this user.
        unique_together = (('owner', 'email'),) 

    def __unicode__(self):
        return u"user <%s> knows <%s>%s" % (
            self.owner, 
            self.email,
            u" who has profile %s" % (self.filled_profile.username) if self.filled_profile else u""
            )


class Friend(models.Model):
    """A record of a friendship."""

    created = models.DateTimeField(
        default=datetime.now,
        help_text = "when the invite was created"
        )

    a = models.ForeignKey(
        auth_models.User, related_name="frienda",
        help_text = "a user in the friendship"
        )

    b = models.ForeignKey(
        auth_models.User, related_name="freindb",
        help_text = "the other user in the friendship"
        )


from hashlib import sha1
from random import random

def _email_invite_hash():
    """Make a unique hash to identify the invite."""
    hash_to_try = -1
    while True:
        salt = sha1(str(random())).hexdigest()[:5]
        hash_to_try = sha1(salt + "%s" % datetime.now()).hexdigest()
        if not EmailInvite.objects.filter(tracker = hash_to_try):
            break
    return hash_to_try

class EmailInvite(models.Model):
    """A model which represents the email invitiation of a contact."""

    contact = models.ForeignKey(
        Contact, 
        help_text = "the contact to whom the invite is being sent"
        )

    created = models.DateTimeField(
        default=datetime.now,
        help_text = "when the invite was created"
        )

    email_to = models.EmailField(
        help_text = "the email the invite is being sent to. Denormalized from the Contact"
        )

    email_from = models.EmailField(
        help_text = "the email address this is from"
        )

    tracker = models.CharField(
        max_length=40, unique=True, default=_email_invite_hash,
        help_text = "a unique hash to identify the invite"
        )

    friend = models.ForeignKey(
        Friend, blank=True, null=True,
        help_text = "the friend record binding the invitee and the inviter"
        )
    
    def __unicode__(self):
        return u"%s > %s" % (self.email_to, self.email_from)


# End
