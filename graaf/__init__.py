import os

from stencil import TemplateLoader, Context

from .base import get_yaml


class Processor(object):
    def __init__(self, srcdir, destdir, templatedir, generators=None):
        self.srcdir = srcdir
        self.destdir = destdir
        self.templatedir = templatedir
        self.generators = generators or []
        self.templates = TemplateLoader([templatedir])

    def run(self):
        print "Generating..."

        self.context = Context({})

        for root, dirs, files in os.walk(self.srcdir):
            print "Scanning: %r (%d files)" % (root, len(files))
            dest_root = os.path.join(self.destdir, root[len(self.srcdir):])
            try:
                os.makedirs(dest_root)
            except OSError:
                pass

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

    def render(self, template_name, extra_context):
        self.context.push(**extra_context)
        content = self.templates[template_name](self.context)
        self.context.pop()
        return content
