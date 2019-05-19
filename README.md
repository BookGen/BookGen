# BookGen

BookGen is a makefile which can be used to generate a wide variety of formats from a per­‑chapter Markdown source. It is designed to ease the technical aspects of publishing electronic documents so that authors can focus on simply writing.

In order to use BookGen, you will need to make or acquire `.css` and/or `.cls` styles, which will be used to format your work. Some basic styles to get you started can be found here : <https://gist.github.com/marrus-sh/77be7f563f1b7fa412113d5090190a07>. Basic LaTeX knowledge will help in debugging PDF generation and ensuring good output, but is ( hopefully ) not required.

BookGen uses Pandoc under­‑the­‑hood ; click to read about [Pandocʼs approach to markdown](https://pandoc.org/MANUAL.html#pandocs-markdown). In contrast with normal Pandoc, BookGen does *not* perform automatic quote‑ or dash‑substitutions ; it is expected that you write what you mean in your Markdown source.

BookGen runs on the command­‑line ; consequently, basic understanding of how to use a terminal emulator is advised.

## Installation

BookGen is designed for GNU Make 3.81, and will hopefully work with this and any later version. It will *not* work properly with earlier versions of GNU Make, or with other `make` programs.

You can test which version of `make` you have by running `make -v`. On my device, I get the following output :

	GNU Make 3.81
	Copyright (C) 2006  Free Software Foundation, Inc.
	This is free software; see the source for copying conditions.
	There is NO warranty; not even for MERCHANTABILITY or FITNESS FOR A
	PARTICULAR PURPOSE.

	This program built for i386-apple-darwin11.3.0

As you can see from the first line, I am running GNU Make 3.81.

If your version of make is out­‑of­‑date ( or nonexistent ), you can download a new one by following the directions here : <https://www.gnu.org/software/make/>

In addition to GNU Make, you will need to make sure you have the following installed on your computer :

+ **For general usage :**
	+ Haskell, including the following packages :
		+ `pandoc`
		+ `pandoc-citeproc` ( for bibliography handling only )
		+ See <https://pandoc.org/installing.html> for installation instructions regarding the above
	+ Python, including the following packages :
		+ `panflute` ( can be installed with `pip install panflute` ; see <http://scorreia.com/software/panflute/install.html> )
+ **For PDF generation :**
	+ TeX, LaTeX, XeTeX, etc…
		+ I use [TeXLive](http://www.tug.org/texlive/) ( or, more properly, [MacTeX](http://www.tug.org/mactex/) )
		+ `xelatex` is the recommended LaTeX command, and the default
		+ You will need at least the following LaTeX packages :
			+ `memoir`
			+ `url`
			+ `hyperref`
			+ `logreq`
			+ `ncctools`
			+ `soul`
			+ `ulem`
			+ `xcolor`
			+ `ifetex`
			+ `everypage`
			+ `background`
			+ `newunicodechar`
			+ `mfirstuc`
			+ `biblatex`, including `biber` ( for works with bibliographies )
				+ `biblatex-chicago` is used by default, but you can change this with a `BIBREQUIRE` override
			+ ( …and all of their prerequisites )
			+ You will likely only need to install these yourself if you purposefully installed a limited TeX distribution like BasicTeX
+ **For PNG generation :**
	+ Everything required for PDF generation ( PNGs are built from PDFs )
	+ GhostScript
		+ See <https://ghostscript.com/>
		+ For macOS, MacTeX offers their own GhostScript package here, if you didnʼt install it as part of MacTeX : <http://www.tug.org/mactex/morepackages.html>
	+ ImageMagick
		+ See <https://imagemagick.org/>
		+ For macOS, you may want to use [Homebrew](https://brew.sh/) ( `brew install imagemagick` )
	+ `pdftotext`
		+ A part of the Xpdf command line tools available here : <http://www.xpdfreader.com/>
		+ Comes preinstalled on many platforms
+ **For zip generation :**
	+ Zip
		+ See <http://infozip.sourceforge.net/Zip.html>
		+ Comes preinstalled on many platforms

To install, `git clone` this repository someplace you will be able to find it later, recursing submodules :

	git clone --recurse-submodules https://github.com/marrus-sh/BookGen.git

Or, if you already have this repository cloned, but forgot to set up the submodules :

	git submodule update --init

( Alternatively, if you donʼt want to use `git`, download [`DeluxeMakefile/Makefile.sty`](https://gist.githubusercontent.com/marrus-sh/ce267187fff0c658c0b4b06b997e5376/raw/235e4ed3d69241aa20ee2535a2c2f36c02f794d4/Makefile.sty) and [`StoryTime/index.html`](https://gist.githubusercontent.com/marrus-sh/c3bb0a37b3a39ddf5d02403eb1641d50/raw/1f20ccc3a0c99831dc3a6102c6b87a63ae1a1deb/index.html) and place them in their respective positions in this folder. )

## File Structure

Within your project, source files are principally located in two folders : `Markdown/`, which will contain the markdown texts of the project, and `Styles/`, which will contain `.css` and `.cls` files to use when rendering your source into various formats. In addition to these, you will need an `info.yml` file, specifying metadata about the project as a whole.

There are three types of source text you can create :

+ Chapter files, located at `Markdown/Chapters/$N.md`, where `$N` is a two­‑digit number identifying the chapter.

+ Appendix files, located at `Markdown/Chapters/A$N.md`, where `$N` is a two­‑digit number identifying the appendix.

+ Standalone files, as all other `.md` files in the `Markdown/` directory. Standalone files cannot be placed in any subdirectories, and are generally treated as frontmatter.

This beïng a Makefile, **you should not use colons, semicolons, or spaces in filenames**. You also should not create source files at `Markdown/Chapter/index.md` or `Markdown/text.md` without adjusting the `INDEX` or `FULLTEXT` overrides, respectively. Finally, style names which are the same as an existing argument defined by this makefile ( `html.css`, `latex.cls`, etc ) are not supported, as they would otherwise make compiling by style ambiguous.

### Markdown extensions

There are a few added features you can take advantage of in your Markdown for special formatting and display :

+ A Div with a class of `chapterprecis` can be used at the beginning of a chapter to insert a chapter precis:

		# My Chapter

		::: chapterprecis :::
		| A very good chapter,
		| Yes, very good indeed.
		:::::::::::::::::::::

+ A Div with a `role` of `note` can be used for notes:

		::: {role=note}
		This is a note.
		:::

+ A Span with a class of `lettrine` can be used for leading text:

		[This is the beginning]{.lettrine} of a section of text.

+ A Span with a `data-colour` ( or `data-color` ) attribute can be used to set the text colour. This can be either a 6­‑digit HTML hex value or an SVG colour name. In the latter case, the name must be properly capitalized:

		Some [red]{data-colour=#FF0000} and [blue]{data-colour=MidnightBlue} text.

+ An empty Span with a class of `at` can be used to generate a `\@` for sentence­‑spacing adjustment in LaTeX. This is only necessary if you are generating PDFs with a style which does not use `\frenchspacing`.

		Reading Rainbow, Mr[]{.at}. Rogers, etc.[]{.at} are all fond memories for me.

+ A raw HTML block of the form `<hr class="plain"/>` represents a plain ( unfancy ) break.

### YAML metadata

The metadata provided in `info.yml` can customize the compiled result. The available parameters are :

+ `title` : The title of the work ( plaintext only )
+ `series` : The series that the work belongs to ( plaintext only )
+ `author` : The author of the work ( plaintext only )
+ `publisher` : The publisher of the work ( plaintext only )
+ `description` : A description of the work ( plaintext only )
+ `year` : The copyright year( s ) of the work
+ `rights` : The ( short ) rights or license statement associated with the work
+ `details` : Detailed information regarding the licensing or publication of the work ; this can contain paragraph content
+ `draft` : A short string indicating the current draft of the work ; this will be set automatically for individual texts ( but not the work as a whole ) if you have `DRAFTS` enabled
+ `lang` : The language of the work ( for HTML )
+ `final` : Use this to declare that your work is finished and remove the **DRAFT** markings.
+ `header-includes` : Content to include in the header of every document ; you should only use this to insert raw HTML headers ( LaTeX header information should be specified in your style file )
+ `include-before` : Content to include at the beginning of every text
+ `include-after` : Content to include at the ending of every text

You can also provide this metadata on a per­‑text basis for additional customization.

### Bibliography

You can use citations and/or a bibliography with Pandoc by specifying it via the `BIBLIOGRAPHY` override. This must be a BibLaTeX bibliography file with the extension `.bib`. By default, the Chicago Manual of Style notes‑bibliography style is used for citations.

All entries which appear in your bibliography will be printed, regardless of whether you actually cite them in one of your texts.

The [Wikibooks page on LaTeX bibliography management](https://en.wikibooks.org/wiki/LaTeX/Bibliography_Management#BibTeX) may be useful in learning the overall structure of a `.bib` file.

## Usage

	make [ ⟨ make-options ⟩ ] [ ⟨ args ⟩ ] [ ⟨ options ⟩ ] [ ⟨ overrides ⟩ ]

If you are calling `make` from your work directory, you will want to specify the `-f` option with the path to `GNUmakefile`. Conversely, if you are calling `make` from this directory, you will need the `-C` option to specify the work directory in which to operate.

There are two other `⟨ make-options ⟩` which are likely to be of use to you : `-B` will consider all targets out­‑of­‑date ( and consequently remake everything ), and `-s` will run `make` in “ quiet mode ” to avoid cluttering up your console.

### Args and output

The `⟨ args ⟩` you provide will determine which files to make. If blank, this is the same as `all`.

If you only want a specific file to be generated, you can specify its file name as an argument ( for example, `HTML/$style/$file.xhtml` ). Of course, there are a number of more generalized arguments you can use to generate multiple files at once.

#### Markdown

Arguments : `md`, `markdown`

Unless you have the `DRAFTS` override set, this only creates zip files of your markdown source, unless the `NOARCHIVE` option is toggled, in which case this does nothing. If the `DRAFTS` override is set, this will create all of the symlinks in the `Markdown/` directory.

#### LaTeX

Arguments : `latex`, `tex`

LaTeX files are generated with a `.tex` extension in the `LaTeX/` directory. These are *not* complete files ( they do not have a `\begin{document}` ), but rather are intended to be `\include`d into other documents. This process happens automatically when you use this makefile to generate a PDF.

#### HTML

Arguments : `htm`, `html`, `html5`, `xht`, `xhtml`, `xhtml5`, `xml`

HTML files will be placed in the `HTML/$style/` directory, where `$style` is the name of the stylesheet used to generate the file. By default, this will run for every `.css` stylesheet defined in the `Styles/` directory ; you can limit it to particular stylesheets using the `STYLE` override.

If the `ALLSTYLES` option is provided, then all of the styles will be available in every HTML document, as alternative stylesheets specified by using the `title` attribute on the `<style>` element. Note that currently only Firefox actually provides a mechanism for toggling between alternative style sheets.

Each generated file is a standalone (X)HTML file ( embedded CSS ) with an `.xhtml` extension. A table of contents file will also be generated ; see the `INDEX` override for the name of this file.

#### PDF

Arguments : `pdf`

PDF files are generated with a `.pdf` extension in the `PDF/$style/` directory, where `$style` is the name of the stylesheet used to generate the file. By default, this will run for every `.cls` stylesheet defined in the `Styles/` directory ; you can limit it to particular stylesheets using the `STYLE` override.

Styles need to be `memoir` extensions as some of the Markdown to LaTeX conversions take advantage of `memoir` features. In particular, horizontal rules will be transformed into a `\pfbreak`. Blockquotes use the `quoting` environment, which will be loaded automatically ( but which you may want to configure in your style ).

#### PNG

Arguments : `png`

PNG files are generated, one per page, with a `.png` extension in a folder in the `PNG/$style/` directory, where `$style` is the name of the stylesheet used to generate the file. By default, this will run for every `.cls` stylesheet defined in the `Styles/` directory ; you can limit it to particular stylesheets using the `STYLE` override.

An `index.html` file will be placed in the folder containing the PNGs, which you can open in any browser with JavaScript enabled to browse them. BookGen will attempt to generate proper alt­‑text for this file from the PDF for each PNG, using GhostScript.

#### Zip

Arguments : `dist`, `zip`

Using the `dist` or `zip` arguments will generate *every* zip. However, zip files will also be created when you use another generic argument ( like `html` ) unless the `NOARCHIVE` option is set. Zip files are generated in the `Zip/` directory, matching the directory structure of the files they contain.

#### Other arguments

There are a few special arguments which donʼt just generate a single type of file :

+ `all` or `everything` : This is the same as specifying `md xhtml tex pdf png`.

+ `clean` : Removes the build directory and temporary build files.

+ `unclean` : Removes the `LaTeX/`, `HTML/`, `PDF/`, `PNG/`, and `Zip/` directories. Also removes the `Markdown/` directory if the `DRAFTS` override is set. These are the directories which contain files generated by this makefile.

+ `clobber`, `distclean`, or `gone` : This is the same as specifying `clean unclean`.

Finally, you can use a specific style name ( the name of a file in `Styles/` ) to compile all of the formats which make use of that style.

### Options

`⟨ options ⟩` are a special kind of makefile override which are either true ( if set to any nonempty value ) or false ( the default ). The available options to you are as follows :

+ `ALLSTYLES` : Embed every stylesheet in every HTML document. This will still generate separate HTML files for each provided style, but the only difference between these files will be which stylesheet is the default.

+ `NOARCHIVE` : Do not generate zips ( unless specifically requested, eg with the `zip` argument ).

+ `VECTORIZE` : Vectorize the final PDFs instead of leaving them with embedded fonts. Specifying this option may help with fonts which do not play nicely with printers. However, this will disable text selection on computers, so you should not use this option when compiling for digital distribution.

+ `VERBOSE` : Shows verbose output ; especially useful for debugging LaTeX.

### Overrides

There are a number of `⟨ overrides ⟩` which can be used to further configure the `make`. These are:

+ `APPENDIXPREFIX` : The prefix for appendixes. Defaults to `$(CHAPTERPREFIX)A`. Must not contain colons or spaces.

+ `BIBLIOGRAPHY` : The name of the workʼs bibliography file, which must have a suffix of `.bib`. Requires `biber` to process.

+ `BIBREQUIRE` : The arguments to `\RequirePackage`/`\usepackage` for the proper bibliography package to use in LaTeX. Defaults to `[notes,annotation]{biblatex-chicago}`.

+ `BUILDDIR` : The directory in which to place LaTeX build files. Defaults to `Build`.

+ `CHAPTERPREFIX` : The prefix for non­‑appendix chapters. Defaults to `Chapters/`. Must not contain colons or spaces.

+ `DRAFTS` : If nonempty, automatically symlinks in the `Markdown/` folder to the last file in the equivalent folder in the specified directory. For example, `DRAFTS=Drafts` will symlink `Markdown/Chapters/01` to `Drafts/Chapters/01/$N.md`. If you use this, you should not place files in the `Markdown/` directory, as it will be deleted on `gone`. Defaults to empty.

	As a standard makefile limitation, symlinks will not update if they are more recent than the files they “ should ” be pointing to ( especially relevant in the case that they once pointed to a newer file which was deleted ). Simply delete any outdated symlinks to force their regeneration.

+ `FULLTEXT` : The name to use for the fulltext PDF/PNG file( s ). Defaults to `text`. Naturally, it will cause problems if you have a source file with the same name as this file.

+ `INDEX` : The name to use for outputted index files. Defaults to `$(CHAPTERPREFIX)index`. Naturally, it will cause problems if you have a source file with the same name as this file.

+ `LATEX` : The LaTeX compiler to use. Defaults to `xelatex`.

+ `FILEPREFIX` : A prefix to prepend to the `Markdown`, `LaTeX`, `HTML`, `PDF`, `PNG`, and `Zip` folders on input and output. Empty by default.

+ `STYLE` : The names of the styles to compile. If empty, every style available for a given type will be used. Empty by default.

+ `YAML` : The name of the YAML metadata file. Defaults to `info.yml`.

### Recursion and includes

You may want to `include` this makefile from another one, for example in your work directory, to avoid having to directly use the `-C` or `-f` options. In this case, you will need to override the `srcdir` variable to properly point to this directory from the other makefile. For example, you might configure a makefile as follows :

	override srcdir := BookGen
	include $(srcdir)/GNUmakefile

You can naturally include any number of other overrides in this file as well. Here is one sample configuration :

	# Default make.
	default: html pdf;

	# The path to the BookGen source.
	override srcdir := BookGen

	# Overrides.
	override APPENDIXPREFIX := Appendices/
	override BIBLIOGRAPHY := bibliography.bib
	override DRAFTS := Drafts/
	override FULLTEXT := my-amazing-story
	override INDEX := contents

	# BookGen rule imports.
	include $(srcdir)/GNUmakefile

If you save such a file as `Makefile` ( or `GNUmakefile` ) in your work directory, then you need only call `make` to compile your project.

If you have other build tasks which you need to complete, a simple `include` may not work for you. In this case, a match­‑anything pattern rule can be used to achieve the same effect. You donʼt need to override `srcdir` with a match­‑anything pattern rule because it will properly be inferred through calling `make` the second time :

	Makefile: ;
	%: force
		@$(MAKE) -ef BookGen/GNUmakefile $@
	force: ;

Setting the `-e` flag allows you to export options and overrides from the parent makefile. Be sure to always write `GNUmakefile` with correct capitalization.

## Prior art

This Makefile began as an extension of my work on [Deluxe Makefile for LaTeX](https://gist.github.com/marrus-sh/ce267187fff0c658c0b4b06b997e5376), to allow it to be used in conjunction with Pandoc to generate documents of a variety of filetypes. After hacking together solutions for a number of projects, I decided to write a new, comprehensive makefile which was much more robust.

## License

The source code of this makefile is licensed under the GNU General Public License, version 3 or later. For more information, see [COPYING](./COPYING).

This makefile has two submodule dependencies, [Deluxe Makefile for LaTeX](https://gist.github.com/marrus-sh/ce267187fff0c658c0b4b06b997e5376) ( for `Makefile.sty` only ) and [StoryTime](https://gist.github.com/marrus-sh/c3bb0a37b3a39ddf5d02403eb1641d50) ( for `index.html` ). See each submodule for appropriate licensing information.
