# Static site builder in Python

- Uses `stencil` templates
- Page content in .md
- Additional page data in .yml files

## Why Graaaf?

See [Van de Graaf](https://en.wikipedia.org/wiki/Van_de_Graaff_generator)

## Layout

- assets/
  - where pages are output
- pages/
  - \**/*.(md|rst) page content -> .html
- templates/
  - default.html
  - ....

For each directory, if a `_.yml` file is found it's parsed and pushed onto the template context.

For each `*.md` file found in the directory, if a matching `.yml` file is found it's parsed and pushed onto the template context.
The markdown is rendered, and then added to the context as 'content'.
Then a `.html` file is created under ``assets`` by rendering the template.


## Generating

Just run:

    graaf

Help:

    $ graaf -h
    usage: graaf [-h] [--source SRC] [--dest DEST] [--templates TMPL]

    Graaf static site generator.

    optional arguments:
    -h, --help            show this help message and exit
    --source SRC, -s SRC  Root of source documents.
    --dest DEST, -d DEST  Directory to output generated files to.
    --templates TMPL, -t TMPL
                            Directory to search for templates in.

