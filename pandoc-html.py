#!/usr/bin/env python3

"""
Pandoc HTML filters.
"""

from panflute import *
from helper import *
from collections import OrderedDict
from xml.sax.saxutils import escape

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
		doc.metadata['localization-' + name] = metadata.text(doc, 'localization-' + name)

def sanitize_styles(doc):
	styles = doc.get_metadata('styles')
	result = None
	if isinstance(styles, MetaList):
		result = MetaList()
		for index, stylemap in enumerate(styles):
			if isinstance(stylemap, MetaMap):
				name = stylemap.get('name', None)
				text = content.text(stylemap.get('css', None), doc)
				if name and text:
					result.append((name, text))
	if result:
		doc.metadata.content['styles'] = result
	elif hasattr(doc.metadata, 'styles'):
		del doc.metadata.content.styles

def sanitize_template_metadata(doc):
	sanitize_localization(doc)
	for name in [
		'lang',
		'dir',
		'draft',
		'style',
		'type'
	]:
		doc.metadata[name] = metadata.text(doc, name)
	chapter = -1
	try:
		chapter = int(metadata.text(doc, 'chapter'))
	except ValueError:
		pass
	if chapter >= 0:
		doc.metadata['chapter'] = str(chapter)
	elif hasattr(doc.metadata, 'chapter'):
		del doc.metadata.content.chapter
	type = doc.get_metadata('type')
	doc.metadata['noun'] = metadata.text(doc, 'noun', metadata.text(doc, 'localization-type-' + type, type.title()))
	doc.metadata['final'] = MetaBool(bool(metadata.text(doc, 'final')))
	sanitize_styles(doc)

def make_title(doc):
	title = ''
	data = metadata.text(doc, 'series')
	if data:
		title += data + u' \u2013 '
	data = metadata.text(doc, 'title')
	if data:
		title += data
	data = metadata.text(doc, 'type')
	if data != 'standalone':
		title += ': ' + metadata.text(doc, 'localization-type-' + data, { 'index': 'Contents', 'biblio': 'Bibliography'}.get(data, data.title()))
	chapter = int(metadata.text(doc, 'chapter', -1))
	if chapter >= 0:
		title += (' 0' if chapter < 10 else ' ') + str(chapter)
	return title

def metas(doc):
	result = []
	for name in ['author', 'publisher', 'description']:
		value = []
		data = doc.get_metadata(name, builtin=False)
		if isinstance(data, MetaList):
			for item in data:
				value.append(content.text(item, doc))
		else:
			value.append(content.text(data, doc))
		result.extend([
			RawBlock('<meta name="' + name + '" content="' + escape(x, entities={'"': '&quot;'}) + '"/>', format='html') for x in value if x
		])
	data = doc.get_metadata('keywords', builtin=False)
	value = []
	if isinstance(data, MetaList):
		for item in data:
			value.append(content.text(item, doc))
	else:
		value.append(content.text(data, doc))
	value = ','.join(escape(x, entities={'"': '&quot;'}) for x in value if x)
	if value:
		result.append(
			RawBlock('<meta name="keywords" content="' + value + '"/>', format='html')
		)
	return result

def links(doc):
	result = []
	for name, rel in OrderedDict([
		('self', 'canonical'),
		('homepage', 'home'),
		('index', 'contents directory index toc'),
		('first', 'first start'),
		('prev','prev'),
		('next', 'next'),
		('last', 'last'),
		('repository', 'code-repository')
	]).items():
		href = metadata.text(doc, name)
		if href:
			result.append(RawBlock('<link rel="' + rel + '" href="' + escape(href, entities={'"': '&quot;'}) + '" data-external="1"/>'))
	return result

def prepare(doc):
	pass

def action(elem, doc):
	if isinstance(elem, Header):
		if elem.level == 1 and metadata.text(doc, 'type') in ['chapter', 'appendix']:
			elem.classes = ['unnumbered'] + elem.classes
	elif isinstance(elem, LineBlock):
		result = Para()
		for item in elem.content:
			if isinstance(item, LineItem):
				indented = False
				if isinstance(item.content[0], Span) and len(item.content[0].content) == 0 and 'indent' in item.content[0].classes:
					indented = True
					item.content.pop(0)
				item.content.append(LineBreak())
				result.content.append(
					Span(*item.content, classes=(['line-item', 'indented'] if indented else ['line-item']))
				)
			else:
				result.content.append(item)
		return Div(result, classes=['line-block'])
	elif isinstance(elem, Div):
		if 'data-from-metadata' in elem.attributes:
			elem.content = metadata.blocks(doc, elem.attributes.get('data-from-metadata'))
		# Keep going…
		if 'plain' in elem.classes:
			if len(elem.content) == 1 and isinstance(elem.content[0], Para):
				return Plain(*elem.content[0].content)
	elif isinstance(elem, Span):
		if 'data-from-metadata' in elem.attributes:
			elem.content = metadata.inlines(doc, elem.attributes.get('data-from-metadata'))
		# Keep going…
		if len(elem.content) == 0 and 'at' in elem.classes:
			return []
		elif 'data-colour' in elem.attributes or 'data-color' in elem.attributes:
			elem.attributes = dict({ 'style': 'color: ' + elem.attributes.get('data-colour', elem.attributes.get('data-color')) }, **elem.attributes)

def finalize(doc):
	sanitize_template_metadata(doc)
	header_includes = doc.get_metadata('header-includes', MetaBlocks(), builtin=False)
	if isinstance(header_includes, MetaInlines):
		header_includes = MetaBlocks(Plain(*header_includes.content))
	elif isinstance(header_includes, MetaString):
		header_includes = MetaBlocks(Plain(Str(header_includes.text)))
	elif not isinstance(header_includes, MetaBlocks):
		header_includes = MetaBlocks()
	header_includes.walk(ignore.do)
	header_text = content.text(header_includes)
	if not ('<title>' in header_text):
		header_includes.content.append(RawBlock('<title>' + escape(make_title(doc)) + '</title>', format='html'))
	header_includes.content.extend(metas(doc))
	header_includes.content.extend(links(doc))

def main(doc=None):
	return run_filter(action, doc=doc, prepare=prepare, finalize=finalize)

if __name__ == '__main__':
	main()
