VIRTUALENV=virtualenv

.PHONY: clear test

.env: requirements.txt
	rm -fr $@ && $(VIRTUALENV) $@ && \
	. $@/bin/activate && \
	pip install -r $^ && \
	deactivate

.testenv: requirements.txt requirements_test.txt
	rm -fr $@ && $(VIRTUALENV) $@ && \
	. $@/bin/activate && \
	pip install -r $(word 1,$^) && pip install -r $(word 2,$^) && \
	deactivate

test: .testenv
	. $^/bin/activate && py.test && deactivate

clear:
	find . -name "*.pyc" -delete
	rm -fr .env .testenv
	
