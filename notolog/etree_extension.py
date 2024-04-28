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

    debug = AppConfig.get_debug()

    def extendMarkdown(self, md: Markdown) -> None:
        if self.debug:
            self.logger.info('%s extension engaged' % self . __class__ . __qualname__)

        md.registerExtension(self)
        md.treeprocessors.register(ElementTreeProcessor(md), 'custom', 1)


class ElementTreeProcessor(Treeprocessor):
    """
    Custom markdown extension processor
    """

    logger = logging.getLogger('tree_processor')

    debug = AppConfig.get_debug()

    def run(self, root):
        # Customize elements tree here
        for idx, elem in enumerate(root.iter()):
            if self.debug:
                self.logger.info('%s > %d: %s' % (self . __class__ . __qualname__, idx, elem.tag))
            """
            Works when `codehilite` is switched off:
            if elem.tag == 'pre':
                for idxy, celem in enumerate(elem):
                    if celem.tag == 'code':
                        celem.set('style', 'background-color: #373737; color: #f5f5f5; padding: 10px;')
            """
            if elem.tag == 'p' and len(elem) > 0:
                for idxy, celem in enumerate(elem):
                    if self.debug:
                        self.logger.info('%s > Inner element > %d: %s'
                                         % (self . __class__ . __qualname__, idxy, celem.tag))
                    # Example of how to update elements tree
                    if celem.tag == 'a' and False:
                        # Skip element that was already re-inserted
                        if celem.get('class') == '_re-inserted':
                            continue
                        # Add break space before the element
                        br_str = "<hr/>"
                        br_elem = ElementTree.fromstring(br_str)
                        # Remove `a` element
                        elem.remove(celem)
                        # Insert `br` element
                        elem.insert(idxy, br_elem)
                        # Setup class as a flag to determine re-inserted `a` element
                        celem.set('class', '_re-inserted')
                        # Re-insert the `a` element with a new class
                        elem.insert(idxy + 1, celem)

    def get_index(self, root, element):
        for idx, child in enumerate(root):
            if element == child:
                return idx
        else:
            raise ValueError("No inner '%s' tag found in '%s'" %
                 (element.tag, root.tag))
