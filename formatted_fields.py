# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

import docutils
from pelican.readers import MarkdownReader, RstReader, render_node_to_html


def md_parse_metadata(reader, meta):
    """Return the dict containing document metadata"""
    if 'FORMATTED_FIELDS' in reader.settings:
        formatted_fields = reader.settings['FORMATTED_FIELDS']
        formatted_fields.append('summary')
    else:
        formatted_fields = ['summary']

    output = {}
    for name, value in meta.items():
        name = name.lower()
        if name in formatted_fields:
            # handle summary metadata as markdown
            # summary metadata is special case and join all list values
            summary_values = "\n".join(value)
            # reset the markdown instance to clear any state
            reader._md.reset()
            summary = reader._md.convert(summary_values)
            output[name] = reader.process_metadata(name, summary)
        elif name in METADATA_PROCESSORS:
            if len(value) > 1:
                logger.warning('Duplicate definition of `%s` '
                    'for %s. Using first one.', name, reader._source_path)
            output[name] = reader.process_metadata(name, value[0])
        elif len(value) > 1:
            # handle list metadata as list of string
            output[name] = reader.process_metadata(name, value)
        else:
            # otherwise, handle metadata as single string
            output[name] = reader.process_metadata(name, value[0])
    return output


def rst_parse_metadata(reader, document):
    """Return the dict containing document metadata"""
    if 'FORMATTED_FIELDS' in reader.settings:
        formatted_fields = reader.settings['FORMATTED_FIELDS']
        formatted_fields.append('summary')
    else:
        formatted_fields = ['summary']

    output = {}
    for docinfo in document.traverse(docutils.nodes.docinfo):
        for element in docinfo.children:
            if element.tagname == 'field':  # custom fields (e.g. summary)
                name_elem, body_elem = element.children
                name = name_elem.astext()
                if name in formatted_fields:
                    value = render_node_to_html(document, body_elem)
                else:
                    value = body_elem.astext()
            elif element.tagname == 'authors':  # author list
                name = element.tagname
                value = [element.astext() for element in element.children]
                value = ','.join(value) # METADATA_PROCESSORS expects a string
            else:  # standard fields (e.g. address)
                name = element.tagname
                value = element.astext()
            name = name.lower()

            output[name] = reader.process_metadata(name, value)
    return output


def register():
    MarkdownReader._parse_metadata = md_parse_metadata
    RstReader._parse_metadata = rst_parse_metadata

