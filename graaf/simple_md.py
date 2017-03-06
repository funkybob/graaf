import os

import markdown

from .base import Generator, get_yaml

md = markdown.Markdown()


class SimpleMarkdown(Generator):
    '''
    Generator for processing plain Markdown files

    Will try to read {filename}.yml for additional context.
    Will use context['template'] for the template name.
    '''
    extensions = ['.md']

    def process(self, src_dir, dest_dir, filename, processor):
        basename, ext = os.path.splitext(filename)

        processor.context.push(
            **get_yaml(os.path.join(src_dir, basename + '.yml'))
        )

        processor.context['content'] = md.reset().convert(
            self.read_file(src_dir, filename)
        )
        tmpl = processor.templates[processor.context['template']]
        self.write_file(dest_dir, basename + '.hmtl', tmpl.render(processor.context))

        processor.context.pop()

        return True
