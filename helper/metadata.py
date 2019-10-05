from panflute import *
from . import content

def text(doc, name, default=''):
	return content.text(doc.get_metadata(name, builtin=False), doc) or default

def inlines(doc, name, default=''):
	return content.inlines(doc.get_metadata(name, builtin=False), doc) or ([Str(default)] if isinstance(default, str) else default)

def blocks(doc, name, default=None):
	return content.blocks(doc.get_metadata(name, builtin=False), doc) or ([Plain(Str(default))] if isinstance(default, str) else default)
