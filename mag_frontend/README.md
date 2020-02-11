MAG Branding Extension
==============

This extension change the look and feel of FormShare with the logos and text of the Ministry of Agriculture.

Getting Started
---------------

- Activate the FormShare environment.
```
$ . ./path/to/FormShare/bin/activate
```

- Change directory into your newly created plugin.
```
$ cd mag_frontend
```

- Build the translation files and the plug-in
```
$ python setup.py compile_catalog
$ python setup.py develop
```

- Add the plug-in to the FormShare list of plug-ins by editing the following line in development.ini or production.ini
```
    #formshare.plugins = examplePlugin
    formshare.plugins = mag_frontend
```

- Run FormShare again
