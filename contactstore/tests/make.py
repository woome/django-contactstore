from __future__ import with_statement
import unittest
import mock

from contactstore.tools import import_contacts
from contactstore.tools import make_invites
from contactstore.models import Contact

from contactstore.tests.tools import _make_names
from contactstore.tests.tools import _make_user
from contactstore.tests.tools import IMPORTER_PASSWORD


class ContactTest(unittest.TestCase):
    """Test for importing contacts."""

    def setUp(self):
        """Set up

        make the user that will import
        
        make a list of unique emails to import

        make the imported contacts through a mock importer
        """
        unittest.TestCase.setUp(self)
        self.importing = _make_user()

        self.email1 = _make_names("user1")
        self.email2 = _make_names("user2")
        self.email3 = _make_names("user3")
        
        self.data_list = [
            (self.email1, "U Ser1" ),
            (self.email2, "U Ser2" ),
            (self.email3, "U Ser3" )
            ] 

        self.imported_contacts = []
        with mock.patch("contactstore.openinviter.get_contacts") as mock_importer:
            mock_importer.return_value = self.data_list
            self.imported_contacts = import_contacts(
                self.importing, 
                self.importing.email, 
                IMPORTER_PASSWORD
                )


    def test_invite_create(self):
        """Test that invites can be created from a list of contact ids"""
        try:
            contact_ids = [contact["id"] for contact in self.imported_contacts]
            invites = make_invites(contact_ids)

            test_data = "|".join([d[0] for d in self.data_list])
            invite_emails = "|".join([invite["email_to"] for invite in invites])
            self.assertEquals(
                test_data, invite_emails,
                "invite emails are not the same as the test data: %s" % invite_emails
                )
        finally:
            pass

    def test_contact_import(self):
        "Assert that tools.import_contacts leaves the correct things in the db."
        try:
            test_data = "|".join([d[0] for d in self.data_list])
            contact_data = "|".join([i.get("email") for i in self.imported_contacts])
            self.assertEquals(
                contact_data, test_data,
                "%s != %s" % (contact_data, test_data)
                )

            dbcontact_data = "|".join([
                    i.email for i in Contact.objects.filter(
                        owner=self.importing).order_by("email")
                    ])
            self.assertEquals(
                dbcontact_data, test_data,
                "%s != %s" % (dbcontact_data, test_data)
                )
        finally:
            pass

# End
