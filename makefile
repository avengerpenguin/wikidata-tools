all.nt: latest-all.json.bz2
	pv $< | bzip2 | python wd2rdf.py | grep . >$@


latest-all.json.bz2:
	curl -o "$@" ""
