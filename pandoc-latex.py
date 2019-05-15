#!/usr/bin/env python

"""
Pandoc LaTeX filters.
"""

from panflute import *
import re

madelettrine = False

def makelettrine(elem,doc):
	global madelettrine
	if madelettrine:
		pass
	elif isinstance(elem, Str) and len(elem.text) > 0:
		madelettrine = True
		return [
			RawInline('\\lettrine{', format='latex'),
			Str(elem.text[0]),
			RawInline('}{', format='latex'),
			Str(elem.text[1:])
		]

def action(elem, doc):
	global madelettrine
	if isinstance(elem, RawInline) and elem.format=='html':
		if elem.text.startswith('<link'):
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
		if elem.text.startswith('<meta') or elem.text.startswith("<script") or elem.text.startswith("<style"):
			return []
		elif re.match(r'^<hr */?>$', elem.text):
			return RawBlock('\\fancybreak{\\pfbreakdisplay}', format='latex')
		elif re.match(r'^<hr +class="plain" */?>$', elem.text):
			return RawBlock('\plainbreak{1}', format='latex')
	elif isinstance(elem, HorizontalRule):
		return RawBlock('\\fancybreak{\\pfbreakdisplay}', format='latex')
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
	elif isinstance(elem, Div):
		if 'chapterprecis' in elem.classes:
			if len(elem.content) == 1 and isinstance(elem.content[0], Para):
				return [
					RawBlock('\\chapterprecishere{', format='latex'),
					Div(*elem.content[0].content),
					RawBlock('}', format='latex')
				]
			return [
				RawBlock('\\chapterprecishere{', format='latex'),
				Div(*elem.content),
				RawBlock('}', format='latex')
			]
	elif isinstance(elem, Span):
		if 'lettrine' in elem.classes and len(elem.content) > 0:
			madelettrine = False
			elem.walk(makelettrine)
			return elem.content.list + [RawInline('}', format='latex')]
		if 'at' in elem.classes and len(elem.content) == 0:
			return RawInline('\@', format='latex')

def main(doc=None):
	return run_filter(action, doc=doc)

if __name__ == "__main__":
	main()
