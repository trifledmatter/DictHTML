from typing import List, Union, Optional, Callable, Dict, Any
from htypes import HTMLElement, HTMLPlainText


class HTMLUtility:
    def __init__(self, root: HTMLElement):
        self.root = root

    def prettify_elements(self, element: List[HTMLElement]) -> List[HTMLElement]:
        for _ in element:
            if 'class' not in _.attributes.keys():
                continue

            cn = "..." if len(_.attributes["class"]) >= 8 else str(_.attributes['class'])[:8]
            _.attributes["class"] = cn
        
        return element

    def element(self, element: HTMLElement, tag: str) -> bool:
        return element.tag == tag

    def find_unique(
        self,
        predicate: Optional[Callable[[HTMLElement], bool]] = None,
        tag: Optional[str] = None,
        attributes: Optional[Dict[str, str]] = None,
        class_name: Optional[str] = None,
    ) -> Optional[HTMLElement]:
        """Finds a unique element that matches the predicate or the optional tag, attributes, and class_name."""
        return self._find_recursive(
            self.root,
            lambda el: (predicate(el) if predicate else True)
            and self._matches(el, tag, attributes, class_name),
        )

    def find_many(
        self,
        predicate: Optional[Callable[[HTMLElement], bool]] = None,
        tag: Optional[str] = None,
        attributes: Optional[Dict[str, str]] = None,
        class_name: Optional[str] = None,
    ) -> List[HTMLElement]:
        """Finds all elements that match the predicate or the optional tag, attributes, and class_name."""
        results = []
        self._find_many_recursive(
            self.root,
            lambda el: (predicate(el) if predicate else True)
            and self._matches(el, tag, attributes, class_name),
            results,
        )
        return results

    def find_first(
        self,
        predicate: Optional[Callable[[HTMLElement], bool]] = None,
        tag: Optional[str] = None,
        attributes: Optional[Dict[str, str]] = None,
        class_name: Optional[str] = None,
    ) -> Optional[HTMLElement]:
        """Finds the first element that matches the predicate or the optional tag, attributes, and class_name."""
        return self.find_unique(
            predicate=predicate, tag=tag, attributes=attributes, class_name=class_name
        )

    def count(
        self,
        predicate: Optional[Callable[[HTMLElement], bool]] = None,
        tag: Optional[str] = None,
        attributes: Optional[Dict[str, str]] = None,
        class_name: Optional[str] = None,
    ) -> int:
        """Counts the number of elements that match the predicate or the optional tag, attributes, and class_name."""
        return len(
            self.find_many(
                predicate=predicate,
                tag=tag,
                attributes=attributes,
                class_name=class_name,
            )
        )

    def get_text(self, element: HTMLElement) -> str:
        """Returns the text content of an element (including nested text)."""
        return self._get_text_recursive(element)

    def get_children(
        self, element: HTMLElement
    ) -> List[Union[HTMLElement, HTMLPlainText]]:
        """Returns the direct children of an element."""
        return element.children if element and element.children else []

    def get_descendants(
        self, element: HTMLElement
    ) -> List[Union[HTMLElement, HTMLPlainText]]:
        """Returns all descendants of an element."""
        descendants = []
        self._get_descendants_recursive(element, descendants)
        return descendants

    def get_by_id(self, element_id: str) -> Optional[HTMLElement]:
        """Finds a unique element by its id."""
        return self.find_unique(attributes={"id": element_id})

    def get_by_class(self, class_name: str) -> List[HTMLElement]:
        """Finds all elements with a specific class."""
        return self.find_many(class_name=class_name)

    def select(self, element: HTMLElement, fields: List[str]) -> Dict[str, Any]:
        """
        Select specific fields from an element.
        Example fields: ["tag", "attributes", "children"]
        """
        result = {}
        for field in fields:
            if hasattr(element, field):
                result[field] = getattr(element, field)
        return result
    
    def exclude(
        self,
        list_of_elements: List[HTMLElement],
        tags_to_remove: Callable[[HTMLElement], Any]
    ) -> List[HTMLElement]:
        """
        Removes elements from the list of elements that match the predicate (tags_to_remove).
        """
        filtered_elements = []

        for element in list_of_elements:
            if not tags_to_remove(element):
                element.children = self.exclude(element.children, tags_to_remove)
                filtered_elements.append(element)

        return filtered_elements
        

    def include(
        self, element: HTMLElement, relations: Dict[str, Callable[[HTMLElement], Any]]
    ) -> Dict[str, Any]:
        """
        Include related data or extra information about the element.
        The `relations` parameter is a dictionary of field names (like 'children', 'descendants')
        mapped to a function that fetches or processes that field.
        """
        result = {}
        for key, relation_fn in relations.items():
            result[key] = relation_fn(element)
        return result

    def _matches(
        self,
        element: HTMLElement,
        tag: Optional[str],
        attributes: Optional[Dict[str, str]],
        class_name: Optional[str],
    ) -> bool:
        """Helper function to check if an element matches the provided tag, attributes, and class_name."""
        if tag and element.tag != tag:
            return False
        if attributes:
            for key, value in attributes.items():
                if element.attributes.get(key) != value:
                    return False
        if class_name and class_name not in element.attributes.get("class", "").split():
            return False
        return True

    def _find_recursive(
        self, element: HTMLElement, predicate: Callable[[HTMLElement], bool]
    ) -> Optional[HTMLElement]:
        """Helper function for finding a single matching element."""
        if predicate(element):
            return element
        for child in element.children:
            if isinstance(child, HTMLElement):
                result = self._find_recursive(child, predicate)
                if result:
                    return result
        return None

    def _find_many_recursive(
        self,
        element: HTMLElement,
        predicate: Callable[[HTMLElement], bool],
        results: List[HTMLElement],
    ):
        """Helper function for finding multiple matching elements."""
        if predicate(element):
            results.append(element)
        for child in element.children:
            if isinstance(child, HTMLElement):
                self._find_many_recursive(child, predicate, results)

    def _get_text_recursive(self, element: HTMLElement) -> str:
        """Helper function for extracting text content from an element."""
        text_content = ""
        for child in element.children:
            if isinstance(child, HTMLPlainText):
                text_content += child.text
            elif isinstance(child, HTMLElement):
                text_content += self._get_text_recursive(child)
        return text_content

    def _get_descendants_recursive(
        self, element: HTMLElement, descendants: List[Union[HTMLElement, HTMLPlainText]]
    ):
        """Helper function for getting all descendants of an element."""
        for child in element.children:
            descendants.append(child)
            if isinstance(child, HTMLElement):
                self._get_descendants_recursive(child, descendants)



