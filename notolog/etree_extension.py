"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Example of an etree extension that allows processing and modifying the document's tree.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2025 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from xml.etree import ElementTree

from markdown import Markdown
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor

import re
import logging


class ElementTreeExtension(Extension):
    """
    Custom markdown extension.
    """

    logger = logging.getLogger('tree_extension')

    def extendMarkdown(self, md: Markdown) -> None:
        self.logger.debug('%s extension engaged' % self.__class__.__qualname__)
        # Registering extension
        md.registerExtension(self)
        # noinspection SpellCheckingInspection
        md.treeprocessors.register(ElementTreeProcessor(md), 'notolog_extension', 1)


class ElementTreeProcessor(Treeprocessor):
    """
    Custom markdown extension tree processor.
    """

    logger = logging.getLogger('tree_processor')

    def run(self, root):
        # Customize elements tree here
        for idx, elem in enumerate(root.iter()):
            self.logger.debug('Process elements > %d: %s' % (idx, elem.tag))
            # Process <table> elements
            if elem.tag == 'table':
                self.process_table(elem)
            if elem.tag in ['th', 'td']:
                self.process_table_td(elem)
            # Process <img> elements
            if elem.tag == 'img':
                self.process_image(elem)
            # Process <p> elements
            if elem.tag == 'p':
                self.process_paragraph(elem)
            # noinspection SpellCheckingInspection
            """
            Works when `codehilite` is switched off:
            if elem.tag == 'pre':
                for id_xy, c_elem in enumerate(elem):
                    if c_elem.tag == 'code':
                        c_elem.set('style', 'background-color: #373737; color: #f5f5f5; padding: 10px;')
            """

    def get_index(self, root, element):
        for idx, child in enumerate(root):
            if element == child:
                return idx
        else:
            raise ValueError("No inner '%s' tag found in '%s'" % (element.tag, root.tag))

    def process_table(self, elem):
        if not elem.get('class'):
            self.logger.debug(f'Table without class found {elem}')
            elem.set('class', '_nl_tbl')
            elem.set('cellpadding', '0')
            elem.set('cellspacing', '0')

    def process_table_td(self, elem):
        # Replace 'style' with 'class' as css doesn't work otherwise
        if elem.get('style') and elem.get('style').startswith('text-align'):
            # re = QRegularExpression(r'^text-align:\s?(.*?);$')
            # match = re.match(elem.get('style'))
            # if match.capturedTexts() and match.captured(1):
            #    ...
            pattern = re.compile(r'^text-align:\s?(.*?);$')
            match = pattern.search(elem.get('style'))
            if match:
                del elem.attrib['style']
                elem.set('class', match.group(1))

    def process_image(self, elem):
        self.logger.debug(f'Image element {elem}')
        # elem.set('title', '...')
        # elem.set('onerror', "this.onerror=null;this.src='...';")

    def process_paragraph(self, elem):
        # Check inner elements
        if not (len(elem) > 0):
            return
        # Process inner elements
        for id_xy, c_elem in enumerate(elem):
            self.logger.debug('Inner element > %d: %s' % (id_xy, c_elem.tag))
            # Example of how to update elements tree
            if c_elem.tag == 'a' and False:
                # Skip element that was already re-inserted
                if c_elem.get('class') == '_re-inserted':
                    continue
                # Add break space before the element
                br_str = "<br/>"
                br_elem = ElementTree.fromstring(br_str)
                # Remove `a` element
                elem.remove(c_elem)
                # Insert `br` element
                elem.insert(id_xy, br_elem)
                # Setup class as a flag to determine re-inserted `a` element
                c_elem.set('class', '_re-inserted')
                # Re-insert the `a` element with a new class
                elem.insert(id_xy + 1, c_elem)
