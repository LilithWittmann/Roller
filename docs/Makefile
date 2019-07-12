SPHINXTARGETS = html dirhtml singlehtml pickle json htmlhelp qthelp devhelp epub latex latexpdf latexpdfja text man texinfo info gettext changes xml pseudoxml linkcheck doctest coverage

.PHONY: help clean apidoc $(SPHINXTARGETS)

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = scooters
SOURCEDIR     = .
BUILDDIR      = _build

define clean-rsts =
	find . -type f -name "*.rst" ! -name index.rst -delete
endef

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O);\
	echo "  [34;01mapidoc  [39;49;00m    to auto-generate the apidoc from the application code";\
	echo "  [34;01mclean  [39;49;00m     to clean the directory"

clean:
	$(clean-rsts)
	rm -rf _build/*

apidoc:
	$(clean-rsts)
	sphinx-apidoc -o . .. ../**/migrations/*

$(SPHINXTARGETS): apidoc
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
