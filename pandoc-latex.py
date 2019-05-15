#!/usr/bin/env python

"""
Pandoc LaTeX filters.
"""

from panflute import *
import re

def action(elem, doc):
	if isinstance(elem, RawInline) and elem.format=='html':
		if elem.text.startswith('<meta') or elem.text.startswith('<link'):
			return []
		elif elem.text=='<b>':
			return RawInline('\\textbf{', format='latex')
		elif elem.text=='<dfn>':
			return RawInline('\\textbf{\\emph{', format='latex')
		elif elem.text=='<cite>' or elem.text=='<i>':
			return RawInline('\\emph{', format='latex')
		elif elem.text=='<small>':
			return RawInline('{\small{}', format='latex')
		elif re.match(r'^<br */?>$', elem.text):
			return LineBreak()
		elif re.match(r'^<wbr */?>$', elem.text):
			return RawInline('\\linebreak[0]{}', format='latex')
		elif elem.text=='</b>' or elem.text=='</cite>' or elem.text=='</i>' or elem.text=='</small>':
			return RawInline('}', format='latex')
		elif elem.text=='</dfn>':
			return RawInline('}}', format='latex')
	elif isinstance(elem, RawBlock):
		if elem.text.startswith("<script") or elem.text.startswith("<style"):
			return []
		elif re.match(r'^<hr */?>$', elem.text):
			return RawBlock('\\pfbreak{}', format='latex')
	elif isinstance(elem, HorizontalRule):
		return RawBlock('\\pfbreak{}', format='latex')
	elif isinstance(elem, Link):
		return [
			RawInline(u'\\link{' + elem.url.replace('%', '\\%') + u'}{', format='latex'),
			Span(*elem.content),
			RawInline('}', format='latex')
		]
	elif isinstance(elem, BlockQuote):
		return [
			RawBlock('\\begin{quoting}', format='latex'),
			Div(*elem.content),
			RawBlock('\\end{quoting}', format='latex')
		]

def main(doc=None):
	return run_filter(action, doc=doc)

if __name__ == "__main__":
	main()
