# RaspiBallFollower

## Description

This little piece of software allows you track your favourite ball wherever it is and wherever it goes anywhere, anytime.
We know from Toys Story that our toy can move when we don't stare at them. 
To fullfill your curiosity we give you oportunity to observe your moving ball when you don't look directly at it. 

## Features

* 360 degrees tracking thanks to stepper motor or servo.
* Display which shows you where your ball is trying to hide.

## Hardware Requirements

* Raspberry Pi 3B or better
* Stepper motor with ULN2003 driver
* Few wires
* Breadboard

## Software Requirements

* Raspbian Wheezy
* Python 3.5.x or higher
* opencv-python-contrib
* pigpio

## Installation

To run this script you need to install opencv-python and pigpio libraries:
> pip3 install opencv-contrib-python pigpio

or

> pip3 install -r requirements.txt

## Usage

To start tracking your ball you only need to run Tracking.py
> python Tracking.py

That's all. From now your balls will never hide from you :)
