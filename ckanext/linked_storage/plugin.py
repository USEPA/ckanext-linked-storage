import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from ckanext.linked_storage.uploader import LinkedResource


class LinkedStoragePlugin(plugins.SingletonPlugin):
    #plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IUploader)


    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        #toolkit.add_resource('fanstatic', 'linked_storage')

    # IUploader

    def get_resource_uploader(self, data_dict):
        if data_dict.get('url_type',None)  == 'link-storage' or data_dict.get('link_path', None):
            return LinkedResource(data_dict)
        else:
            return None


    def get_uploader(self, upload_to, old_filename=None):
        # We don't provide misc-file storage (group images for example)
        # Returning None here will use the default Uploader.
        return None
