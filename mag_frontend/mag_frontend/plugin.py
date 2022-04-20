import formshare.plugins as plugins
import formshare.plugins.utilities as u
import sys
import os
# import requests


class mag_frontend(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfig)
    plugins.implements(plugins.ITranslation)
    # plugins.implements(plugins.IUserAuthentication)

    def update_config(self, config):
        # We add here the templates of the plugin to the config
        u.add_templates_directory(config, "templates")
        u.add_static_view(config, "mag_branding", "static")

    def get_translation_directory(self):
        module = sys.modules["mag_frontend"]
        return os.path.join(os.path.dirname(module.__file__), "locale")

    def get_translation_domain(self):
        return "mag_frontend"

    # IUserAuthentication

    # def after_login(self, request, user):
    #     return True, ""
    #
    # def on_authenticate_user(self, request, user_id, user_is_email):
    #     return None, {}
    #
    # def on_authenticate_password(self, request, user_data, password):
    #     _ = self.translate
    #     user_email = user_data["user_email"].lower()
    #     parts = user_email.split("@")
    #     if len(parts) != 2:
    #         return False, _("Invalid email")
    #
    #     endpoint = "https://sistemas.senasa.go.cr/WS_Autenticacion/Autenticacion.asmx"
    #     if user_email.find("senasa.go.cr") >= 0:
    #         soap_body = '<?xml version="1.0" encoding="utf-8"?>' \
    #                     '<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ' \
    #                     'xmlns:xsd="http://www.w3.org/2001/XMLSchema" ' \
    #                     'xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">' \
    #                     '<soap:Body>' \
    #                     '<verificarUsuarioSenasa xmlns="http://www.senasa.go.cr/ws_Autenticacion">' \
    #                     '<strUsuario>{}</strUsuario>' \
    #                     '<strUsuarioAd>{}</strUsuarioAd>' \
    #                     '<strClaveAd>{}</strClaveAd>' \
    #                     '</verificarUsuarioSenasa>' \
    #                     '</soap:Body>' \
    #                     '</soap:Envelope>'.format(parts[0], parts[0], password)
    #     else:
    #         soap_body = '<?xml version="1.0" encoding="utf-8"?>' \
    #                     '<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ' \
    #                     'xmlns:xsd="http://www.w3.org/2001/XMLSchema" ' \
    #                     'xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">' \
    #                     '<soap:Body>' \
    #                     '<verificarUsuarioSenasa xmlns="http://www.senasa.go.cr/ws_Autenticacion">' \
    #                     '<strUsuario>{}</strUsuario>' \
    #                     '<strUsuarioAd>{}</strUsuarioAd>' \
    #                     '<strClaveAd>{}</strClaveAd>' \
    #                     '</verificarUsuarioSenasa>' \
    #                     '</soap:Body>' \
    #                     '</soap:Envelope>'.format(parts[0], parts[0], password)
    #     session = requests.session()
    #     session.headers = {"Content-Type": "text/xml; charset=utf-8"}
    #     session.headers.update({"Content-Length": str(len(soap_body))})
    #     session.headers.update(
    #         {"SOAPAction": "http://www.senasa.go.cr/ws_Autenticacion/LoguerUsuario"}
    #     )
    #     response = session.post(url=endpoint, data=soap_body, verify=False)
    #     if response.status_code == 200:
    #         return True, ""
    #     else:
    #         return False, "Unable to authenticate. Error: {}".format(
    #             response.status_code
    #         )
    #
    # def after_collaborator_login(self, request, collaborator):
    #     return True, ""
