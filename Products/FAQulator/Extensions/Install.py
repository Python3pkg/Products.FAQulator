from Products.Archetypes.public import listTypes
from Products.Archetypes.Extensions.utils import installTypes, install_subskin
from Products.CMFCore.utils import getToolByName
from Products.FAQulator.config import PROJECTNAME, GLOBALS

from io import StringIO

def configureTypes(self, out):
    """Register new types and configure them."""

    installTypes(self, out, listTypes(PROJECTNAME), PROJECTNAME)

    ft=getToolByName(self, "portal_factory")
    pft=list(ft.getFactoryTypes().keys())
    for type in [ "FAQ", "FAQEntry" ]:
        if type not in pft:
            print("Adding %s to factory types" % type, file=out)
            pft.append(type)
    ft.manage_setPortalFactoryTypes(listOfTypeIds=pft)


def install(self):
    out = StringIO()

    configureTypes(self, out)
    install_subskin(self, out, GLOBALS)

    print("Successfully installed %s." % PROJECTNAME, file=out)
    return out.getvalue()

