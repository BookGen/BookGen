#!/usr/bin/env python
# coding: utf-8

"""
Pandoc LaTeX filters.
"""

from panflute import *
from helper import *
import re

def sanitize_localization(doc):
	for name in [
		'appendices',
		'chapters',
		'draft',
		'index',
		'top',
		'type-appendix',
		'type-biblio',
		'type-chapter',
		'type-index',
		'type-standalone'
	]:
		doc.metadata['localization-' + name] = MetaInlines(*metadata.inlines(doc, 'localization-' + name))

def sanitize_template_metadata(doc):
	sanitize_localization(doc)
	for name in [
		'draft',
		'filename',
		'style',
		'type'
	]:
		doc.metadata[name] = MetaString(metadata.text(doc, name))
	number = -1
	try:
		number = int(metadata.text(doc, 'number'))
	except ValueError:
		pass
	if number >= 0:
		doc.metadata['number'] = MetaString(str(number))
	elif hasattr(doc.metadata, 'number'):
		del doc.metadata.content.number
	type = metadata.text(doc, 'type')
	doc.metadata['noun'] = MetaString(metadata.text(doc, 'noun', metadata.text(doc, 'localization-type-' + type, type.title())))
	final = doc.get_metadata('final', builtin=False)
	doc.metadata['final'] = MetaBool(bool(final.boolean if isinstance(final, MetaBool) else content.text(final, doc)))

def defines(doc):
	result = [RawInline('% Metadata %', format='latex')]
	for name, command in [
		('author', 'authorinfo'),
		('description', 'descriptioninfo'),
		('download', 'downloaduri'),
		('draft', 'draftinfo'),
		('homepage', 'homepageuri'),
		('noun', 'nouninfo'),
		('profile', 'profileuri'),
		('publisher', 'publisherinfo'),
		('repository', 'repositoryuri'),
		('rights', 'rightsinfo'),
		('series', 'seriesinfo'),
		('style', 'styleinfo'),
		('title', 'titleinfo'),
		('type', 'bookgentype'),
		('year', 'yearinfo')
	]:
		value = []
		data = doc.get_metadata(name, builtin=False)
		if isinstance(data, MetaList):
			for item in data:
				value.extend(content.inlines(item, doc))
		else:
			value.extend(content.inlines(data, doc))
		result.extend([
			RawInline('\n\\renewcommand{\\' + command + '}', format='latex'),
			Span(*value)
		])
	data = doc.get_metadata('keywords', builtin=False)
	value = []
	if isinstance(data, MetaList):
		for item in data:
			value.extend(content.inlines(item, doc) + [Str(', ')])
		value.pop() # The final comma is unnecessary
	else:
		value.extend(content.inlines(data, doc))
	result.extend([
		RawInline('\\renewcommand{\\keywordsinfo}', format='latex'),
		Span(*value)
	])
	return result

def unindent(elem, doc):
	if doc.unindented:
		pass
	elif isinstance(elem, Para):
		elem.content.insert(0, RawInline('\\noindent{}', format='latex'))
		doc.unindented = True

def prepare(doc):
	doc.unindented = False

def action(elem, doc):
	if isinstance(elem, RawInline) and elem.format=='html':
		match = re.match(r'<(/?)([^\s>]+)[\s>]', elem.text)
		if match:
			closing = match.group(1)
			name = match.group(2)
			textformat = {
				'b': 'attnfont',
				'cite': 'citefont',
				'code': 'codefont',
				'del': 'deletefont',
				'dfn': 'termfont',
				'i': 'offsetfont',
				'ins': 'insertfont',
				's': 'strikefont',
				'small': 'smallfont'
			}.get(name, None)
			if textformat:
				return RawInline('}', format='latex') if closing else RawInline('{\\' + textformat + '{}', format='latex')
			elif name == 'link' or (closing and name in ['br', 'wbr']):
				return []
			elif name == 'br':
				return LineBreak()
			elif name == 'wbr':
				return RawInline('\\linebreak[0]{}', format='latex')
	elif isinstance(elem, RawBlock) and elem.format=='html':
		match = re.match(r'<(/?)(\w+)[\s>]', elem.text)
		if match:
			closing = match.group(1)
			name = match.group(2)
			if name in ['link', 'meta', 'script', 'style', 'title']:
				return []
			elif name in ['hr', 'hr/']:
				if re.match(r'^<hr +class="plain" */?>$', elem.text):
					return RawBlock('\\plainbreak{1}', format='latex')
				return RawBlock('\\fancybreak{\\pfbreakdisplay}', format='latex')
	elif isinstance(elem, HorizontalRule):
		return RawBlock('\\fancybreak{\\pfbreakdisplay}', format='latex')
	elif isinstance(elem, Link):
		if 'uri' in elem.classes:
			return [
				RawInline('\\url', format='latex'),
				Span(*elem.content)
			]
		return [
			RawInline('\\href{' + elem.url.replace('%', '\\%').replace('#', '\\#') + '}{{\\linkfont{}', format='latex'),
			Span(*elem.content),
			RawInline('}}', format='latex')
		]
	elif isinstance(elem, BlockQuote):
		return [
			RawBlock('\\begin{quoting}', format='latex'),
			Div(*elem.content),
			RawBlock('\\end{quoting}', format='latex')
		]
	elif isinstance(elem, Div):
		if 'data-from-metadata' in elem.attributes:
			value = doc.get_metadata(elem.attributes.get('data-from-metadata'), builtin=False)
			if isinstance(value, MetaString):
				elem.content = [Plain(Str(value.text))]
			elif isinstance(value, MetaInlines):
				elem.content = [Plain(*value.content)]
			elif isinstance(value, MetaBlocks):
				elem.content = value.content
			else:
				value = text_content(value, doc)
				if value:
					elem.content = [Plain(Str(value))]
		# Keep going…
		if 'plain' in elem.classes:
			if len(elem.content) == 1 and isinstance(elem.content[0], Para):
				return Plain(*elem.content[0].content)
		elif 'chapterprecis' in elem.classes:
			if len(elem.content) == 1 and isinstance(elem.content[0], Para):
				return [
					RawBlock('\\chapterprecishere{', format='latex'),
					elem.content[0],
					RawBlock('}', format='latex')
				]
			return [
				RawBlock('\\chapterprecishere{', format='latex'),
				Div(*elem.content),
				RawBlock('}', format='latex')
			]
		elif 'verse' in elem.classes:
			result = [RawBlock('\\begin{verse}\\versefont{}', format='latex')]
			if 'alternating' in elem.classes:
				for subelem in elem.content.list:
					if isinstance(subelem, LineBlock):
						result += [
							RawBlock('\\begin{altverse}', format='latex'),
							subelem,
							RawBlock('\\end{altverse}', format='latex')
						]
					else:
						result += [subelem]
			else:
				result += elem.content.list
			return result + [RawBlock('\\end{verse}', format='latex')]
		elif elem.attributes.get('role') == 'note':
			unindented = False
			elem.walk(unindent)
			return [
				RawBlock('\\begin{snugshade}', format='latex'),
				Div(*elem.content),
				RawBlock('\\end{snugshade}', format='latex')
			]
		elif 'continuation' in elem.classes:
			doc.unindented = False
			elem.walk(unindent)
	elif isinstance(elem, Header):
		if elem.level == 1 and metadata.text(doc, 'type') not in ['chapter', 'appendix']:
			elem.classes.append('unnumbered')
	elif isinstance(elem, Span):
		if 'data-from-metadata' in elem.attributes:
			value = doc.get_metadata(elem.attributes.get('data-from-metadata'), builtin=False)
			if isinstance(value, MetaString):
				elem.content = [Str(value.text)]
			elif isinstance(value, MetaInlines):
				elem.content = value.content
			else:
				value = text_content(value, doc)
				if value:
					elem.content = [Str(value)]
		# Keep going…
		if 'lettrine' in elem.classes and len(elem.content) > 0:
			if isinstance(elem.content[0], Span):
				elem.content = [
					RawInline('\\lettrine', format='latex'),
					elem.content[0],
					Span(*elem.content.list[1:])
				]
			else:
				elem.content.insert(0, RawInline('\\LettrineTextFont{}', format='latex'))
		elif 'data-colour' in elem.attributes or 'data-color' in elem.attributes:
			colour = elem.attributes.get('data-colour', elem.attributes.get('data-color'))
			if colour == 'RebeccaPurple':
				colour = '#663399' # Not supported out­‑of­‑the­‑box in `xcolor`
			return [
				RawInline('\\textcolor'+ ('[HTML]' if colour[0] == '#' else '[named]') +'{' + (colour[1:] if colour[0] == '#' else colour) + '}', format='latex'),
				Span(*elem.content)
			]
		elif 'data-font' in elem.attributes:
			result = [RawInline('\\' + elem.attributes.get('data-font') + '{}', format='latex')] + elem.content.list
			return Span(*result)
		elif len(elem.content) == 0:
			if 'at' in elem.classes:
				return RawInline('\\@', format='latex')
			elif 'indent' in elem.classes:
				return RawInline('\\vin{}', format='latex')
	elif isinstance(elem, Strikeout):
		return [
			RawInline('{\strikefont{}', format='latex'),
			Span(*elem.content),
			RawInline('}')
		]

def finalize(doc):
	sanitize_template_metadata(doc)
	header_includes = MetaBlocks(*metadata.blocks(doc, 'header-includes'))
	header_includes.walk(ignore.do, doc)
	header_includes.content.append(Plain(*defines(doc)))
	doc.metadata['header-includes'] = header_includes
	del doc.unindented

def main(doc=None):
	return run_filter(action, doc=doc, prepare=prepare, finalize=finalize)

if __name__ == '__main__':
	main()
