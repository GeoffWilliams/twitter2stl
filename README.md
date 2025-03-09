## Setup
```shell
python -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt 
```

## Troubleshooting

### AttributeError: 'FileFinder' object has no attribute 'find_module

Cause:

* https://github.com/JustAnotherArchivist/snscrape/issues/782
* https://github.com/bellingcat/auto-archiver/issues/209
```
snscrape/modules/__init__.py", line 13, in _import_modules
    module = importer.find_module(moduleName).load_module(moduleName)
             ^^^^^^^^^^^^^^^^^^^^
AttributeError: 'FileFinder' object has no attribute 'find_module'
```

Solution: Use python 3.11.x for now