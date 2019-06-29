#!/usr/bin/env python
# coding: utf-8

"""
Pandoc LaTeX filters.
"""

from panflute import *
import re

madelettrine = False
unindented = False

def isOneOf(elem,names):
	for name in names:
		if elem.text=='<'+name+'>' or elem.text.startswith('<'+name+' '):
			return True
	return False

def unindent(elem,doc):
	global unindented
	if unindented:
		pass
	elif isinstance(elem, Para):
		unindented = True
		result = [RawInline('\\noindent ', format='latex')] + elem.content.list
		return Para(*result)

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
		if isOneOf(elem,['link','/link','/br','/wbr']):
			return []
		elif isOneOf(elem,['b']):
			return RawInline('\\textbf{', format='latex')
		elif isOneOf(elem,['dfn']):
			return RawInline('\\textbf{\\textit{', format='latex')
		elif isOneOf(elem,['cite','i']):
			return RawInline('\\textit{', format='latex')
		elif isOneOf(elem,['del','s']):
			return RawInline('\\sout{', format='latex')
		elif isOneOf(elem,['ins']):
			return RawInline('\\uuline{', format='latex')
		elif isOneOf(elem,['small']):
			return RawInline('{\small{}', format='latex')
		elif isOneOf(elem,['br']):
			return LineBreak()
		elif isOneOf(elem,['wbr']):
			return RawInline('\\linebreak[0]{}', format='latex')
		elif isOneOf(elem,['/b','/cite','/i','/del','/s','/ins','/small']):
			return RawInline('}', format='latex')
		elif isOneOf(elem,['/dfn']):
			return RawInline('}}', format='latex')
	elif isinstance(elem, RawBlock):
		if isOneOf(elem,['meta','script','style','/meta','/script','/style']):
			return []
		elif isOneOf(elem,['hr']):
			if re.match(r'^<hr +class="plain" */?>$', elem.text):
				return RawBlock('\plainbreak{1}', format='latex')
			return RawBlock('\\fancybreak{\\pfbreakdisplay}', format='latex')
	elif isinstance(elem, HorizontalRule):
		return RawBlock('\\fancybreak{\\pfbreakdisplay}', format='latex')
	elif isinstance(elem, Link):
		if 'uri' in elem.classes:
			return [
				RawInline(u'\\url'),
				Span(*elem.content)
			]
		return [
			RawInline(u'\\href{' + elem.url.replace('%', '\\%') + u'}{\\dashuline', format='latex'),
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
					Para(*elem.content[0].content),
					RawBlock('}', format='latex')
				]
			return [
				RawBlock('\\chapterprecishere{', format='latex'),
				Div(*elem.content),
				RawBlock('}', format='latex')
			]
		elif elem.attributes['role'] == 'note':
			unindented = False
			elem.walk(unindent)
			return [
				RawBlock('\\begin{snugshade}', format='latex'),
				Div(*elem.content),
				RawBlock('\\end{snugshade}', format='latex')
			]
	elif isinstance(elem, Header):
		if elem.level == 1:
			return Header(*elem.content, attributes=elem.attributes, classes=(elem.classes[:] if doc.get_metadata('type') == 'chapter' or doc.get_metadata('type') == 'appendix' else ['unnumbered'] + elem.classes), identifier=elem.identifier, level=1)
	elif isinstance(elem, Span):
		if 'lettrine' in elem.classes and len(elem.content) > 0:
			madelettrine = False
			elem.walk(makelettrine)
			return elem.content.list + [RawInline('}', format='latex')]
		elif 'data-colour' in elem.attributes or 'data-color' in elem.attributes:
			colour = elem.attributes.get('data-colour', elem.attributes.get('data-color'))
			if colour == 'RebeccaPurple':
				colour = '#663399' # Not supported out­‑of­‑the­‑box in `xcolor`
			return [
				RawInline('\\textcolor'+ ('[HTML]' if colour[0] == '#' else '[named]') +'{' + (colour[1:] if colour[0] == '#' else colour) + '}', format='latex'),
				Span(*elem.content)
			]
		elif 'at' in elem.classes and len(elem.content) == 0:
			return RawInline('\\@', format='latex')
	elif isinstance(elem, Strikeout):
		return [
			RawInline('\sout{', format='latex'),
			Span(*elem.content),
			RawInline('}')
		]

def main(doc=None):
	return run_filter(action, doc=doc)

if __name__ == "__main__":
	main()
