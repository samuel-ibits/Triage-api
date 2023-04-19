# Triage-api


This api helps rank patients in the hospital based on severity of condition and state of emmergency as opposed to the first come first serve system

model: 
exposed route:

# starting the api locally

# To create a virtual enviroment run:
python -m venv venv/

# activate the venv:
venv\Scripts\activate

# on windows if you have trouble activating env run:
Set-ExecutionPolicy Unrestricted -Scope Process
# or (dangerous)
Set-ExecutionPolicy Unrestricted -Force

# install requrements
pip install -r requirements.txt

# start app
py app.py
# or
python app.py
# or(development)
flask run