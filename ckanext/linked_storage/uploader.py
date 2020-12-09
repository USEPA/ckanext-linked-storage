# encoding: utf-8

import os
#import cgi
import datetime
import logging
import magic
import mimetypes
import shlex
from pathlib import Path, PosixPath, PurePath, PurePosixPath, PureWindowsPath # PurePosixPath, PurePath

# from werkzeug.datastructures import FileStorage as FlaskFileStorage

import ckan.lib.munge as munge
import ckan.plugins as plugins
from ckan.plugins.toolkit import config, ValidationError

# from ckan.lib.uploader import ResourceUpload as CKANResourceUpload
#from ckan.lib.uploader import get_storage_path

log = logging.getLogger(__name__)

class LinkedResource(object):
    def __init__(self, resource):

        config_mimetype_guess = config.get('ckan.mimetype_guess', 'file_ext')

        self.filename = None
        self.mimetype = None

        raw_link_path = resource.get('link_path', resource.get('url', ''))

        if raw_link_path.startswith("\\"):
            link_path = PureWindowsPath(raw_link_path)
        else:
            link_path = PurePath(raw_link_path)


        self.mount_path = None
        self.clear = resource.pop('clear_upload', None)

        self.filesize = 0  # bytes
        self.filename = munge.munge_filename(link_path.name)
        self.link_path = link_path.as_posix()

        # Construct mountpoint dictionary
        mountpoints = dict(zip(shlex.split(config.get('ckanext.linked_storage.net_paths', None)),
                               shlex.split(config.get('ckanext.linked_storage.mountpoints', None))))

        log.debug('Available mountpoints: %r',mountpoints)

        for m in mountpoints:
            if self.link_path.upper().startswith(m.upper()):
                self.mount_path = mountpoints[m] + self.link_path[len(m):]

        if not self.mount_path:
            raise ValidationError('Unable to locate file via the known mount points')

        resource['url_type'] = 'upload'     # appear to CKAN as an upload
        resource['url'] = self.filename     # use filename just like an uploaded file
        resource['link_path'] = self.link_path
        resource['last_modified'] = datetime.datetime.fromtimestamp(os.path.getmtime(self.mount_path))

        with open(self.mount_path, 'rb') as f:

            f.seek(0, os.SEEK_END)
            self.filesize = f.tell()
            # go back to the beginning of the file buffer
            f.seek(0, os.SEEK_SET)

            # check if the mimetype failed from guessing with the url
            if not self.mimetype and config_mimetype_guess == 'file_ext':
                self.mimetype = mimetypes.guess_type(self.filename)[0]

            if not self.mimetype and config_mimetype_guess == 'file_contents':
                try:
                    self.mimetype = magic.from_buffer(f.read(), mime=True)
                    f.seek(0, os.SEEK_SET)
                except IOError as e:
                    # Not that important if call above fails
                    self.mimetype = None

    def get_path(self, id):

        return self.mount_path

    def upload(self, id, max_size=10):
        # you would actually upload the file here, but since this is just a link nothing to do...

        return
