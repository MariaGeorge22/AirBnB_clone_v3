#!/usr/bin/python3

from models import storage
from models.engine.file_storage import FileStorage

all = storage.all()
file = FileStorage()
for entity in all:
    file.new(all[entity])
file.save()
