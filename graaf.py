import os

import markdown
import yaml
from stencil import TemplateLoader, Context

md = markdown.Markdown()


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


def cmd(srcdir='pages/', destdir='assets/', templatedir='templates/'):
    print "Generating..."

    loader = TemplateLoader([templatedir])
    context = Context({})

    for root, dirs, files in os.walk(srcdir):
        print "Scanning: %r" % (root,)
        dest_root = os.path.join(destdir, root[len(srcdir):])
        try:
            os.makedirs(dest_root)
        except OSError:
            pass

        context.push(**get_yaml(os.path.join(root, '_.yml')))

        for filename in files:
            basename, ext = os.path.splitext(filename)

            if ext == '.md':
                print "\tFound: %r" % (filename,)
                context.push(**get_yaml(os.path.join(root, basename + '.yml')))
                with open(os.path.join(root, filename)) as fin:
                    context['content'] = md.reset().convert(fin.read())
                tmpl = loader[context['template']]
                with open(os.path.join(dest_root, basename + '.html'), 'w') as fout:
                    fout.write(tmpl.render(context))
                context.pop()

        context.pop()


if __name__ == '__main__':
    cmd()
