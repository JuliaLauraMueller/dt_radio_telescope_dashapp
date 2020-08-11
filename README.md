# Designing a «Digital Twin» of a Radio Telescope - Dash Application for Visualizing

## Application Instructions
This instruction explains how to start the Dash application for visualizing the radio images created by SATRO.

### 1. Make sure you have Python installed
To execute the the initial script you need to have python installed on your operating system.

https://www.python.org/downloads/

Python version 3.7 is sufficient for execution.

### 2. Make sure you have important packages installed
Make sure that you have certain packages installed for executing this application.
To easy manage your packages you can navigate with Anaconda, a user interface for managing packages and environments.

#### To install it:
https://docs.anaconda.com/anaconda/install/

#### To getting started with:
https://docs.anaconda.com/anaconda/navigator/getting-started/

![Anaconda Navigator](documentation/dash_app_readme.png)

The following packages are required for this application:
- matplotlib
- plotly
- plotly-express
- astropy
- pandas
- numpy
- dash
- dash-core-components
- dash-bootstrap-components
- dash-html-components

### 3. Execute script and open dash application
Firstly start your terminal at this folder:

dt_radio_telescope_dashapp/AppDash

To simply start the application you have to enter
```
python app.py
```

Afterwards it will show you the localhost adress where the application is running.
