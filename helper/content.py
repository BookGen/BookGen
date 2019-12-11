from panflute import *
from . import ignore
from functools import partial

def _add_text(elem, doc=None, to=None):
	if to == None:
		to = []
	if ignore.should(elem, doc):
		pass
	elif hasattr(elem, 'text'):
		to.append(elem.text)
	elif isinstance(elem, (Space, LineBreak, SoftBreak)):
		to.append(' ')
	elif isinstance(elem, Para):
		to.append('\n\n')

def text(elem, doc=None):
	mapper = partial(text, doc=doc)
	if not elem:
		return ''
	result = []
	adder = partial(_add_text, to=result)
	if isinstance(elem, Element):
		elem.walk(adder, doc=doc)
	elif isinstance(elem, list):
		result = map(mapper, elem)
	else:
		return str(elem)
	return ''.join(result)

def inlines(elem, doc=None):
	mapper = partial(inlines, doc=doc)
	if isinstance(elem, MetaBool):
		return [Str(u'\u2B55' if elem.boolean else u'\u274C')]
	elif isinstance(elem, MetaInlines):
		return elem.content.list[:]
	elif isinstance(elem, MetaList) or isinstance(elem, Block) and hasattr(elem, content):
		result = []
		for item in map(mapper, elem.content):
			result += [Str(', ')] + item
		return result[1:] # Drop unnecessary leading comma
	elif isinstance(elem, MetaMap):
		result = []
		for (key, item) in elem.content.items():
			result += [Str(', '), Str(key + ': ')] + mapper(item)
		return result[1:] # Drop unnecessary leading comma
	elif isinstance(elem, MetaString):
		return [Str(elem.text)]
	elif isinstance(elem, Inline):
		return [elem]
	elif isinstance(elem, list):
		return map(mapper, elem)
	else:
		result = text(elem, doc)
		if result:
			return [Str(result)]
		else:
			return []

def blocks(elem, doc=None):
	mapper = partial(blocks, doc=doc)
	if isinstance(elem, MetaBlocks):
		return elem.content.list[:]
	elif isinstance(elem, MetaList):
		result = []
		for item in map(mapper, elem.content):
			result.extend(item)
		return result
	elif isinstance(elem, MetaMap):
		result = []
		for key, value in elem.content.items():
			if isinstance(value, MetaList):
				result.append(DefinitionItem([Str(key)], map(lambda item: Definition(*item), map(mapper, value.content))))
			else:
				item = mapper(value)
				result.append(DefinitionItem([Str(key)], [Definition(*item)]))
		return [DefinitionList(*result)]
	elif isinstance(elem, Block):
		return [elem]
	elif isinstance(elem, list):
		return map(mapper, elem)
	else:
		result = inlines(elem, doc)
		if result:
			return [Plain(*result)]
		else:
			return []
