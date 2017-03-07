import os

from stencil import TemplateLoader, Context

from .base import get_yaml

VERSION = (0, 2, 2)


def get_version():
    return '.'.join(map(str, VERSION))


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
        content = self.templates[template_name](self.context)
        self.context.pop()
        return content
