Gastos Abertos
==============

API para dados de execução orçamentária da cidade de São Paulo.


## Installation (Debian like systems)

Install virtualenv and git:

    sudo apt-get install python-virtualenv git

Initiate a virtual environment you'll work with:

    virtualenv env
    . env/bin/activate

Clone this project repository:

    git clone https://github.com/okfn-brasil/gastos_abertos.git

Enter the project folder:

    cd gastos_abertos
    
Run this SQL:

    psql mydatabasename -c "CREATE EXTENSION postgis";

Install python's dependencies:

    python setup.py install

Prepare DB and other files:

    flask initdb

Start the server:

    flask run
