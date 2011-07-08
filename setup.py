from setuptools import setup

classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Utilities',
    'Topic :: Communications :: Email',
]

# Recursive file finder for adding our PHP
import os
import os.path
def lsrecursive(base):
    output = []
    lst = os.listdir(base)
    for f in lst:
        entry = os.path.join(base,f)
        if os.path.isdir(entry) and entry != ".." and entry != ".":
            output += lsrecursive(entry)
        else:
            output += [entry]
    return output

def _get_files():
    lst = [s.split("contactstore/openinviter/")[1] 
             for s in lsrecursive(os.path.join(os.path.dirname(__file__), "contactstore/openinviter/php"))
             ]
    return lst

# Depends: 
# django, php
setup(
    name = "django-contactstore",
    version = "0.1.3",
    description = "an openinviter based contact importer",
    long_description = """Allows importing and invite sending with OpenInviter using PHP.""",
    license = "GPLv2",
    author = "Nic Ferrier",
    author_email = "nic@woome.com",
    url = "http://github.com/woome/django-contactstore",
    download_url="http://github.com/woome/django-contactstore/downloads",
    platforms = ["unix"],
    packages = ["contactstore", "contactstore.tests", "contactstore.openinviter"],
    package_data = {
        "contactstore.openinviter": _get_files(),
        },
    entry_points = {
        'console_scripts': [
            'openinviter = contactstore.openinviter.invitercmd:main',
            ],
        },
    classifiers =  classifiers
    )
