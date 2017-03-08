import io
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

    def read_file(self, src_dir, filename):
        with io.open(os.path.join(src_dir, filename), mode='r', encoding='utf-8') as fin:
            return fin.read()

    def write_file(self, dest_dir, filename, content):
        with io.open(os.path.join(dest_dir, filename), mode='w', encoding='utf-8') as fout:
            fout.write(content)

    def start(self, processor):
        '''
        Hook to alow Generators to react to start of processing.
        '''
        pass

    def enter_dir(self, src_dir, dirs, files):
        '''
        Hook to allow Generators to react to start of processing a dir.
        '''
        pass

    def leave_dir(self, src_dir, dirs, files):
        '''
        Hook to allow Generators to react to end of processing a dir.
        '''
        pass


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
