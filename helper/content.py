from panflute import *
from . import ignore
from functools import partial

def _add_text(elem, doc=None, to=[]):
	if ignore.should(elem, doc):
		pass
	elif hasattr(elem, 'text'):
		to.append(elem.text)
	elif isinstance(elem, (Space, LineBreak, SoftBreak)):
		to.append(' ')
	elif isinstance(elem, Para):
		to.append('\n\n')

def text(elem, doc=None):
	if not elem:
		return ''
	result = []
	adder = partial(_add_text, to=result)
	elem.walk(adder)
	return ''.join(result)

def inlines(elem, doc=None):
	if isinstance(elem, MetaBool):
		return [Str(u'\u2B55' if elem.boolean else u'\u274C')]
	elif isinstance(elem, MetaInlines):
		return elem.content.list
	elif isinstance(elem, MetaList):
		result = []
		for item in map(inlines, elem.content):
			result += [Str(', ')] + item
		return result[1:] # Drop unnecessary leading comma
	elif isinstance(elem, MetaMap):
		result = []
		for (key, item) in elem.content.items():
			result += [Str(', '), Str(key + ': ')] + inlines(item)
		return result[1:] # Drop unnecessary leading comma
	elif isinstance(elem, MetaString):
		return [Str(elem.text)]
	else:
		result = text(elem, doc)
		if result:
			return [Str(result)]
		else:
			return []

def blocks(elem, doc=None):
	if isinstance(elem, MetaBlocks):
		return elem.content.list
	elif isinstance(elem, MetaList):
		result = []
		for item in map(blocks, elem.content):
			result.extend(item)
		return result
	elif isinstance(elem, MetaMap):
		result = []
		for key, value in elem.content.dict:
			if isinstance(value, MetaList):
				result.append(DefinitionItem([Str(key)], map(lambda item: Definition(*item), map(blocks, value.content))))
			else:
				item = blocks(value)
				result.append(DefinitionItem([Str(key)], [Definition(*item)]))
		return [DefinitionList(*result)]
	else:
		result = inlines(elem, doc)
		if result:
			return [Plain(*result)]
		else:
			return []
