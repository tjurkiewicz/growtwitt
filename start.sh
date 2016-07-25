#!/bin/bash

cd src && python manage.py migrate && python server.py

