# About the Project
This is an inventory app where exotic music instruments are stored, edited, deleted.

As a user that's not registered, you can only see the instruments and its details,
either by accessing the web page or by accessing the provided endpoints.

In order to add instruments to the inventory, edit or delete them, sign in with your Google Account.

You can only edit or delete instruments added by you.

It is a project for the [Full Stack Web Development
Nanodegree @Udacity](https://eu.udacity.com/course/full-stack-web-developer-nanodegree--nd004)

This project uses Flask and PostGreSQL. It runs on a Virtual Machine (Ubuntu) in combination with Vagrant. See instructions to get it running.

## Setting up your environment:

1. This project makes use of a linux-based virtual machine. To install it, go to Virtual Box's website: https://www.virtualbox.org/wiki/Downloads

2. We use Vagrant to manage our virtual machine and sync our local repo with VM's repo. Please install vagrant: https://www.vagrantup.com/downloads.html

3. Clone the current repo by running
`git clone git@github.com:dani-santos-code/music_inventory.git`

4. On your terminal, type in `cd music_inventory`.

5. Run `vagrant up` followed by `vagrant ssh`.

6. Run `cd /vagrant/catalog`.

7. You can skip to the next section ("Running the web app") and get the app running, but in case you're curious about what happens behind the scenes, keep reading below. ⬇️

**IMPORTANT**:
When you build your virtual machine, the Vagrantfile runs several package management (`pip`) commands that will install all required dependencies for you behind the scenes automatically, such as:
- authlib
- google-api-python-client
- google-auth
- flake8

The basic configuration of the Vagrantfile was provided by [Udacity](https://github.com/udacity/fullstack-nanodegree-vm)

*More packages were added to suit the requirements of this project.*

Note that `instruments.db`(containing SQL *INSERT* commands to populate the tables) has already been provided for you on this git repo, so there's no need to load dummy data yourself. 😎

*Careful*: ☠️☠️☠️ If you run DB files manually you might run into problems.
In case that happens, please delete the file `instruments.db` and run `python loadinstruments.py`

*Summarizing*: There is no need to install the dependencies or the dummy data yourself. 🔆

*Notice*:  In case you want to stop the machine from running on localhost, type in `sudo halt`.Then run, `vagrant halt` to shut down the VM.

## Running the webapp:

To get the app running, type in `python main.py` which will run the website at http://localhost:8000

*Make sure you're in the right directory (`/vagrant/catalog`)*

## Additional Information About the Project

### Folder Structure
```
.
├── LICENSE
├── README.md
├── Vagrantfile
└── catalog
    ├── database_setup.py
    ├── loadinstruments.py
    ├── main.py
    ├── static
    │   ├── css
    │   │   ├── bg-image.jpeg
    │   │   └── styles.css
    │   ├── favicon.ico
    │   └── images
    │       ├── africa.svg
    │       ├── asia.svg
    │       ├── europe.svg
    │       ├── logo.svg
    │       ├── noinst.svg
    │       ├── nopic.svg
    │       ├── north_america.svg
    │       ├── oceania.svg
    │       └── south_america.svg
    └── templates
        ├── africa.html
        ├── asia.html
        ├── base.html
        ├── dashboard.html
        ├── deleteinstrument.html
        ├── details.html
        ├── editinstrument.html
        ├── europe.html
        ├── main.html
        ├── newinstrument.html
        ├── north_america.html
        ├── oceania.html
        └── south_america.html
 ```

### Linting

To make sure PEP style is being followed, you can run `flake8`. If it returns nothing, it means all `.py` files have been correctly formatted.


### API Endpoints
There are only READ endpoints:

**Regions**:
- /regions/JSON  --> (Endpoint to see all regions)

**Instruments Per Region**:
- /regions/asia/JSON  --> Endpoint to see all Asian instruments
- /regions/africa/JSON --> Endpoint to see all African instruments
- /regions/europe/JSON --> Endpoint to see all European instruments
- /regions/north_america/JSON --> Endpoint to see all North American instruments
- /regions/south_america/JSON --> Endpoint to see all instruments from Asia
- /regions/oceania/JSON --> Endpoint to see all instruments from Oceania

**Instrument Details**
- /details/**id**/JSON --> Endpoint to see details of any given instrument, by its id
