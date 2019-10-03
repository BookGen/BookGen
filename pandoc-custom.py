#!/usr/bin/env python3

"""
Pandoc custom filters.
"""

from panflute import *

def prepare(doc):
	for name in ['prepare', 'action', 'finalize']:
		code = doc.get_metadata('filter.' + name)
		if code:
			setattr(doc, name, compile(code, '<filter.' + name + '>', 'exec'))
	if hasattr(doc, 'prepare'):
		exec(doc.prepare)

def action(elem, doc):
	if hasattr(doc, 'action'):
		result = None
		exec(doc.action)
		return result

def finalize(doc):
	if hasattr(doc, 'finalize'):
		exec(doc.finalize)
	for name in ['prepare', 'action', 'finalize']:
		if hasattr(doc, name):
			delattr(doc, name)

def main(doc=None):
	return run_filter(action, doc=doc, prepare=prepare, finalize=finalize)

if __name__ == "__main__":
	main()
