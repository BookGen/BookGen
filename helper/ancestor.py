from panflute import *

def metadata(elem):
	ancestor = elem.parent
	while ancestor and not isinstance(ancestor, MetaValue):
		if isinstance(ancestor, Doc):
			return False
		ancestor = ancestor.parent
	return True

def where(elem, test):
	ancestor = elem.parent
	while ancestor and not test(ancestor):
		if isinstance(ancestor, Doc):
			return None
		ancestor = ancestor.parent
	return ancestor
