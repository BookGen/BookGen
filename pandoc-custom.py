#!/usr/bin/env python3

"""
Pandoc custom filters.
"""

from panflute import *

def prepare(doc):
	for name in ['prepare', 'action', 'finalize']:
		codes = doc.get_metadata('filter.' + name, builtin=False)
		if codes:
			setattr(
				doc, name, compile(
					'\n'.join(
						[
							x.text for x in (
								codes.content if isinstance(
									codes, MetaBlocks
								) else [codes]
							) if (
								isinstance(x, CodeBlock) or (
									isinstance(x, RawBlock) and (
										x.format == doc.format or
										x.format in ['html', 'html5'] and
										doc.format in ['html', 'html5']
									)
								)
							)
						]
					),
				'<filter.' + name + '>', 'exec')
			)
	if hasattr(doc, 'prepare'):
		exec(doc.prepare, globals(), {'doc': doc})

def action(elem, doc):
	if hasattr(doc, 'action'):
		result = None
		exec(doc.action)
		return result

def finalize(doc):
	if hasattr(doc, 'finalize'):
		exec(doc.finalize, globals(), {'doc': doc})
	for name in ['prepare', 'action', 'finalize']:
		if hasattr(doc, name):
			delattr(doc, name)

def main(doc=None):
	return run_filter(action, doc=doc, prepare=prepare, finalize=finalize)

if __name__ == "__main__":
	main()
