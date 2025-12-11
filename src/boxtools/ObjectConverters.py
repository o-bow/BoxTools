#!/usr/bin/env python3
class MapConverter:
    def __init__(self):
        self.idx = 0

    def _add_element(self, value):
        element = [self.idx, value]
        self.idx += 1
        return element

    def _add_idx_to_element(self, value):
        element = '(' + str(self.idx) + ' ) ' + value
        self.idx += 1
        return element

    def _update_element(self, element):
        return [self._add_idx_to_element(element), element]

    def list_to_map(self, value_list: list) -> map:
        return map(self._add_element, value_list)

    def add_index_to_key(self, value_map: map) -> map:
        return map(self._update_element, value_map)


class ListConverter:
    def __init__(self):
        self.separator = ''

    def _convert_element(self, element):
        a_s_element = map(str, element)
        return self.separator.join(list(a_s_element))

    def map_to_list(self, elements: map, separator: str) -> list:
        self.separator = separator
        return list(map(self._convert_element, elements))
