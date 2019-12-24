#!/usr/bin/env python3

"""
Pandoc HTML filters.
"""

from panflute import *
from helper import *
from xml.sax.saxutils import escape
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

def sanitize_styles(doc):
	styles = doc.get_metadata('styles')
	result = None
	if isinstance(styles, MetaList):
		result = MetaList()
		for index, stylemap in enumerate(styles):
			if isinstance(stylemap, MetaMap):
				name = stylemap.get('name', None)
				text = MetaString(content.text(stylemap.get('css', None), doc))
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
		if title:
			title += ': '
		title += metadata.text(doc, 'localization-type-' + data, {'index': 'Contents', 'biblio': 'Bibliography'}.get(data, data.title()))
	number = int(metadata.text(doc, 'number', -1))
	if number >= 0:
		title += (' 0' if number < 10 else ' ') + str(number)
	if data not in ['index', 'biblio']:
		match = re.match(r'[0-9][0-9]-(.*)', metadata.text(doc, 'filename'))
		if match:
			if title:
				title += u'\u00A0\u2013 '
			title += match.group(1).replace('_', ' ').title()
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
	for name, rel in [
		('self', 'canonical'),
		('homepage', 'home'),
		('index', 'contents directory index toc'),
		('first', 'first start'),
		('prev','prev'),
		('next', 'next'),
		('last', 'last'),
		('repository', 'code-repository')
	]:
		href = metadata.text(doc, name)
		if href:
			result.append(RawBlock('<link rel="' + rel + '" href="' + escape(href, entities={'"': '&quot;'}) + '" data-external="1"/>'))
	return result

def set_name(elem, doc):
	if not hasattr(doc, 'name') and isinstance(elem, Header) and elem.level == 1:
		doc.name = elem.content

def append_names(elem, doc):
	if isinstance(elem, Link) and elem.url[0] == '.':
		output = metadata.text(doc, 'outputfile')
		name = None
		if output:
			referenced = None
			match = re.match(r'(.*/?)HTML/[^/]+/(.*/|)[^/]+\.xhtml', output) # FILEPREFIX and any INDEX prefix
			try:
				with open(match.group(1) + 'Markdown/' + match.group(2) + '/' + elem.url[:-len('.xhtml#BookGen.main')] + '.md', encoding='utf-8') as f:
					referenced = convert_text(f.read(), standalone=True)
			except:
				pass
			if referenced:
				referenced.walk(set_name, doc=referenced)
				if hasattr(referenced, 'name'):
					name = referenced.name
				else:
					match = re.search(r'[0-9][0-9]-([^/]+).md$', output)
					if match:
						name = Plain(Str(match.group(1)))
			if name:
				if len(elem.content) > 1:
					elem.content.extend([
						Str(u'\u00A0\u2013 '),
						RawInline('<cite>', format='html')
					] + referenced.name.list + [
						RawInline('</cite>', format='html')
					])
				else:
					elem.content = referenced.name

def prepare(doc):
	pass

def action(elem, doc):
	if isinstance(elem, Header):
		if elem.level == 1 and metadata.text(doc, 'type') not in ['chapter', 'appendix']:
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
		if 'BookGen.toc' == elem.identifier:
			elem.walk(append_names)
			return elem.content.list
		elif 'plain' in elem.classes:
			if len(elem.content) == 1 and isinstance(elem.content[0], Para):
				return Plain(*elem.content[0].content)
	elif isinstance(elem, Span):
		if 'data-from-metadata' in elem.attributes:
			elem.content = metadata.inlines(doc, elem.attributes.get('data-from-metadata'))
		# Keep going…
		if len(elem.content) == 0 and 'at' in elem.classes:
			return []
		elif 'data-colour' in elem.attributes or 'data-color' in elem.attributes:
			elem.attributes = dict({'style': 'color: ' + elem.attributes.get('data-colour', elem.attributes.get('data-color'))}, **elem.attributes)

def finalize(doc):
	sanitize_template_metadata(doc)
	header_includes = MetaBlocks(*metadata.blocks(doc, 'header-includes'))
	header_includes.walk(ignore.do, doc)
	if not ('<title>' in content.text(header_includes, doc)):
		header_includes.content.append(RawBlock('<title>' + escape(make_title(doc)) + '</title>', format='html'))
	header_includes.content.extend(metas(doc))
	header_includes.content.extend(links(doc))
	doc.metadata['header-includes'] = header_includes
	if hasattr(doc, 'name'):
		del doc.name

def main(doc=None):
	return run_filter(action, doc=doc, prepare=prepare, finalize=finalize)

if __name__ == '__main__':
	main()
