VIRTUALENV=virtualenv

.PHONY: .env

.env: requirements.txt
	rm -fr $@ && virtualenv $@ && pip install -r $^


	
