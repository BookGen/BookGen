#!/usr/bin/env python

"""
Pandoc HTML filters.
"""

from panflute import *

madelettrine = False

def makelettrine(elem,doc):
	global madelettrine
	if madelettrine:
		pass
	elif isinstance(elem, Str) and len(elem.text) > 0:
		madelettrine = True
		return [
			RawInline('<b>', format='html'),
			Str(elem.text[0]),
			RawInline('</b>', format='html'),
			Str(elem.text[1:])
		]

def action(elem, doc):
	global madelettrine
	if isinstance(elem, Span):
		if 'lettrine' in elem.classes and len(elem.content) > 0:
			madelettrine = False
			elem.walk(makelettrine)
		elif 'data-colour' in elem.attributes or 'data-color' in elem.attributes:
			return Span(*elem.content, identifier=elem.identifier, classes=elem.classes, attributes=dict( { 'style': 'color: ' + elem.attributes.get('data-colour', elem.attributes.get('data-color')) }, **elem.attributes))
		elif 'at' in elem.classes and len(elem.content) == 0:
			return []

def main(doc=None):
	return run_filter(action, doc=doc)

if __name__ == "__main__":
	main()
