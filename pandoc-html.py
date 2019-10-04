#!/usr/bin/env python3

"""
Pandoc HTML filters.
"""

from panflute import *
from functools import partial
from collections import OrderedDict
from xml.sax.saxutils import escape

def is_ignorable(elem, doc=None):
	return (
		isinstance(elem, RawBlock) or isinstance(elem, RawInline)
	) and not (doc and
		(doc.format == elem.format or doc.format == 'html5' and elem.format == 'html')
	)

def ignore(elem, doc=None):
	if is_ignorable(elem, doc):
		return []

def add_text_content(elem, doc=None, to=[]):
	if is_ignorable(elem, doc):
		pass
	elif hasattr(elem, 'text'):
		to.append(elem.text)
	elif isinstance(elem, (Space, LineBreak, SoftBreak)):
		to.append(' ')
	elif isinstance(elem, Para):
		to.append('\n\n')

def text_content(elem, doc=None):
	if not elem:
		return ''
	result = []
	adder = partial(add_text_content, to=result)
	elem.walk(adder)
	return ''.join(result)

def get_string_metadata(doc, name, default=''):
	return text_content(doc.get_metadata(name, builtin=False), doc) or default

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
		doc.metadata['localization-' + name] = get_string_metadata(doc, 'localization-' + name)

def sanitize_styles(doc):
	styles = doc.get_metadata('styles')
	result = None
	if isinstance(styles, MetaList):
		result = MetaList()
		for index, stylemap in enumerate(styles):
			if isinstance(stylemap, MetaMap):
				name = stylemap.get('name', None)
				text = text_content(stylemap.get('css', None), doc)
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
		doc.metadata[name] = get_string_metadata(doc, name)
	chapter = -1
	try:
		chapter = int(get_string_metadata(doc, 'chapter'))
	except ValueError:
		pass
	if chapter >= 0:
		doc.metadata['chapter'] = str(chapter)
	elif hasattr(doc.metadata, 'chapter'):
		del doc.metadata.content.chapter
	type = doc.get_metadata('type')
	doc.metadata['noun'] = get_string_metadata(doc, 'noun', get_string_metadata(doc, 'localization-type-' + type, type.title()))
	doc.metadata['final'] = MetaBool(bool(get_string_metadata(doc, 'final')))
	sanitize_styles(doc)

def make_title(doc):
	title = ''
	data = get_string_metadata(doc, 'series')
	if data:
		title += data + u' \u2013 '
	data = get_string_metadata(doc, 'title')
	if data:
		title += data
	data = doc.get_metadata('type')
	if data != 'standalone':
		title += ': ' + get_string_metadata(doc, 'localization-type-' + data, { 'index': 'Contents', 'biblio': 'Bibliography'}.get(data, data.title()))
	chapter = int(doc.get_metadata('chapter', -1))
	if chapter >= 0:
		title += (' 0' if chapter < 10 else ' ') + str(chapter)
	return title

def metas(doc):
	result = []
	for name in ['author', 'publisher', 'description']:
		content = []
		data = doc.get_metadata(name, builtin=False)
		if isinstance(data, MetaList):
			for item in data:
				content.append(text_content(item, doc))
		else:
			content.append(text_content(data, doc))
		result.extend([
			RawBlock('<meta name="' + name + '" content="' + escape(x, entities={'"': '&quot;'}) + '"/>', format='html') for x in content if x
		])
	data = doc.get_metadata('keywords', builtin=False)
	content = []
	if isinstance(data, MetaList):
		for item in data:
			content.append(text_content(item, doc))
	else:
		content.append(text_content(data, doc))
	content = ','.join(escape(x, entities={'"': '&quot;'}) for x in content if x)
	if content:
		result.append(
			RawBlock('<meta name="keywords" content="' + content + '"/>', format='html')
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
		href = get_string_metadata(doc, name)
		if href:
			result.append(RawBlock('<link rel="' + rel + '" href="' + escape(href, entities={'"': '&quot;'}) + '" data-external="1"/>'))
	return result

def prepare(doc):
	pass

def action(elem, doc):
	if isinstance(elem, Header):
		if elem.level == 1 and doc.get_metadata('type') in ['chapter', 'appendix']:
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
	header_includes.walk(ignore)
	header_text = text_content(header_includes)
	if not ('<title>' in header_text):
		header_includes.content.append(RawBlock('<title>' + escape(make_title(doc)) + '</title>', format='html'))
	header_includes.content.extend(metas(doc))
	header_includes.content.extend(links(doc))

def main(doc=None):
	return run_filter(action, doc=doc, prepare=prepare, finalize=finalize)

if __name__ == '__main__':
	main()
