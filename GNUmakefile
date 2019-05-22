# BOOKGEN #
# <https://github.com/marrus-sh/BookGen/>
#
# I canʼt imagine why you would want to TOUCH this code, but just in case :
#
# This program is free software : you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or ( at your option ) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# See README.md for usage.

SHELL = /bin/sh
srcdir := $(patsubst %/GNUmakefile,%,$(lastword $(MAKEFILE_LIST)))
override octothorpe := \#

#  DEFAULT VALUES FOR OVERRIDES  #

CHAPTERPREFIX := Chapters/

APPENDIXPREFIX := $(CHAPTERPREFIX)A
BIBLIOGRAPHY :=
BIBREQUIRE := [notes,annotation]{biblatex-chicago}
BUILDDIR := Build
DRAFTS :=
FULLTEXT := text
INDEX := index
LATEX := xelatex
FILEPREFIX :=
STYLE :=
YAML := info.yml

# BASIC RULES #

all everything: md xhtml tex pdf png;
htm html html5 xht xhtml5 xml: xhtml;
latex: tex;
markdown: md;
dist: zip;
clean: ; rm -rf $(BUILDDIR)
unclean: ; rm -rf $(if $(DRAFTS),$(FILEPREFIX)Markdown,) $(FILEPREFIX)LaTeX $(FILEPREFIX)HTML $(FILEPREFIX)PDF $(FILEPREFIX)PNG $(FILEPREFIX)Zip
clobber distclean gone: clean unclean;
zip: ;
.PHONY: all everything htm html html5 xht xhtml5 xml latex markdown dist clean unclean clobber distclean gone zip;
.SUFFIXES: ;
.SECONDEXPANSION: ;

# SOURCE FILES AND NAMES #

chapternames = $(patsubst $(FILEPREFIX)Markdown/$(CHAPTERPREFIX)%.md,%,$(1))
appendixnames = $(patsubst $(FILEPREFIX)Markdown/$(APPENDIXPREFIX)%.md,%,$(1))
standalonenames = $(patsubst $(FILEPREFIX)Markdown/%.md,%,$(1))

srcs = $(patsubst %,$(FILEPREFIX)Markdown/%.md,$(1))

ifdef DRAFTS
chaptersrcs := $(sort $(patsubst $(DRAFTS)/%/,$(FILEPREFIX)Markdown/%.md,$(dir $(wildcard $(DRAFTS)/$(CHAPTERPREFIX)[0-9][0-9]/*.md))))
appendixsrcs := $(sort $(patsubst $(DRAFTS)/%/,$(FILEPREFIX)Markdown/%.md,$(dir $(wildcard $(DRAFTS)/$(APPENDIXPREFIX)[0-9][0-9]/*.md))))
standalonesrcs := $(sort $(filter-out $(chaptersrcs) $(appendixsrcs),$(patsubst $(DRAFTS)/%/,$(FILEPREFIX)Markdown/%.md,$(dir $(wildcard $(DRAFTS)/*/*.md)))))
else
chaptersrcs := $(sort $(wildcard $(FILEPREFIX)Markdown/$(CHAPTERPREFIX)[0-9][0-9].md))
appendixsrcs := $(sort $(wildcard $(FILEPREFIX)Markdown/$(APPENDIXPREFIX)[0-9][0-9].md))
standalonesrcs := $(sort $(filter-out $(chaptersrcs) $(appendixsrcs),$(wildcard $(FILEPREFIX)Markdown/*.md)))
endif
allsrcs := $(standalonesrcs) $(chaptersrcs) $(appendixsrcs)

allstandalonenames := $(call standalonenames,$(standalonesrcs))
allchapternames := $(call chapternames,$(chaptersrcs))
allappendixnames := $(call appendixnames,$(appendixsrcs))
allnames := $(allstandalonenames) $(addprefix $(CHAPTERPREFIX),$(allchapternames)) $(addprefix $(APPENDIXPREFIX),$(allappendixnames))

types = $(foreach src,$(1),$(if $(findstring $(src),$(appendixsrcs)),appendix,$(if $(findstring $(src),$(chaptersrcs)),chapter,standalone)))
names = $(call $(call types,$(1))names,$(1))

# FOLDERS AND LINKS #

makefolders = remaining="$(or $(1),$@)"; while [[ "$$remaining" == */* ]]; do [[ -d "$${remaining%%/*}" ]] || mkdir "$${remaining%%/*}"; cd "$${remaining%%/*}"; remaining="$${remaining$(octothorpe)*/}"; done

returntoroot = $(foreach dir,$(strip $(subst /, ,$(dir /$(1)))),../)

define link
$(makefolders)
ln -fs "$(realpath $(or $(1),$<))" $(or $(2),$@)
endef

# ZIP CREATION #

define makezip
$(call makefolders,$@)
rm -f $@
cd $(FILEPREFIX)$(firstword $(subst /, ,$(patsubst $(FILEPREFIX)%,%,$(firstword $(or $(1),$^))))); zip -MM -9DX$(if $(VERBOSE),v,q)r ../$(patsubst $(FILEPREFIX)%,%,$(basename $@)) $(patsubst $(FILEPREFIX)$(firstword $(subst /, ,$(patsubst $(FILEPREFIX)%,%,$(firstword $(or $(1),$^)))))/%,%,$(or $(1),$^))
@echo "Zip generated at $@"
endef

# STYLES AND FILES #

stylesrcs = $(sort $(wildcard Styles/*.$(1)))
ifdef STYLE
stylenames = $(filter $(STYLE),$(patsubst Styles/%.$(1),%,$(call stylesrcs,$(1))))
else # If no styles are specified, use all of them.
stylenames = $(patsubst Styles/%.$(1),%,$(call stylesrcs,$(1)))
endif

styles = $(foreach file,$(1),$(word 2,$(subst /, ,$(patsubst $(FILEPREFIX)%,%,$(1)))))

# For the remaining rules in this section:
# $(1): The folder name
# $(2): The style name OR file extension
# $(3): The resulting file extension
# $(4): File names

files = $(if $(findstring /,$(3)),$(patsubst %,$(FILEPREFIX)$(1)/$(2)/%/$(notdir $(3)),$(4)),$(patsubst %,$(FILEPREFIX)$(1)/$(2)/%.$(3),$(4)))
chapters = $(call files,$(1),$(2),$(3),$(addprefix $(CHAPTERPREFIX),$(allchapternames)))
appendixes = $(call files,$(1),$(2),$(3),$(addprefix $(APPENDIXPREFIX),$(allappendixnames)))
standalones = $(call files,$(1),$(2),$(3),$(allstandalonenames))
everything = $(call files,$(1),$(2),$(3),$(4) $(allnames))

filenames = $(if $(findstring /,$(3)),$(patsubst $(FILEPREFIX)$(1)/$(2)/%/$(notdir $(3)),%,$(4)),$(patsubst $(FILEPREFIX)$(1)/$(2)/%.$(3),%,$(4)))

allfiles = $(foreach style,$(call stylenames,$(2)),$(call files,$(1),$(style),$(3),$(4)))
allchapters = $(call allfiles,$(1),$(2),$(3),$(addprefix $(CHAPTERPREFIX),$(allchapternames)))
allappendixes = $(call allfiles,$(1),$(2),$(3),$(addprefix $(APPENDIXPREFIX),$(allappendixnames)))
allstandalones = $(call allfiles,$(1),$(2),$(3),$(allstandalonenames))
alleverything = $(call allfiles,$(1),$(2),$(3),$(4) $(allnames))

stylezip = $(FILEPREFIX)Zip/$(1)/Styles/$(2).zip

allfilezips = $(patsubst %,$(FILEPREFIX)Zip/$(1)/%.zip,$(4) $(allnames))
allstylezips = $(foreach style,$(call stylenames,$(2)),$(call stylezip,$(1),$(style)))

# UNSTYLED FILES #
# For use with plain LaTeX/text.

# $(1): The folder name
# $(2): The resulting file extension
# $(3): File names

unstyledfiles = $(if $(findstring /,$(3)),$(patsubst %,$(FILEPREFIX)$(1)/%/$(notdir $(2)),$(3)),$(patsubst %,$(FILEPREFIX)$(1)/%.$(2),$(3)))
unstyledchapters = $(call unstyledfiles,$(1),$(2),$(addprefix $(CHAPTERPREFIX),$(allchapternames)))
unstyledappendixes = $(call unstyledfiles,$(1),$(2),$(addprefix $(APPENDIXPREFIX),$(allappendixnames)))
unstyledstandalones = $(call unstyledfiles,$(1),$(2),$(allstandalonenames))
unstyledeverything = $(call unstyledfiles,$(1),$(2),$(allnames) $(3))

unstylednames = $(if $(findstring /,$(3)),$(patsubst $(FILEPREFIX)$(1)/%/$(notdir $(2)),%,$(3)),$(patsubst $(FILEPREFIX)$(1)/%.$(2),%,$(3)))

unstyledzip = $(FILEPREFIX)Zip/$(1).zip

# COMMON TARGETS #
# For use with $(eval).

define targettype
$(if $(findstring /,$(3)),$(patsubst %/,%,$(dir $(3))),$(3)): $$(if $$(NOARCHIVE),$$(call alleverything,$(1),$(2),$(3),$(4)),$$(call allstylezips,$(1),$(2)) $$(call allfilezips,$(1),$(2),$(3),$(4)));
.PHONY: $$(3)
endef

# This rule uses a double­‑colon since it is possible that multiple different file types use the same style name.
define targetstyles
$$(call stylenames,$(2)):: $$(if $$(NOARCHIVE),$$$$(call everything,$(1),$$$$@,$(3),$(4)),$$$$(call stylezip,$(1),$$$$@));
.PHONY: $$(call stylenames,$(2))
endef

define targetstylezips
$$(call allstylezips,$(1),$(2)): $(FILEPREFIX)Zip/$(1)/Styles/%.zip: $$$$(call everything,$(1),$$$$*,$(3),$(4)); $(if $(findstring /,$(3)),$$(call makezip,$$(call everything,$(1),$$*,/*,$(4))),$$(makezip))
zip: $$(call allstylezips,$(1),$(2))
endef

define targetfilezips
$$(call allfilezips,$(1),$(2),$(3),$(4)): $(FILEPREFIX)Zip/$(1)/%.zip: $$$$(call allfiles,$(1),$(2),$(3),$$$$*); $(if $(findstring /,$(3)),$$(call makezip,$$(call allfiles,$(1),$(2),/*,$$*)),$$(makezip))
zip: $$(call allfilezips,$(1),$(2),$(3),$(4))
endef

define targets
$$(eval $$(call targettype,$(1),$(2),$(3),$(4)))
$$(eval $$(call targetstyles,$(1),$(2),$(3),$(4)))
$$(eval $$(call targetstylezips,$(1),$(2),$(3),$(4)))
$$(eval $$(call targetfilezips,$(1),$(2),$(3),$(4)))
endef

# COMMON UNSTYLED TARGETS #
# For use with $(eval).

define unstyledtargettype
$(if $(findstring /,$(2)),$(patsubst %/,%,$(dir $(2))),$(2)): $$(if $$(NOARCHIVE),$$(call unstyledeverything,$(1),$(2),$(3)),$$(call unstyledzip,$(1))) ;
.PHONY: $$(2)
endef

define unstyledtargetzip
$$(call unstyledzip,$(1)): $$(call unstyledeverything,$(1),$(2),$(3)); $(if $(findstring /,$(2)),$$(call makezip,$$(call unstyledeverything,$(1),/*,$(3))),$$(makezip))
zip: $$(call unstyledzip,$(1))
endef

define unstyledtargets
$$(eval $$(call unstyledtargettype,$(1),$(2),$(3)))
$$(eval $$(call unstyledtargetzip,$(1),$(2),$(3)))
endef

# YAML #

# We do not want to set the chapter for standalone documents.
chapteryaml = $(if $(findstring $(call types,$<),chapter appendix),echo "chapter: $(call names,$<)";,)

fileyaml = echo "name: $(call names,$<)"; $(chapteryaml) $(if $(DRAFTS),echo "draft: $(basename $(notdir $(wildcard $(DRAFTS)/$(call standalonenames,$<)/*.md)))";,) echo "type: $(call types,$<)"

# Empty YAML if no file exists.
$(YAML):
	touch $(YAML)

# Markdown #

$(eval $(call unstyledtargets,Markdown,md))

ifdef DRAFTS
# This rule is just for symlink creation in the case that a `DRAFTS` override has been set.
$(allsrcs): $(FILEPREFIX)Markdown/%.md: $$(lastword $$(sort $$(wildcard $(DRAFTS)/$$*/*.md))); $(link)
endif

# LaTeX #

$(eval $(call unstyledtargets,LaTeX,tex,$(INDEX)))

$(call unstyledeverything,LaTeX,tex): $(FILEPREFIX)LaTeX/%.tex: $$(call srcs,$$*) $(YAML) $(srcdir)/pandoc-latex.py $(srcdir)/template.tex
	$(makefolders)
	(cat $<; echo; echo; echo "---"; cat $(YAML); $(fileyaml); echo "...") | pandoc -f markdown-smart -t latex-smart --standalone --template "$(srcdir)/template.tex" --filter "$(srcdir)/pandoc-latex.py" -o $@ --top-level-division=chapter $(if $(BIBLIOGRAPHY),--biblatex,)
	@echo "LaTeX file for $< generated at $@"

$(FILEPREFIX)LaTeX/$(INDEX).tex: $$(call unstyledeverything,LaTeX,tex) $(YAML) $(srcdir)/pandoc-latex.py
	$(makefolders)
	(echo "---"; cat $(YAML); echo "name: $(INDEX)"; echo "type: index"; echo "...") | pandoc -f markdown-smart -t latex-smart --standalone --template "$(srcdir)/template.tex" --filter "$(srcdir)/pandoc-latex.py" -o $@ --top-level-division=chapter $(if $(BIBLIOGRAPHY),--biblatex,)
	(echo "\\\\frontmatter"; $(foreach standalone,$(allstandalonenames),echo "\\\\include{$(standalone)}";) echo "\\\\cleardoublepage\\\\tableofcontents"; echo; echo "\\\\clearpage\\\\null\\\\thispagestyle{cleared}\\\\cleartooddpage[\null\thispagestyle{cleared}]\\\\mainmatter"; echo; $(foreach chapter,$(allchapternames),echo "\\\\include{$(CHAPTERPREFIX)$(chapter)}";) echo; $(if $(allappendixnames),echo "\\\\clearpage\\\\null\\\\thispagestyle{cleared}\\\\cleartooddpage[\null\thispagestyle{cleared}]\\\\appendix\\\\appendixpage"; $(foreach appendix,$(allappendixnames),echo "\\\\include{$(APPENDIXPREFIX)$(appendix)}";) echo;,) echo "\\\\clearpage$(if $(BIBLIOGRAPHY),\\\\null\\\\thispagestyle{cleared}\\\\cleartooddpage[\null\thispagestyle{cleared}]\\\\backmatter\\\\printbibliography,)") >> $@
	@echo "LaTeX index generated at $@"

# HTML #

$(eval $(call targets,HTML,css,xhtml,$(INDEX) $(basename $(BIBLIOGRAPHY))))

$(call alleverything,HTML,css,xhtml): $$(call srcs,$$(call filenames,HTML,$$(call styles,$$@),xhtml,$$@)) $(YAML) $(srcdir)/pandoc-html.py $(srcdir)/template.xhtml Styles/$$(call styles,$$@).css
	$(makefolders)
	(cat $<; echo; echo; echo "---"; echo "suppress-bibliography: true"; $(if $(BIBLIOGRAPHY),echo "bibliography: $(addsuffix .bib,$(basename $(BIBLIOGRAPHY)))"; echo "citation-style: '$(realpath $(srcdir)/chicago-note-bibliography-16th-edition.csl)'";,) echo "styles:"; echo "- name: $(call styles,$@)"; echo "  css: |"; echo '    ```{=html}'; cat Styles/$(call styles,$@).css | sed 's/^/    /'; echo '    ```'; $(if $(ALLSTYLES),$(foreach style,$(filter-out $(call styles,$@),$(stylenames)),echo "- name: $(style)"; echo "  css: |"; echo '    ```{=html}'; cat Styles/$(style).css | sed 's/^/    /'; echo '    ```';)) cat $(YAML); $(fileyaml); $(if $(findstring $(call types,$<),appendix),echo "appendix: true";,) echo "...") | pandoc -f markdown-smart -t html5-smart --standalone --template "$(srcdir)/template.xhtml" --filter "$(srcdir)/pandoc-html.py" $(if $(BIBLIOGRAPHY),--filter pandoc-citeproc,) -o $@ --self-contained --section-divs --mathml
	@echo "$(call styles,$@) HTML file for $< generated at $@"

$(call allfiles,HTML,css,xhtml,$(INDEX)): $(FILEPREFIX)HTML/%/$(INDEX).xhtml: $(YAML) $(srcdir)/template.xhtml Styles/%.css
	$(makefolders)
	(echo '```{=html}'; echo '<ol>'; $(foreach standalone,$(allstandalonenames),echo '  <li><a href="$(call returntoroot,$(INDEX).xhtml)$(standalone).xhtml">$(standalone)</a></li>';) echo '  <li><a href="$(call returntoroot,$(INDEX).xhtml)$(INDEX).xhtml">Contents</a></li>'; $(if $(allchapternames),echo '<li><span>Chapters</span><ol>'; $(foreach chapter,$(allchapternames),echo '  <li><a href="$(call returntoroot,$(INDEX).xhtml)$(subst ",&quot;,$(CHAPTERPREFIX))$(chapter).xhtml">Chapter $(chapter)</a></li>';,) echo '</ol></li>';,) $(if $(allappendixnames),echo '<li><span>Appendices</span><ol>'; $(foreach appendix,$(allappendixnames), echo '  <li><a href="$(call returntoroot,$(INDEX).xhtml)$(subst ",&quot;,$(APPENDIXPREFIX))$(appendix).xhtml">Appendix $(appendix)</a></li>';) echo '</ol></li>';,) $(if $(BIBLIOGRAPHY),echo '<li><a href="$(call returntoroot,$(INDEX).xhtml)$(basename $(BIBLIOGRAPHY)).xhtml">Bibliography</a></li>';,) echo '</ol>'; echo '```'; echo; echo "---"; echo "styles:"; echo "- name: $(call styles,$@)"; echo "  css: |"; echo '    ```{=html}'; cat Styles/$*.css | sed 's/^/    /'; echo '    ```'; $(if $(ALLSTYLES),$(foreach style,$(filter-out $*,$(stylenames)),echo "- name: $(style)"; echo "  css: |"; echo '    ```{=html}'; cat Styles/$*.css | sed 's/^/    /'; echo '    ```';)) cat $(YAML); echo "...") | pandoc -f markdown-smart -t html5-smart --standalone --template "$(srcdir)/template-index.xhtml" --filter "$(srcdir)/pandoc-html.py" $(if $(BIBLIOGRAPHY),--filter pandoc-citeproc,) -o $@ --self-contained
	@echo "$* HTML index generated at $@"

$(call allfiles,HTML,css,xhtml,$(basename $(BIBLIOGRAPHY))): $(FILEPREFIX)HTML/%/$(basename $(BIBLIOGRAPHY)).xhtml: $(BIBLIOGRAPHY) Styles/%.css
	$(makefolders)
	(echo "---"; echo "bibliography: $(addsuffix .bib,$(basename $(BIBLIOGRAPHY)))"; echo "citation-style: '$(realpath $(srcdir)/chicago-note-bibliography-16th-edition.csl)'"; echo "styles:"; echo "- name: $(call styles,$@)"; echo "  css: |"; echo '    ```{=html}'; cat Styles/$(call styles,$@).css | sed 's/^/    /'; echo '    ```'; $(if $(ALLSTYLES),$(foreach style,$(filter-out $(call styles,$@),$(stylenames)),echo "- name: $(style)"; echo "  css: |"; echo '    ```{=html}'; cat Styles/$(style).css | sed 's/^/    /'; echo '    ```';)) cat $(YAML); echo "name: bibliography"; echo "type: bibliography"; echo "nocite: '@*'"; echo "..."; echo "$(octothorpe) Bibliography") | pandoc -f markdown-smart -t html5-smart --standalone --template "$(srcdir)/template.xhtml" --filter "$(srcdir)/pandoc-html.py" --filter pandoc-citeproc -o $@ --self-contained --section-divs --mathml

# PDF BUILDFILES #

buildtext = cd $(BUILDDIR)/$(call styles,$@) && $(LATEX) --jobname=$(call filenames,PDF,$(call styles,$@),pdf,$@) $(if $(VERBOSE),,--interaction=batchmode --halt-on-error) --file-line-error "\documentclass{style}\nofiles\usepackage{bookgen}$(if $(BIBLIOGRAPHY),\usepackage$(BIBREQUIRE)\addbibresource{bibliography.bib}\nocite{*},)\begin{document}$(if $(findstring $(call types,$(call srcs,$(call filenames,PDF,$(call styles,$@),pdf,$@))),chapter appendix),\mainmatter ,\frontmatter )$(if $(findstring $(call types,$(call srcs,$(call filenames,PDF,$(call styles,$@),pdf,$@))),appendix),\appendix )\makeatletter\@nameuse{cp@$(call filenames,PDF,$(call styles,$@),pdf,$@)@pre}\makeatother\input{$(call filenames,PDF,$(call styles,$@),pdf,$@)}\end{document}"

buildfulltext = cd $(BUILDDIR)/$* && $(LATEX) --jobname=$(FULLTEXT) $(if $(VERBOSE),,--interaction=batchmode --halt-on-error) --file-line-error "\documentclass{style}\usepackage{Makefile}\usepackage{bookgen}$(if $(BIBLIOGRAPHY),\usepackage$(BIBREQUIRE)\addbibresource{bibliography.bib}\nocite{*},)\input{GO.xxx}\input{$(INDEX)}\afterfulltext\end{document}"

$(patsubst $(FILEPREFIX)%,%,$(call allfiles,$(BUILDDIR),cls,sty,Makefile)): $(srcdir)/DeluxeMakefile/Makefile.sty; $(link)
$(patsubst $(FILEPREFIX)%,%,$(call allfiles,$(BUILDDIR),cls,sty,bookgen)): $(srcdir)/bookgen.sty; $(link)
$(patsubst $(FILEPREFIX)%,%,$(call allfiles,$(BUILDDIR),cls,cls,style)): $(BUILDDIR)/%/style.cls: Styles/%.cls; $(link)
$(patsubst $(FILEPREFIX)%,%,$(call allfiles,$(BUILDDIR),cls,bib,bibliography)): $(addsuffix .bib,$(basename $(BIBLIOGRAPHY))); $(link)
$(patsubst $(FILEPREFIX)%,%,$(call alleverything,$(BUILDDIR),cls,tex,$(INDEX))): $$(call unstyledfiles,LaTeX,tex,$$(call filenames,$(BUILDDIR),$$(call styles,$(FILEPREFIX)$$@),tex,$(FILEPREFIX)$$@)); $(link)

$(patsubst $(FILEPREFIX)%,%,$(call allfiles,$(BUILDDIR),cls,xxx,GO)): $(BUILDDIR)/%/GO.xxx: $(YAML) $(srcdir)/template.xxx
	$(makefolders)
	(echo "---"; cat $(YAML); echo "style: $*"; echo "...") | pandoc -f markdown -t latex --standalone --template "$(srcdir)/template.xxx" -o $@

$(patsubst $(FILEPREFIX)%,%,$(call allfiles,$(BUILDDIR),cls,aux,$(FULLTEXT))): $(BUILDDIR)/%/$(FULLTEXT).aux: $(patsubst $(FILEPREFIX)%,%,$(call alleverything,$(BUILDDIR),cls,tex,$(INDEX))) $(BUILDDIR)/%/Makefile.sty $(BUILDDIR)/%/bookgen.sty $(BUILDDIR)/%/GO.xxx $(BUILDDIR)/%/style.cls
	$(makefolders)
	$(buildfulltext)

$(patsubst $(FILEPREFIX)%,%,$(call allfiles,$(BUILDDIR),cls,bbl,$(FULLTEXT))): $(BUILDDIR)/%/$(FULLTEXT).bbl: $(BUILDDIR)/%/bibliography.bib | $(BUILDDIR)/%/$(FULLTEXT).aux
	cd $(BUILDDIR)/$* && biber $(if $(VERBOSE),,--onlylog) $(FULLTEXT)

# PDF #

$(eval $(call targets,PDF,cls,pdf,$(FULLTEXT)))

$(call alleverything,PDF,cls,pdf): $(FILEPREFIX)PDF/$$(call styles,$$@)/$(FULLTEXT).pdf
	$(makefolders)
	$(buildtext)
	$(if $(VECTORIZE),gs -dNoOutputFonts -sDEVICE=pdfwrite $(if $(VERBOSE),,-dQUIET) -o $@ $(BUILDDIR)/$(call styles,$@)/$(call filenames,PDF,$(call styles,$@),pdf,$@).pdf,mv -f $(BUILDDIR)/$(call styles,$@)/$(call filenames,PDF,$(call styles,$@),pdf,$@).pdf $@)
	@echo "$(call styles,$@) PDF for $(call srcs,$(call filenames,PDF,$(call styles,$@),pdf,$@)) generated at $@"

$(call allfiles,PDF,cls,pdf,$(FULLTEXT)): $(FILEPREFIX)PDF/%/$(FULLTEXT).pdf: $(BUILDDIR)/%/$(FULLTEXT).aux $(if $(BIBLIOGRAPHY),$(BUILDDIR)/%/$(FULLTEXT).bbl,)
	$(makefolders)
	$(buildfulltext)
	$(if $(VECTORIZE),gs -dNoOutputFonts -sDEVICE=pdfwrite $(if $(VERBOSE),,-dQUIET) -o $@ $(BUILDDIR)/$*/$(FULLTEXT).pdf,mv -f $(BUILDDIR)/$*/$(FULLTEXT).pdf $@)
	@echo "$* fulltext PDF generated at $@"

# PNGs #

$(eval $(call targets,PNG,cls,png/index.html,$(FULLTEXT)))

$(call alleverything,PNG,cls,png/index.html,$(FULLTEXT)): $(FILEPREFIX)PNG/%/index.html: $(FILEPREFIX)PDF/%.pdf $(srcdir)/StoryTime/index.html
	$(makefolders)
	cp "$(srcdir)/StoryTime/index.html" $@
	magick -density 144 $< -quality 100 -colorspace RGB -alpha remove $(dir $@)Page_%d.png; ((( m=0 )); for page in $(dir $@)/*.png; do echo; echo Page_$$m.png | tr '\n' ' '; (( m++ )); pdftotext -f $$m -l $$m -enc UTF-8 -eol unix -nopgbrk -raw $< - | awk '{gsub(/-\n/, ""); print}' | tr '\n' ' ' | tr -s ' '; done; echo) >> $@
	@echo $(if $(findstring $(FILEPREFIX)PNG/$(call styles,$@)/$(FULLTEXT)/index.html,$@),"$(call styles,$@) fulltext PNGs generated at $(dir $@)","$(call styles,$@) PNGs for $(call srcs,$(call filenames,PNG,$(call styles,$@),/index.html,$@)) generated at $(dir $@)")
