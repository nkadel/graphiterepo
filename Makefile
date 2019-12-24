#
# Makefile - build wrapper for carbon on CentPOS 7
#
#	git clone RHEL 7 SRPM building tools from
#	https://github.com/nkadel/[package] into designated
#	CARBONPKGS below
#
#	Set up local 

REPOBASE=file://$(PWD)
#REPOBASE=http://localhost

CARBONPKGS+=python-carbon-srpm
CARBONPKGS+=python-whisper-srpm

REPOS+=carbonrepo/el/7
REPOS+=carbonrepo/el/8

REPODIRS := $(patsubst %,%/x86_64/repodata,$(REPOS)) $(patsubst %,%/SRPMS/repodata,$(REPOS))

# No local dependencies at build time
CFGS+=carbonrepo-7-x86_64.cfg
CFGS+=carbonrepo-8-x86_64.cfg

# Link from /etc/mock
MOCKCFGS+=epel-7-x86_64.cfg
MOCKCFGS+=epel-8-x86_64.cfg

all:: $(CFGS) $(MOCKCFGS)
all:: $(REPODIRS)
all:: $(CARBONPKGS)
all:: install

.PHONY: build getsrc install clean
build getsrc install clean::
	@for name in $(CARBONPKGS); do \
	     (cd $$name; $(MAKE) $(MFLAGS) $@); \
	done  

# Dependencies
python-carbon-srpm::
python-whisper-srpm::

# Actually build in directories
.PHONY: $(CARBONPKGS)
$(CARBONPKGS)::
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

carbonrepo-7-x86_64.cfg: /etc/mock/epel-7-x86_64.cfg
	@echo Generating $@ from $?
	@cat $? > $@
	@sed -i 's/epel-7-x86_64/carbonrepo-7-x86_64/g' $@
	@echo >> $@
	@echo "config_opts['yum.conf'] += \"\"\"" >> $@
	@echo '[carbonrepo]' >> $@
	@echo 'name=carbonrepo' >> $@
	@echo 'enabled=1' >> $@
	@echo 'baseurl=file://$(PWD)/carbonrepo/el/7/x86_64/' >> $@
	@echo 'failovermethod=priority' >> $@
	@echo 'skip_if_unavailable=False' >> $@
	@echo 'metadata_expire=1' >> $@
	@echo 'gpgcheck=0' >> $@
	@echo '#cost=2000' >> $@
	@echo '"""' >> $@

carbonrepo-8-x86_64.cfg: /etc/mock/epel-8-x86_64.cfg
	@echo Generating $@ from $?
	@cat $? > $@
	@sed -i 's/epel-8-x86_64/carbonrepo-8-x86_64/g' $@
	@echo >> $@
	@echo "config_opts['yum.conf'] += \"\"\"" >> $@
	@echo '[carbonrepo]' >> $@
	@echo 'name=carbonrepo' >> $@
	@echo 'enabled=1' >> $@
	@echo 'baseurl=file://$(PWD)/carbonrepo/el/8/x86_64/' >> $@
	@echo 'failovermethod=priority' >> $@
	@echo 'skip_if_unavailable=False' >> $@
	@echo 'metadata_expire=1' >> $@
	@echo 'gpgcheck=0' >> $@
	@echo '#cost=2000' >> $@
	@echo '"""' >> $@

carbonrepo-f30-x86_64.cfg: /etc/mock/fedora-30-x86_64.cfg
	@echo Generating $@ from $?
	@cat $? > $@
	@sed -i 's/fedora-30-x86_64/carbonrepo-f30-x86_64/g' $@
	@echo >> $@
	@echo "config_opts['yum.conf'] += \"\"\"" >> $@
	@echo '[carbonrepo]' >> $@
	@echo 'name=carbonrepo' >> $@
	@echo 'enabled=1' >> $@
	@echo 'baseurl=file://$(PWD)/carbonrepo/fedora/30/x86_64/' >> $@
	@echo 'failovermethod=priority' >> $@
	@echo 'skip_if_unavailable=False' >> $@
	@echo 'metadata_expire=1' >> $@
	@echo 'gpgcheck=0' >> $@
	@echo '#cost=2000' >> $@
	@echo '"""' >> $@


$(MOCKCFGS)::
	ln -sf --no-dereference /etc/mock/$@ $@

repo: carbonrepo.repo
carbonrepo.repo:: Makefile carbonrepo.repo.in
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
	@for name in $(CARBONPKGS); do \
	    $(MAKE) -C $$name clean; \
	done

distclean: clean
	rm -rf $(REPOS)

maintainer-clean: distclean
	rm -rf $(CARBONPKGS)
