#!/usr/bin/env python

"""
Pandoc HTML filters.
"""

from panflute import *

def action(elem, doc):
	pass

def main(doc=None):
	return run_filter(action, doc=doc)

if __name__ == "__main__":
	main()
