#!/usr/bin/env python3

"""
Pandoc custom filters.
"""

from panflute import *
from helper import *
from importlib import import_module

def prepare(doc):
	filterprop = doc.get_metadata('filter')
	filters = {}
	if isinstance(filterprop, str):
		try:
			filters = import_module(filterprop)
		except ImportError:
			pass
	for name in ['prepare', 'action', 'finalize']:
		fn = getattr(filters, name, None)
		codes = doc.get_metadata('filter.' + name, builtin=False)
		if callable(fn) or codes:
			setattr(doc, '_BookGen__' + name, fn if callable(fn) else compile('\n'.join([
				x.text for x in (
					codes.content if isinstance(codes, MetaBlocks) else [codes]
				) if (
					isinstance(x, CodeBlock) or (
						isinstance(x, RawBlock) and (
							x.format == doc.format or
							x.format in ['html', 'html5'] and
							doc.format in ['html', 'html5']
						)
					)
				)
			]), '<filter.' + name + '>', 'exec'))
	if hasattr(doc, '_BookGen__custom_prepare'):
		exec(doc._BookGen__custom_prepare, globals(), {'doc': doc})

def action(elem, doc):
	if hasattr(doc, '_BookGen__custom_action'):
		result = None
		exec(doc._BookGen__custom_action)
		return result

def finalize(doc):
	if hasattr(doc, '_BookGen__custom_finalize'):
		exec(doc._BookGen__custom_finalize, globals(), {'doc': doc})
	for name in [
		'_BookGen__custom_prepare',
		'_BookGen__custom_action',
		'_BookGen__custom_finalize'
	]:
		if hasattr(doc, name):
			delattr(doc, name)

def main(doc=None):
	return run_filter(action, doc=doc, prepare=prepare, finalize=finalize)

if __name__ == '__main__':
	main()
