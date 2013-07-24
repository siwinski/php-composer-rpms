PWD              = $(shell pwd)
RPMBUILD_OPTIONS = --define "_topdir $(PWD)/rpmbuild"
SPECTOOL_OPTIONS = --get-files --directory '$(PWD)/rpmbuild/SOURCES'

RPM_DIST         = $(shell rpm --eval '%{dist}')
REPO_RELEASE     = $(shell \
						if [ ".fc18" == "$(RPM_DIST)" ]; then \
							echo "fedora-18"; \
						elif [ ".el6" == "$(RPM_DIST)" ]; then \
							echo "epel-6"; \
						fi)
REPO_PATH        = fedorapeople.org:/srv/repos/siwinski/php-composer/$(REPO_RELEASE)

PKGS             := $(shell find ./pkgs -name "*.spec")

# TARGET: help          Print this information
.PHONY: help
help:
	# Usage:
	#   make <target>
	#
	# Targets:
	@egrep "^# TARGET:" [Mm]akefile | sed 's/^# TARGET:\s*/#   /'

# TARGET: setup         Setup rpmbuild directories
.PHONY: setup
setup:
	@mkdir -p -m 755 ./rpmbuild/{BUILD,BUILDROOT,RPMS,SOURCES,SRPMS}
	@mkdir -p -m 755 ./rpmbuild/RPMS/noarch

# TARGET: core          Make core RPMs
.PHONY: core
core: CORE_SOURCE=$(shell spectool --list-files core/php-composer.spec | grep '^Source0:' | sed 's/Source0:\s*//')
core: CORE_FILENAME=$(shell basename "$(CORE_SOURCE)")
core: CORE_COMMIT=$(shell echo "$(CORE_SOURCE)" | sed 's#$(CORE_FILENAME)##' | xargs basename)
core: setup
	@[ -e rpmbuild/SOURCES/$(CORE_FILENAME) ] && [ -e rpmbuild/SOURCES/composer.phar ] \
		|| spectool $(SPECTOOL_OPTIONS) core/php-composer.spec
	@[ ! -e rpmbuild/SOURCES/$(CORE_FILENAME) ] && [ -e rpmbuild/SOURCES/$(CORE_COMMIT) ] \
		&& mv rpmbuild/SOURCES/$(CORE_COMMIT) rpmbuild/SOURCES/$(CORE_FILENAME) \
		|| :
	@[ -L core/$(CORE_FILENAME) ] || ln -s ../rpmbuild/SOURCES/$(CORE_FILENAME) core/$(CORE_FILENAME)
	@[ -L core/composer.phar ]  || ln -s ../rpmbuild/SOURCES/composer.phar core/composer.phar
	rpmbuild $(RPMBUILD_OPTIONS) --define '_sourcedir $(PWD)/core' -ba core/php-composer.spec

# TARGET: pkgs          Make all pkgs RPMs
.PHONY: pkgs $(PKGS)
pkgs: setup $(PKGS)

$(PKGS): PKG_SOURCE=$(shell spectool --list-files '$@' | grep '^Source0:' | sed 's/Source0:\s*//')
$(PKGS): PKG_FILENAME=$(shell basename "$(PKG_SOURCE)")
$(PKGS): PKG_COMMIT=$(shell echo "$(PKG_SOURCE)" | sed 's#$(PKG_FILENAME)##' | xargs basename)
$(PKGS): setup
	[ -e rpmbuild/SOURCES/$(PKG_SOURCE) ] || spectool $(SPECTOOL_OPTIONS) $@
	@[ ! -e rpmbuild/SOURCES/$(PKG_FILENAME) ] && [ -e rpmbuild/SOURCES/$(PKG_COMMIT) ] \
                && mv rpmbuild/SOURCES/$(PKG_COMMIT) rpmbuild/SOURCES/$(PKG_FILENAME)
	rpmbuild $(RPMBUILD_OPTIONS) -ba $@

# TARGET: all           Make all core and pkgs RPMs
.PHONY: all
all: core pkgs

# TARGET: rpmlint       Run rpmlint on all spec files
.PHONY: rpmlint
rpmlint:
	@echo ""
	@for SPEC in */*.spec; do \
		echo "-------------------- $$SPEC --------------------"; \
		rpmlint ./$$SPEC; \
		echo ""; \
	done

# TARGET: repos-pull    Pull repos from fedorapeople.org
.PHONY: repos-pull
repos-pull: setup
	@[ "" != "$(REPO_RELEASE)" ] || \
		(echo "ERROR: Invalid distribution" 1>&2; exit 1)
	@echo "-------------------- Pull SRPMS repo --------------------"
	rsync -rlptv $(REPO_PATH)/SRPMS/ rpmbuild/SRPMS/
	@echo "-------------------- Pull RPMS repo --------------------"
	rsync -rlptv $(REPO_PATH)/noarch/ rpmbuild/RPMS/noarch/

# TARGET: repos-create  Create RPM and SRPM repos
.PHONY: repos
repos-create: repos-pull
	@echo "-------------------- Create SRPMS repo --------------------"
	createrepo --update -v rpmbuild/SRPMS/
	@echo ""
	@echo "-------------------- Create RPMS repo --------------------"
	createrepo --update -v rpmbuild/RPMS/noarch/

# TARGET: repos-push    Push repos to fedorapeople.org
.PHONY: repos-push
repos-push: repos-create
	@[ "" != "$(REPO_RELEASE)" ] || \
		(echo "ERROR: Invalid distribution" 1>&2; exit 1)
	@echo "-------------------- Push SRPMS repo --------------------"
	rsync -avz rpmbuild/SRPMS/ $(REPO_PATH)/SRPMS/
	@echo "-------------------- Push RPMS repo --------------------"
	rsync -avz rpmbuild/RPMS/noarch/ $(REPO_PATH)/noarch/

# TARGET: clean         Delete any temporary or generated files
.PHONY: clean
clean:
	rm -rf ./rpmbuild
	find . -name '*~' -delete
	find . -name '*.gz' -delete
	find . -name '*.tgz' -delete
	find . -name '*.rpm' -delete
	find . -name '*.zip' -delete
	find . -type l -delete
