from typing import Iterator, List, Union

import bs4.element
from bs4 import BeautifulSoup

from sec_html_parser.font_style import FontStyle


class Parser:
    def _is_child(self, node: bs4.element.Tag, other: bs4.element.Tag) -> bool:
        """Check if node is a child of other with respect to font styles"""

        # check that other has a style
        try:
            ostyle = FontStyle(other)
        except ValueError:
            return False

        # a node with no style is always a child
        try:
            nstyle = FontStyle(node)
        except ValueError:
            return True

        # check if style by size
        if ostyle.size is not None:
            if nstyle.size is not None and nstyle.size < ostyle.size:
                return True

        # check if style by weight
        if ostyle.weight is not None:
            if nstyle.weight is not None and nstyle.weight < ostyle.weight:
                return True

        # child if style by style
        if ostyle.style is not None:
            if nstyle.style is not None:
                if ostyle.style == "italic" and nstyle.style != "italic":
                    return True
                else:
                    return False
            return ostyle.style == "italic"

        # if not child by any of the above then it is not a child
        return False

    def _walk_soup(
        self,
        element: Union[BeautifulSoup, bs4.element.PageElement],
        not_into: List[str] = list(),
    ) -> Iterator[bs4.element.PageElement]:
        """
        Iterate given element and all its children in a depth-first manner

        Will not yield elements without a `name` (e.g. a text element in a span),
        neither will it yield elements whose `name` is in the `not_into` list.
        """

        element_is_not_soup = not isinstance(element, BeautifulSoup)
        element_has_name = element.name is not None

        if element_is_not_soup and element_has_name:
            yield element

        element_has_children = hasattr(element, "children")
        if element_has_children:

            should_recurse = element.name not in not_into
            if should_recurse:
                for child in element.children:
                    yield from self._walk_soup(child, not_into)
