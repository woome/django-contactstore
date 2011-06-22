from __future__ import with_statement

import unittest
import mock
import urllib

from django.test.client import Client                
from django.core.urlresolvers import reverse as url_reverse

from djangoxslt.xslt.testhelp import assertXpath

from contactstore.models import EmailInvite
from contactstore.tools import import_contacts
from contactstore.tests.tools import _make_names
from contactstore.tests.tools import _make_user
from contactstore.tests.tools import IMPORTER_PASSWORD

class WebTest(unittest.TestCase):
    """Test for importing contacts via the web app."""

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.client = Client()
        self.importing = _make_user()

        self.email1 = _make_names("user1")
        self.email2 = _make_names("user2")
        self.email3 = _make_names("user3")
        
        self.data_list = [
            (self.email1, "U Ser1" ),
            (self.email2, "U Ser2" ),
            (self.email3, "U Ser3" )
            ] 

    def test_web_invite(self):
        try:
            contact_ids = []
            with mock.patch("contactstore.openinviter.get_contacts") as mock_importer:
                mock_importer.return_value = self.data_list
                imported_contacts = import_contacts(
                    self.importing, 
                    self.importing.email, 
                    IMPORTER_PASSWORD
                    )
                contact_ids += [contact["id"] for contact in imported_contacts]

            self.assertTrue(self.client.login(
                    username=self.importing.username, 
                    password=IMPORTER_PASSWORD
                    ))

            invite_url = url_reverse("contactstore.views.create_invites")
            data = urllib.urlencode({
                    "contact_id": contact_ids
                    }, doseq=True)
            response = self.client.post(
                invite_url, 
                data=data, 
                content_type="application/x-www-form-urlencoded"
                )
            self.assertEquals(response.status_code, 200)
            
            invites = EmailInvite.objects.filter(contact__id__in=contact_ids)
            self.assertEquals(len(invites), len(contact_ids))

        finally:
            pass

    def test_web_import(self):
        "Assert that the web client can POST a username and password and get back the list of contacts"
        try:
            with mock.patch("contactstore.openinviter.get_contacts") as mock_importer:
                mock_importer.return_value = self.data_list
                self.assertTrue(self.client.login(
                        username=self.importing.username, 
                        password=IMPORTER_PASSWORD
                        ))

                import_url = url_reverse('contactstore.views.download_contacts')
                response = self.client.post(import_url, {
                        "email": self.importing.email,
                        "password": IMPORTER_PASSWORD
                        })
                self.assertEquals(200, response.status_code)

                # Check we have all the users
                xpath = "//ul[@class='friends']//li[text()='%s']"
                assertXpath(
                    response.content, xpath % (self.email1),
                    html=True
                    )
                assertXpath(
                    response.content, xpath % (self.email2),
                    html=True
                    )
                assertXpath(
                    response.content, xpath % (self.email3),
                    html=True
                    )

        finally:
            pass

# End
