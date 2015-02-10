================
Formatted fields
================

This plugin lets you create fields (metadata) that will be formatted
in the same way the main file content is formatted.

For example, in a reStructuredText document, you can define fields containing
a value in reStructuredText, and it will be translated to HTML.

To select which fields are translated, list them in the
FORMATTED_FIELDS setting in your Pelican configuration file:

.. code:: python

   FORMATTED_FIELDS = ['read_more', 'some_facts']
