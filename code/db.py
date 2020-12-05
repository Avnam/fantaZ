import requests
import json
from player import player

prints = True
season = "1920"
resp = requests.get('https://fantasy.premierleague.com/api/bootstrap-static/')

if resp.status_code != 200:
    # This means something went wrong.
    raise ApiError('GET /tasks/ {}'.format(resp.status_code))

if (prints):
	print ("printing mainDB")
	
with open('../players/' + season + '.txt', 'w') as the_file:
	print (json.dumps(resp.json(), sort_keys=False, indent=4), file = the_file)

for _player in resp.json()['elements']:
#	print (_player)
	pId = _player['id']
	p = player(pId)
	if (prints):
		print ("printing " + _player['first_name']+ ' ' + _player['second_name'] + " file");
	with open('../players/' + season +'/' + _player['first_name']+ '_' + _player['second_name'] +'.txt', 'w') as the_file:
		p.print(the_file)


#	playerResp = requests.get('https://fantasy.premierleague.com/drf/element-summary/' + str(pId))
#	
#	with open('../players1920/' + _player['first_name']+ '_' + _player['second_name'] +'.txt', 'w') as the_file:
#		print (json.dumps(playerResp.json(), sort_keys=False, indent=4), file=the_file)
	