# Love-Hate-and-Prague
Map visualisation where people feel well and where not.

## Purpose
This application primarly serves for analysis of happiness of people in specific location. This prototype application is foccused on area of Prague.

## Features
Main features of the application are:
 * twitter messages extraction
 * sentiment analysis of a twitter message
 * location analysis of a twitter message
 * visualisation of processed twitter messages
 * integration of FlatZone offers
 * extraction of municipality services
 * visualization of municipality services

## How to set-up things
* Instal virtualenvwrapper

  ```pip install virtualenvwrapper```
  
* Clone the repository
* Go to the folder with repository
* Make virtual environment

  ```mkvirtualenv -p /usr/bin/python3 love_have_and_prague```
  
* Install dependencies

  ```pip install -r requirements.txt```

* Download Sentiment-analysis model
  1. Download file https://drive.google.com/file/d/1_JUJK-wQ6xOMOXjAl1lyAubqJJI1vMH5/view?usp=sharing
  2. Put it into sentiment_analysis/models/combined_corpora_processed.bin