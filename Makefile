CSV_FILES = \
  data/co2_org-short-cycle_c.csv \
  data/co2_excl_short-cycle_org_c.csv \
  data/ch4.csv \
  data/n2o.csv

all: venv $(CSV_FILES)

data/%.csv: scripts/%.py
	@echo $@
	@./venv/bin/python $<

venv: scripts/requirements.txt
	[ -d ./venv ] || python3 -m venv venv
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -Ur scripts/requirements.txt
	touch venv

clean:
	rm -rf data/*.csv

clean-venv:
	rm -rf venv

.PHONY: clean
