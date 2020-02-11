import formshare.plugins as plugins
import formshare.plugins.utilities as u
import sys
import os


class mag_frontend(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfig)
    plugins.implements(plugins.ITranslation)

    def update_config(self, config):
        # We add here the templates of the plugin to the config
        u.add_templates_directory(config, "templates")
        u.add_static_view(config, "mag_branding", "static")

    def get_translation_directory(self):
        module = sys.modules["mag_frontend"]
        return os.path.join(os.path.dirname(module.__file__), "locale")

    def get_translation_domain(self):
        return "mag_frontend"
