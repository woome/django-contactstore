import mock
import logging

from django import forms

from django.http import HttpResponse, HttpResponseServerError
from django.forms.util import ValidationError
from django.template import RequestContext
from django.core.urlresolvers import reverse as url_reverse

from djangoxslt.xslt import render_to_response
from djangoxslt.xslt.managers import xmlifyiter

from contactstore import tools
from contactstore.openinviter import LoginException

class ContactImportForm(forms.Form):
    """Specifies the contract for the addressbook download."""

    email    = forms.EmailField()
    password = forms.CharField(
        max_length=50, 
        required=True, 
        widget=forms.widgets.PasswordInput()
        )

    def clean_email(self):
        email = self.cleaned_data['email']
        if email.endswith('@googlemail.com'):
            email = email.replace('@googlemail.com', '@gmail.com')
        return email

    def clean(self):
        super(forms.Form, self).clean()
        if not self.cleaned_data.get("email"):
            raise ValidationError("please enter your email address")

        # Do we need to change this rule to qualify yahoo? (or any other oauth provider)
        # If we are yahoo we SHOULD get back an access token, this would replace a password
        # With it we can do YQL
        # We should probably make sure we know what the provider was as well
        if not self.cleaned_data.get("password"):
            raise ValidationError("please enter your password")
        return self.cleaned_data


def download_contacts(request):
    """The view that handles the display and download attempt for the importer."""
    logger = logging.getLogger("download_contacts")
    try:
        post = request.POST.copy()
        form = ContactImportForm(post)
        if not form.is_valid():
            print form.errors
            raise ValidationError("something went wrong with the form")
    except ValidationError, e:
        # Fixme!!!
        ctx = RequestContext(request, {
                "form": form,
                "error_message": e.get_message()
                })
        response = render_to_response("share.xslt", ctx)
        response.status_code = 401
        return response
    else:
        try:
            #with mock.patch("contactstore.openinviter.get_contacts") as mock_importer:
            #    mock_importer.return_value = [
            #        ("email1@aol.com", "user 1"),
            #        ("email2@aol.com", "user 2"),
            #        ("email3@aol.com", "user 3"),
            #        ]

            importer_contacts = tools.import_contacts(
                request.user,
                form.cleaned_data["email"],
                form.cleaned_data["password"]
                )
        except LoginException, e:
            return HttpResponseServerError("bad login")
        except Exception, e:
            # FIXME
            logger.exception(e)
            return HttpResponse("no contacts")
        else:
            # FIXME - use the new xmlify stuff
            contacts = xmlifyiter(
                importer_contacts, 
                "{http://djangoproject.com/template/xslt}contact",
                id="id",
                contact_name="name",
                email="email"
                )

            # Where should the POST go?
            action_url = url_reverse("contactstore.views.create_invites")

            ctx = RequestContext(request, {
                    "contacts": contacts,
                    "action_url": action_url
                    })

            response = render_to_response("share-result.xslt", ctx)
            print response.content
            return response



def create_invites(request):
    # Not gonna use forms for this
    logger = logging.getLogger("create_invites")
    try:
        post = request.POST.copy()
        contact_ids = post.getlist("contact_id")

        # Make the invites... we're going to throw this list away tho
        invites = tools.make_invites(contact_ids)

        response = render_to_response("invited.xslt", RequestContext(request, {}))
        return response
    except Exception, e:
        logger.exception("whoops!")

# End
