from xml.etree import ElementTree

from markdown import Markdown
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor

from .app_config import AppConfig

import logging


class ElementTreeExtension(Extension):
    """
    Custom markdown extension
    """

    logger = logging.getLogger('tree_extension')

    logging = AppConfig.get_logging()
    debug = AppConfig.get_debug()

    def extendMarkdown(self, md: Markdown) -> None:
        if self.debug:
            self.logger.info('%s extension engaged' % self . __class__ . __qualname__)

        md.registerExtension(self)
        # noinspection SpellCheckingInspection
        md.treeprocessors.register(ElementTreeProcessor(md), 'notolog_extension', 1)


class ElementTreeProcessor(Treeprocessor):
    """
    Custom markdown extension processor
    """

    logger = logging.getLogger('tree_processor')

    logging = AppConfig.get_logging()
    debug = AppConfig.get_debug()

    def run(self, root):
        # Customize elements tree here
        for idx, elem in enumerate(root.iter()):
            if self.debug:
                self.logger.debug('%s > %d: %s' % (self . __class__ . __qualname__, idx, elem.tag))
            # noinspection SpellCheckingInspection
            """
            Works when `codehilite` is switched off:
            if elem.tag == 'pre':
                for id_xy, c_elem in enumerate(elem):
                    if c_elem.tag == 'code':
                        c_elem.set('style', 'background-color: #373737; color: #f5f5f5; padding: 10px;')
            """
            # if elem.tag == 'img':
            #    elem.set('title', '...')
            #    elem.set('onerror', "this.onerror=null;this.src='app/assets/themes/default/icons/...';")
            if elem.tag == 'p' and len(elem) > 0:
                for id_xy, c_elem in enumerate(elem):
                    if self.debug:
                        self.logger.debug('%s > Inner element > %d: %s'
                                          % (self . __class__ . __qualname__, id_xy, c_elem.tag))
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

    def get_index(self, root, element):
        for idx, child in enumerate(root):
            if element == child:
                return idx
        else:
            raise ValueError("No inner '%s' tag found in '%s'" % (element.tag, root.tag))
