from panflute import *

def metadata(elem):
	ancestor = elem.parent
	while ancestor and not isinstance(ancestor, MetaValue):
		if isinstance(ancestor, Doc):
			return False
		ancestor = ancestor.parent
	return True
