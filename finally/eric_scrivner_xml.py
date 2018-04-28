#!/usr/bin/python
import xml.etree.ElementTree
 
# (c) Copyright 2015 Eric Scrivner.
# https://ericscrivner.me/2015/07/python-tip-convert-xml-tree-to-a-dictionary/
def make_dict_from_tree(element_tree):
    """Traverse the given XML element tree to convert it into a dictionary.
 
    :param element_tree: An XML element tree
    :type element_tree: xml.etree.ElementTree
    :rtype: dict
    """
    def internal_iter(tree, accum):
        """Recursively iterate through the elements of the tree accumulating
        a dictionary result.
 
        :param tree: The XML element tree
        :type tree: xml.etree.ElementTree
        :param accum: Dictionary into which data is accumulated
        :type accum: dict
        :rtype: dict
        """
        if tree is None:
            return accum
 
        if tree.getchildren():
            accum[tree.tag] = {}
            for each in tree.getchildren():
                result = internal_iter(each, {})
                if each.tag in accum[tree.tag]:
                    if not isinstance(accum[tree.tag][each.tag], list):
                        accum[tree.tag][each.tag] = [
                            accum[tree.tag][each.tag]
                        ]
                    accum[tree.tag][each.tag].append(result[each.tag])
                else:
                    accum[tree.tag].update(result)
        else:
            accum[tree.tag] = tree.text
 
        return accum
 
    return internal_iter(element_tree, {})
