from Products.CMFCore import permissions
from AccessControl import ClassSecurityInfo
from Products.ATContentTypes.atct import ATFolder, ATFolderSchema
from Products.FAQulator.config import *
from Products.FAQulator import FAQulatorMessageFactory as _

try:
    from Products.LinguaPlone.public import *
except ImportError:
    # No multilingual support
    from Products.Archetypes.public import *

schema  = ATFolderSchema.copy() + Schema((
        TextField("description",
            searchable = True,
            required   = True,
            accessor   = "Description",
            storage    = MetadataStorage(),
            widget     = VisualWidget(
                label             = _("faq_introlabel", default="Description"),
                description       = _("faq_intro", default="Text above the questions list"),
                  ),
        ),
        BooleanField("show_header",
            searchable  = False,
            widget      = BooleanWidget(
                label             = _("faq_showheaderlabel", default="Show question list"),
                description       = _("faq_showheader", default="Show a short list with all questions at the top of "
                                                                  "the FAQ. This can make it navigation easier if you have "
                                                                  "a large number of entries in your FAQ.")
                ),
        ),
        BooleanField("show_answers",
            searchable = False,
            default    = True,
            widget     = BooleanWidget(
                label         = _("faq_showanswerslabel", default="Show answers"),
                description   = _("faq_showanswers", default="Show the individual questions and their answers in full. This "
                                                               "is standard behaviour for a FAQ.")
            ),
        ),
        ))


class FAQ(ATFolder):
    """A frequently asked questions list."""
    schema                      = schema
    content_icon                = "faq_icon.gif"
    filter_content_types        = True
    allowed_content_types       = ( "FAQEntry", )
    archetype_name              = "FAQ"
    default_view                = "faq_view"
    immediate_view              = "faq_view"
    suppl_views         = ( "folder_summary_view", "folder_tabular_view" )

    security            = ClassSecurityInfo()
    security.declarePublic("listFolderContents")

    actions = ({ 'id': "view",
                 'name': "View",
                 'action': "string:${object_url}/faq_view",
                 'permissions': (permissions.View,)
                 },
               { 'id': 'edit',
                 'name': 'Edit',
                 'action': 'string:${object_url}/base_edit',
                 'condition': 'python: not object.get("isCanonical", False) or object.isCanonical()',
                 'permissions': (permissions.ModifyPortalContent,),
                 },
               { 'id': 'translate',
                 'name': 'Edit',
                 'action': 'string:${object_url}/translate_item',
                 'condition': 'python: object.get("isCanonical", False) and not object.isCanonical()',
                 'permissions': (permissions.ModifyPortalContent,),
                 },
               )

    def post_validate(self, REQUEST=None, errors={}):
        """Custom validator to check if either show_header or show_ansers is set.
        """

        if not (int(REQUEST.form.get("show_header",1)) or int(REQUEST.form.get("show_answers",1))):
            errors["show_header"]=_("Please select one of the show question list or show answers options")


registerType(FAQ, PROJECTNAME)
