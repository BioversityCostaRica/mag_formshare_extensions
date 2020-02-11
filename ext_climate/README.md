Platform for the Management of Climatic Risks
==============

This plug-in extends the functionality of FormShare to interact with satellite data (NDVI and Chirps) and generate climate risk assessments at district level.

Not all forms link with climatic data. FormShare has been configured with a user called "climate" whos ODK forms interact with the satellite data. All forms uploaded by this user are checked to see if the basic sensibility indicators are present in the form. Then when the repository is created by FormShare it injects the processes to calculate the sensibility index and link the indicator data with the satellite data.  Through a graphical interface inside FormShare the user can generate hazard, sensibility and vulnerability maps at district level. 

Getting Started
---------------

- Activate the FormShare environment.
```
$ . ./path/to/FormShare/bin/activate
```

- Change directory into your newly created plugin.
```
$ cd ext_climate
```

- Build the plug-in
```
$ python setup.py develop
```

- Add the plug-in to the FormShare list of plugins by editing the following line in development.ini or production.ini
```
    #formshare.plugins = examplePlugin
    formshare.plugins = ext_climate
```

- Run FormShare again
