#
# Makefile - build wrapper for graphite on CentPOS 7
#
#	git clone RHEL 7 SRPM building tools from
#	https://github.com/nkadel/[package] into designated
#	GRAPHITEPKGS below
#
#	Set up local 

REPOBASE=file://$(PWD)
#REPOBASE=http://localhost

# Placeholder for non-python2-labeled packages
EPELPKGS+=python2-pygments-srpm
EPELPKGS+=python2-setuptools_scm-srpm
# EPEL 7 only
EPELPKGS+=python-mistune-srpm

EPELPKGS+=python-PyHamcrest-srpm
EPELPKGS+=python-appdirs-srpm
EPELPKGS+=python-cachetools-srpm
EPELPKGS+=python-protobuf-srpm
EPELPKGS+=python-pyserial-srpm
EPELPKGS+=python-whisper-srpm
EPELPKGS+=python-zope-interface-srpm

# Depends on python-mistune-srpm
GRAPHITEPKGS+=python-m2r-srpm
GRAPHITEPKGS+=python-Automat-srpm

# Extremely demanding dependency
GRAPHITEPKGS+=python-twisted-srpm

GRAPHITEPKGS+=python-carbon-srpm

#GRAPHITEPKGS+=python-twisted-core-srpm
GRAPHITEPKGS+=python-twisted-srpm

GRAPHITEPKGS+=python-graphite-web-srpm

REPOS+=graphiterepo/el/7
REPOS+=graphiterepo/el/8
REPOS+=graphiterepo/fedora/30
REPOS+=graphiterepo/fedora/31

REPODIRS := $(patsubst %,%/x86_64/repodata,$(REPOS)) $(patsubst %,%/SRPMS/repodata,$(REPOS))

# No local dependencies at build time
CFGS+=graphiterepo-7-x86_64.cfg
CFGS+=graphiterepo-8-x86_64.cfg
CFGS+=graphiterepo-f31-x86_64.cfg

# Link from /etc/mock
MOCKCFGS+=epel-7-x86_64.cfg
MOCKCFGS+=epel-8-x86_64.cfg
MOCKCFGS+=fedora-31-x86_64.cfg

all:: install

install:: $(REPODIRS)
install:: $(EPELPKGS)
install:: $(GRAPHITEPKGS)
install:: $(CFGS) $(MOCKCFGS)

.PHONY: build getsrc install clean
build getsrc install clean::
	@for name in $(GRAPHITEPKGS); do \
	     (cd $$name; $(MAKE) $(MFLAGS) $@); \
	done  

# Dependencies
python-m2r-srpm:: python2-pygments-srpm
python-m2r-srpm:: python-mistune-srpm

python-Automat-srpm:: python-m2r-srpm
python-Automat-srpm:: python-setuptools-scm-srpm

python-twisted-srpm:: python-Automat-srpm

.PHONY: epel
epel:: $(EPELPKGS)

# Actually build in directories
.PHONY: $(EPELPKGS) $(GRAPHITEPKGS)
$(EPELPKGS) $(GRAPHITEPKGS)::
	(cd $@; $(MAKE) $(MLAGS) install)

repos: $(REPOS) $(REPODIRS)
.PHONY: $(REPOS)
$(REPOS):
	install -d -m 755 $@

.PHONY: $(REPODIRS)
$(REPODIRS): $(REPOS)
	@install -d -m 755 `dirname $@`
	/usr/bin/createrepo -q `dirname $@`

.PHONY: cfg cfgs
cfg cfgs:: $(CFGS) $(MOCKCFGS)

graphiterepo-7-x86_64.cfg: /etc/mock/epel-7-x86_64.cfg
	@echo Generating $@ from $?
	@cat $? > $@
	@sed -i 's/epel-7-x86_64/graphiterepo-7-x86_64/g' $@
	@echo >> $@
	@echo "config_opts['yum.conf'] += \"\"\"" >> $@
	@echo '[graphiterepo]' >> $@
	@echo 'name=graphiterepo' >> $@
	@echo 'enabled=1' >> $@
	@echo 'baseurl=file://$(PWD)/graphiterepo/el/7/x86_64/' >> $@
	@echo 'failovermethod=priority' >> $@
	@echo 'skip_if_unavailable=False' >> $@
	@echo 'metadata_expire=1' >> $@
	@echo 'gpgcheck=0' >> $@
	@echo '#cost=2000' >> $@
	@echo '"""' >> $@

graphiterepo-8-x86_64.cfg: /etc/mock/epel-8-x86_64.cfg
	@echo Generating $@ from $?
	@cat $? > $@
	@sed -i 's/epel-8-x86_64/graphiterepo-8-x86_64/g' $@
	@echo >> $@
	@echo "config_opts['yum.conf'] += \"\"\"" >> $@
	@echo '[graphiterepo]' >> $@
	@echo 'name=graphiterepo' >> $@
	@echo 'enabled=1' >> $@
	@echo 'baseurl=file://$(PWD)/graphiterepo/el/8/x86_64/' >> $@
	@echo 'failovermethod=priority' >> $@
	@echo 'skip_if_unavailable=False' >> $@
	@echo 'metadata_expire=1' >> $@
	@echo 'gpgcheck=0' >> $@
	@echo '#cost=2000' >> $@
	@echo '"""' >> $@

graphiterepo-f31-x86_64.cfg: /etc/mock/fedora-31-x86_64.cfg
	@echo Generating $@ from $?
	@cat $? > $@
	@sed -i 's/fedora-31-x86_64/graphiterepo-f31-x86_64/g' $@
	@echo >> $@
	@echo "config_opts['yum.conf'] += \"\"\"" >> $@
	@echo '[graphiterepo]' >> $@
	@echo 'name=graphiterepo' >> $@
	@echo 'enabled=1' >> $@
	@echo 'baseurl=file://$(PWD)/graphiterepo/fedora/31/x86_64/' >> $@
	@echo 'failovermethod=priority' >> $@
	@echo 'skip_if_unavailable=False' >> $@
	@echo 'metadata_expire=1' >> $@
	@echo 'gpgcheck=0' >> $@
	@echo '#cost=2000' >> $@
	@echo '"""' >> $@


$(MOCKCFGS)::
	ln -sf --no-dereference /etc/mock/$@ $@

repo: graphiterepo.repo
graphiterepo.repo:: Makefile graphiterepo.repo.in
	if [ -s /etc/fedora-release ]; then \
		cat $@.in | \
			sed "s|@REPOBASEDIR@/|$(PWD)/|g" | \
			sed "s|/@RELEASEDIR@/|/fedora/|g" > $@; \
	elif [ -s /etc/redhat-release ]; then \
		cat $@.in | \
			sed "s|@REPOBASEDIR@/|$(PWD)/|g" | \
			sed "s|/@RELEASEDIR@/|/el/|g" > $@; \
	else \
		echo Error: unknown release, check /etc/*-release; \
		exit 1; \
	fi

clean::
	find . -name \*~ -exec rm -f {} \;
	rm -f *.cfg
	rm -f *.out
	@for name in $(EPELPKGS) $(GRAPHITEPKGS); do \
	    $(MAKE) -C $$name clean; \
	done

distclean: clean
	rm -rf $(REPOS)

maintainer-clean: distclean
	rm -rf $(GRAPHITEPKGS)
