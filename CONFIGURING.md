# Configuring Book Metadata

The final output of books can be configured through the use of metadata properties in one of two locations:

1. A YAML file located in your source directory, titled `info.yml` (or whatever name you provide with the `YAML` override).

2. [Metadata blocks](https://pandoc.org/MANUAL.html#metadata-blocks) in your Markdown source.

Pandoc uses a *left-based union* to combine metadata blocks.
This means that the first block which specifies a given property will be used.
The `info.yml` file will be appended to the *end* of your document, so chapter properties will always take precedence.

Property values may be any YAML value, although numbers will be interpreted as strings.
Strings will be processed as Markdown.

Raw blocks in properties will generally be ignored if they do not match the current output type (`latex` or `html`).
You can use this to provide format-specific configurations.

## Basic properties

The following basic properties are available:

+ `author`: The author of the work
+ `description`: A description or brief summary of the work
+ `dir`: The writing direction (for HTML)
+ `download`: A URL from which the work can be downloaded
+ `draft`: A short string identifying the current draft of the work; this will be automatically set on a per-chapter basis if the `DRAFTS` override is set
+ `final`: If not false(y), this is a final draft for publication; otherwise, this is a working draft
+ `homepage`: The homepage for the work
+ `keywords`: A list of keywords for the work
+ `lang`: An IETF language tag providing the language of the work (for HTML)
+ `noun`: A noun ("chapter", "appendix", etc) for referring to the current division; this will be automatically set if left unspecified
+ `profile`: The homepage of the work's author
+ `publisher`: The publisher of the work
+ `repository`: The source repository for the work
+ `rights`: A short rights statement regarding the work
+ `series`: The title of the series the work belongs to
+ `title`: The title of the work
+ `year`: The copyright year of the work

These properties are set by BookGen itself and should generally not be modified:

+ `chapter`: The current chapter number
+ `biblio`: A relative link to the bibliography
+ `bibliography`: Bibliography data; used by `pandoc-citeproc`
+ `citation-style`: Path to a citation style for `pandoc-citeproc`; you *can* change this if you want to use a different citation style than the `chicago-note-bibliography-16th-edition` provided by BookGen
+ `first`: A relative link to the first chapter
+ `index`: A relative link to the index
+ `last`: A relative link to the last chapter
+ `next`: A relative link to the next chapter
+ `prev`: A relative link to the previous chapter
+ `self`: A relative link to the current document
+ `style`: The name of the currently-selected style
+ `styles`: An array of maps with `style` and `css` properties, giving all available styles
+ `type`: One of `appendix`, `chapter`, `standalone`

## Localization properties

By default, BookGen templates and filters insert English text.
You can change the text inserted (either to a different language, or just to change the phrasing) using properties prefixed with `localization-`.
The default localization is effectively as follows:

```yaml
localization-appendices: Appendices
localization-chapters: Chapters
localization-draft: Draft
localization-index: Contents
localization-top: Top
localization-type-appendix: Appendix
localization-type-biblio: Bibliography
localization-type-chapter: Chapter
localization-type-index: Contents
localization-type-standalone: Preface
```

## Includes

The `header-includes` property can be used to specify additional markup to include in the document header.

`include-before` and `include-after` can be used to specify additional markup to include before and after the main document body.

## Filters

**Only use this if you know what you are doing!**

The `filter` property allows for custom per-chapter Pandoc filters to be applied prior to the style and BookGen filters.

The value of this property must be either:

1. A path to a Python(3) file, which will be `import`ed and run.

2. A map with three properties, `prepare`, `action`, `finalize`, whose contents must be either:

    1. Raw blocks matching the output format type (all other raw blocks will be ignored), or

    2. Ordinary, untyped code blocks.

    The contents of these blocks must be Python code, and provide the effective bodies for the `prepare`, `action`, and `finalize` arguments to [Panflute](http://scorreia.com/software/panflute/)'s `run_filter`.
The [Panflute API](http://scorreia.com/software/panflute/code.html) will be available with the current `Doc` available on the `doc` local variable.
In the case of the `action` script, `elem` will hold the current `Element`, and you can return a value by assigning it to `result`.

## Style-specific properies

Styles may define their own properties in addition to the ones above.
