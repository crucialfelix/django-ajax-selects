

install:
	$(shell ./install.sh $(DJANGO) 1>&2)
	@echo
	@echo NOW DO:
	@echo source AJAXSELECTS/bin/active
	@echo ./manage.py runserver
	@echo browse: http://localhost:8080/admin/

clean:
	@echo Deleting virtualenv
	rm -rf AJAXSELECTS

cleandb:
	@echo Removing sqllite db
	rm ajax_selects_example

help:
	@echo make install
	@echo or:
	@echo make clean install DJANGO=1.11


.PHONY: install clean cleandb help
