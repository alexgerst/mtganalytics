import sys
import urllib2
import json
import re
import operator


# Threshold for vote counts, below which we ignore Gatherer ratings
threshold = 10

# URL for MTG JSON card data
mtgjson_url = 'http://mtgjson.com/json/AllSetsArray-x.json'

# Base URL for Gatherer card data
gatherer_url = 'http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid='

# Regular expressions for parsing Gatherer pages
rating_regex = re.compile('class="textRatingValue">(\d+(\.\d*)?|\.\d+)</span>')
votes_regex = re.compile('class="totalVotesValue">(\d+)</span>')


# Fetch card information from MTG JSON
def fetch_cards(output_filename):

    # Dictionary to be populated
    card_dict = {}

    # Load card data from MTG JSON
    print('Downloading data from MTG JSON')
    response = urllib2.urlopen(mtgjson_url)
    card_set_list = json.load(response)

    # Iterate through all cards and strip out unneeded info
    try:
        for card_set in card_set_list:
            for card in card_set['cards']:
                if 'multiverseid' in card.keys() and 'types' in card.keys():
                    print('%s (%d)' % (card['name'], card['multiverseid']))
                    if card['name'] not in card_dict.keys():
                        card_dict[card['name']] = {
                            'types': card['types'], 
                            'ids': []
                        }
                    card_dict[card['name']]['ids'].append(card['multiverseid'])
    except:
        pass

    # Write card data to JSON file
    with open(output_filename, 'w') as output_file:
        json.dump(card_dict, output_file)
    return


# Fetch card ratings from Gatherer
def fetch_ratings(input_filename, output_filename):

    # Load card data from file
    with open(input_filename, 'r') as input_file:
        card_dict = json.load(input_file)

    # Iterate through all cards and fetch their ratings
    try:
        for card_name in card_dict.keys():
            total_rating = 0.0
            num_ratings = 0
            for card_id in card_dict[card_name]['ids']:
                print('%s (%d)' % (card_name, card_id))
                response = urllib2.urlopen(gatherer_url + str(card_id))
                response_data = response.read()
                rating = float(rating_regex.search(response_data).group(1))
                votes = int(votes_regex.search(response_data).group(1))
                if votes >= threshold:
                    total_rating += rating
                    num_ratings += 1
            if num_ratings == 0:
                card_dict[card_name]['rating'] = None
            else:
                card_dict[card_name]['rating'] = total_rating / num_ratings
    except:
        pass

    # Write card data to JSON file
    with open(output_filename, 'w') as output_file:
        json.dump(card_dict, output_file)
    return


# Analyze card types relative to ratings
def analyze_types(input_filename):

    # Dictionary to be populated
    rating_dict = {}

    # Load card data from file
    with open(input_filename, 'r') as input_file:
        card_dict = json.load(input_file)

    # Iterate through all cards and analyze their ratings and types
    for card_name in card_dict.keys():
        for type_name in card_dict[card_name]['types']:
            if 'rating' in card_dict[card_name].keys():
                if type_name not in rating_dict.keys():
                    rating_dict[type_name] = []
                rating_dict[type_name].append(card_dict[card_name]['rating'])

    # Iterate through ratings and calculate averages
    for type_name in rating_dict.keys():
        total_rating = 0.0
        num_ratings = 0
        for rating in rating_dict[type_name]:
            if rating is not None:
                total_rating += rating
                num_ratings += 1
        del rating_dict[type_name]
        if num_ratings > 0:
            rating_dict[type_name] = total_rating / num_ratings

    # Print results
    for item in sorted(rating_dict.items(), key=operator.itemgetter(1)):
        print('%-15s %.3f' % (item))
    return


if len(sys.argv) == 3 and sys.argv[1] == 'fetchcards':
    fetch_cards(sys.argv[2])
elif len(sys.argv) == 4 and sys.argv[1] == 'fetchratings':
    fetch_ratings(sys.argv[2], sys.argv[3])
elif len(sys.argv) == 3 and sys.argv[1] == 'analyzetypes':
    analyze_types(sys.argv[2])
else:
    print('Usage:')
    print('')
    print('Fetch card information from MTG JSON:')
    print('    python mtgpowerlevel.py fetchcards cards.json')
    print('')
    print('Fetch card ratings from Gatherer:')
    print('    python mtgpowerlevel.py fetchratings cards.json ratings.json')

