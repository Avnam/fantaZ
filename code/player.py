import requests
import json
import sys

class player:
	def __init__ (self, _id):
		self.id = _id
		self.resp = requests.get('https://fantasy.premierleague.com/api/element-summary/' + str(_id) + '/')
		
		if self.resp.status_code != 200:
		    # This means something went wrong.
		    raise ApiError('GET /tasks/ {}'.format(self.resp.status_code))
	
	def print(self, outFile = sys.stdout):
		print (json.dumps(self.resp.json(), sort_keys=False, indent=4), file = outFile)
		
		#with open('../ta.txt', 'a') as the_file:
		#	print (json.dumps(x.json(), sort_keys=False, indent=4), file=the_file)

#resp = requests.get('https://fantasy.premierleague.com/api/element-summary/496/')
#
#if resp.status_code != 200:
#    # This means something went wrong.
#    raise ApiError('GET /tasks/ {}'.format(resp.status_code))
#			
#print (json.dumps(resp.json(), sort_keys=False, indent=4))

#x = player(1)
#x.print()