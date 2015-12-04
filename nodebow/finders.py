# -*- coding: utf-8 -*-
import os
from collections import OrderedDict

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.staticfiles.finders import FileSystemFinder


class BowerComponentsFinder(FileSystemFinder):
    """
    Find static files installed with npm and/or bower
    """
    locations = []
    serve_unminimized = getattr(settings, 'NODEBOW_SERVE_UNMINIMIZED', False)

    def __init__(self, apps=None, *args, **kwargs):
        nodebow_root = getattr(settings, 'NODEBOW_ROOT', settings.STATIC_ROOT)
        bower_components = os.path.abspath(os.path.join(nodebow_root, 'bower_components'))
        if not os.path.isdir(bower_components):
            return
        self.locations = [
            ('', bower_components),
        ]
        self.storages = OrderedDict()
        filesystem_storage = FileSystemStorage(location=bower_components)
        filesystem_storage.prefix = self.locations[0][0]
        self.storages[bower_components] = filesystem_storage

    def find_location(self, root, path, prefix=None):
        if self.serve_unminimized:
            # search for the unminimized version, and if it exists, return it
            base, ext = os.path.splitext(path)
            base, minext = os.path.splitext(base)
            if minext == '.min':
                unminimized_path = super(BowerComponentsFinder, self).find_location(root, base + ext, prefix)
                if unminimized_path:
                    return unminimized_path
        # otherwise proceed with the given one
        path = super(BowerComponentsFinder, self).find_location(root, path, prefix)
        return path
