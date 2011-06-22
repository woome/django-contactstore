from django.conf.urls.defaults import patterns

urlpatterns = patterns('contactstore.views',
    (r'invitation/$','create_invites'),
    (r'$','download_contacts'),
)
