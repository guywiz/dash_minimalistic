# object oriented dash_minimalistic app
Minimalistic examples of a dash application.

This repository stores an object oriented version of the minimalistic `dash` application complying with the MVC paradigm.

##  dash, OO and MVC

The code is orgabized into three maian facets, namely the controller who accesses both a data manager and view manager to run teh application.

The controller is the one having its hands on the app callbacks, the main objects dealing with events.

Events then trigger actions on the view side, requiring the view manager to compute graphical objects that are fed to the app components (under the controller's callbacks).

In order to complete its tasks, the view manager needs to wuery the data manager to feed the view components (titles, features names, number of topics, etc.).
