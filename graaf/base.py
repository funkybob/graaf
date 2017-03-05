import os

import yaml


class Generator(object):
    '''
    Base Generator class
    '''
    extensions = []

    def can_process(self, filename):
        '''Determine if this instance will attempt to process the file.'''
        return os.path.splitext(filename)[1] in self.extensions

    def process(self, src_dir, dest_dir, filename, processor):
        '''
        Called by the Processor for any file that can_process returns True for.
        '''
        raise NotImplementedError


def get_yaml(src):
    '''
    Try to read a YAML document from the provided file.

    If it doesn't exist, return an empty dict instead.
    '''
    try:
        with open(src) as fin:
            return yaml.load(fin)
    except IOError:
        return {}
