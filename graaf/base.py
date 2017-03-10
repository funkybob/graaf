import io
import os

import yaml

from stencil import TemplateLoader, Context


class Processor(object):
    '''
    Site Processor class.

    Given directories for source documents, destination, and templates, as well
    as a list of generators, will process all files.

    Will apply `_.yml` to the context in each directory.
    '''
    def __init__(self, srcdir, destdir, templatedir, generators=None):
        self.srcdir = srcdir
        self.destdir = destdir
        self.templatedir = templatedir
        self.generators = generators or []
        self.templates = TemplateLoader([templatedir])

    def run(self):
        '''
        Trigger to process...
        '''
        print "Generating..."

        self.context = Context({})

        for generator in self.generators:
            generator.start(self)

        for root, dirs, files in os.walk(self.srcdir):
            print "Scanning: %r (%d files)" % (root, len(files))
            dest_root = os.path.join(self.destdir, root[len(self.srcdir):])
            try:
                os.makedirs(dest_root)
            except OSError:
                pass

            for generator in self.generators:
                generator.enter_dir(root, dirs, files)

            self.context.push(**get_yaml(os.path.join(root, '_.yml')))

            for filename in files:
                for generator in self.generators:
                    if generator.can_process(filename):
                        print "Processing %r" % (filename,)
                        if generator.process(root, dest_root, filename, self):
                            break
                else:
                    pass
                    # print "\tNo generator for: %r" % filename

            self.context.pop()

            for generator in self.generators:
                generator.leave_dir(root, dirs, files)

        for generator in self.generators:
            generator.finish(self)

    def render(self, template_name, extra_context):
        '''
        Helper function to render a template with the current context, and extra
        context.
        '''
        self.context.push(**extra_context)
        content = self.templates[template_name].render(self.context)
        self.context.pop()
        return content


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

    def finish(self, processor):
        '''
        Hook to allow Generators to react to end of processing.
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
