
Config file format
==================

By default, Graaf will read `graaf.yml` for settings.

The layout is as follows, with default values provided:

.. code-block:: yaml

   paths:
     source: pages/
     dest: assets/
     templates: templates/

   generators:
     - name: graaf.simple_md.SimpleMarkdown
     - name: graaf.scss.SassGenerator

The `generators` section lists configurations for the Generators to use, in
order.  Any other values beyond 'name' will be passed to the class when it's
instantiated.

