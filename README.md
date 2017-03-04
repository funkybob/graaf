# Static site builder in Python

- Uses `stencil` templates
- Page content in .md
- Additional page data in .yml files

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

