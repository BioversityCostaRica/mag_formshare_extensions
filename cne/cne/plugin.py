import formshare.plugins as plugins
import formshare.plugins.utilities as u
from .views import ExportCNESheets, GenerateCNESheets
import sys
import os
from pyramid.httpexceptions import HTTPFound


def is_cne_form(request, form_id):
    cne_forms = request.registry.settings.get("cne_forms", "")
    cne_forms = cne_forms.split(",")
    if form_id in cne_forms:
        return True
    else:
        return False


class CNE(plugins.SingletonPlugin):
    plugins.implements(plugins.IRoutes)
    plugins.implements(plugins.IConfig)
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.IProduct)
    plugins.implements(plugins.IExport)
    plugins.implements(plugins.ITemplateHelpers)

    def before_mapping(self, config):
        # We don't add any routes before the host application
        return []

    def after_mapping(self, config):
        # We add here a new route /json that returns a JSON
        custom_map = [
            u.add_route(
                "form_export_cne",
                "/user/{userid}/project/{projcode}/form/{formid}/export/cne_cheets",
                ExportCNESheets,
                "dashboard/projects/forms/export/cne.jinja2",
            ),
            u.add_route(
                "form_download_cne_sheets",
                "/user/{userid}/project/{projcode}/form/{formid}/generate/cne_sheets",
                GenerateCNESheets,
                None,
            ),
        ]

        return custom_map

    def update_config(self, config):
        # We add here the templates of the plugin to the config
        u.add_templates_directory(config, "templates")

    def get_translation_directory(self):
        module = sys.modules["cne"]
        return os.path.join(os.path.dirname(module.__file__), "locale")

    def get_translation_domain(self):
        return "cne"

    def update_orm(self, config):
        config.include("cne.orm")

    def update_extendable_tables(self, tables_allowed):
        tables_allowed.append("cne_example")
        return tables_allowed

    def update_extendable_modules(self, modules_allowed):
        modules_allowed.append("cne.orm.cne")
        return modules_allowed

    # ITemplateHelpers
    def get_helpers(self):
        return {"is_cne_form": is_cne_form}

    # IProduct
    def register_products(self, config):
        return [
            {
                "code": "cne_sheets",
                "hidden": False,
                "icon": "far fa-file-archive",
                "metadata": {
                    "author": "QLands Technology Consultants",
                    "version": "10",
                    "Licence": "QLands",
                },
            },
        ]

    def get_product_description(self, request, product_code):
        if product_code == "cne_sheets":
            return "Cuadros 8 y 9 (Zip)"

    def before_download_private_product(
        self, request, project, form, product, output, file_name, mime_type
    ):
        return True

    def before_partner_download_private_product(
        self, request, partner, project, form, product, output, file_name, mime_type
    ):
        return True

    def before_download_public_product(
        self, request, project, form, product, output, file_name, mime_type
    ):
        return True

    def before_download_product_by_api(
        self, request, project, form, product, output, file_name, mime_type
    ):
        return True

    def before_partner_download_product_by_api(
        self, request, partner, project, form, product, output, file_name, mime_type
    ):
        return True

    # IExport
    def has_export_for(self, request, export_type):
        if export_type == "CNE":
            return True
        return False

    def do_export(self, request, export_type):
        if export_type == "CNE":
            user_id = request.matchdict["userid"]
            project_code = request.matchdict["projcode"]
            form_id = request.matchdict["formid"]
            return HTTPFound(
                location=request.route_url(
                    "form_export_cne",
                    userid=user_id,
                    projcode=project_code,
                    formid=form_id,
                )
            )
