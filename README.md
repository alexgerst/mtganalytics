# MtgPowerLevel

## Overview

This is a Python script for analyzing average power levels of MTG cards (based on Gatherer ratings). Currently it has functionality for fetching a list of all MTG cards from mtgjson.com, then fetching all the ratings for those cards from Gatherer. Once that data has been obtained, users can do with it what they wish. The script will eventually provide some of its own functionality for data analytics.

## Usage

Fetch card information from MTG JSON:

    python mtgpowerlevel.py fetchcards cards.json

Fetch card ratings from Gatherer:

    python mtgpowerlevel.py fetchratings cards.json ratings.json

