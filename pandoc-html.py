#!/usr/bin/env python3

"""
Pandoc HTML filters.
"""

from panflute import *

def action(elem, doc):
	if isinstance(elem, Header):
		if elem.level == 1:
			return Header(*elem.content, attributes=elem.attributes, classes=(elem.classes[:] if doc.get_metadata('type') == 'chapter' or doc.get_metadata('type') == 'appendix' else ['unnumbered'] + elem.classes), identifier=elem.identifier, level=1)
	elif isinstance(elem, LineBlock):
		result = []
		for item in elem.content.list:
			if isinstance(item, LineItem):
				indented = False
				if isinstance(item.content[0], Span) and len(item.content[0].content) == 0 and 'indent' in item.content[0].classes:
					indented = True
					itemcontent = item.content.list[1:] + [LineBreak()]
				else:
					itemcontent = item.content.list + [LineBreak()]
				result += [Span(*itemcontent, classes=(['line-item', 'indented'] if indented else ['line-item']))]
			else:
				result += [item]
		return Div(Para(*result), classes=['line-block'])
	elif isinstance(elem, Span):
		if len(elem.content) == 0 and 'at' in elem.classes:
			return []
		elif 'data-colour' in elem.attributes or 'data-color' in elem.attributes:
			return Span(*elem.content, identifier=elem.identifier, classes=elem.classes, attributes=dict({ 'style': 'color: ' + elem.attributes.get('data-colour', elem.attributes.get('data-color')) }, **elem.attributes))

def main(doc=None):
	return run_filter(action, doc=doc)

if __name__ == "__main__":
	main()
