# About the Project
This is an inventory app where exotic music instruments are stored, edited, deleted. It is a project for the Full Stack Web Development Nanodegree @Udacity (https://eu.udacity.com/course/full-stack-web-developer-nanodegree--nd004)

This project uses Flask and PostGreSQL. It runs on a Virtual Machine (Ubuntu) in combination with Vagrant. See instructions to get it running.

## Setting up your environment:

1. This project makes use of a linux-based virtual machine. To install it, go to Virtual Box's website: https://www.virtualbox.org/wiki/Downloads

2. We use Vagrant to manage our virtual machine and sync our local repo with VM's repo. Please install vagrant: https://www.vagrantup.com/downloads.html

3. Clone the current repo by running
`git clone git@github.com:dani-santos-code/music_inventory.git`

4. Run `vagrant up` followed by `vagrant ssh`.

5. Run `cd /vagrant`.

*Notice*:  In case you want to stop the machine from running on localhost, type in `sudo halt`.Then run, `vagrant halt` to shut down the VM.

## Setting up the database and adding dummy data:

- To setup the database, run `python database_setup.py`

- To load dummy data, run `python loadinstruments.py`


## Running the webapp:

To get the app running, type in `python main.py`
