from panflute import *

def should(elem, doc=None):
	return (
		isinstance(elem, RawBlock) or isinstance(elem, RawInline)
	) and not (doc and
		(doc.format == elem.format or doc.format == 'html5' and elem.format == 'html')
	)

def do(elem, doc=None):
	if should(elem, doc):
		return []
