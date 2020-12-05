import json
from itertools import chain
import copy

season = "1920"
dataLoc = "../data/" + season + "/"

class Player:
    def __init__(self, fName, lName, role):
        self.fName = fName
        self.lName = lName
        self.role = role

    def setTeam(self, team):
        self.team = team

    def getTeam(self):
        return self.team

    def getName(self):
        return self.fName + " " + self.lName 

    def getRole(self):
        return self.role

    def getFileName(self):
        return dataLoc + "players/" + self.fName + '_' + self.lName + '.txt'

class Team:
    def __init__(self, name, id):
       self.name = name
       self.id = id
       self.players = []

    def add_player(self, player):
        self.players.append(player)


teams_list = {}
roles_list = {}

with open(dataLoc + "allData/" + season + ".txt") as GD_json_file:
    general_data = json.load(GD_json_file)
    teamsList = general_data['teams']


    roles = general_data['element_types']
    for role in roles:
        roles_list[role['id']] = role['singular_name_short']

    for team in teamsList:
        t = Team (team['name'], team['id'])
        teams_list[team['id']] = t
        
    playersList = general_data['elements']
    for player in playersList:
        p = Player(player['first_name'], player['second_name'], roles_list[player['element_type']])
        p.setTeam(teams_list[player['team']])
        teams_list[player['team']].add_player(p)

#roundRanges = range(0, 38)
roundRanges = chain(range(0, 29), range(38,47))

roundsStr = ""    
for i in copy.deepcopy(roundRanges):
    roundsStr = roundsStr + str(i+1) + ", "

with open(dataLoc + "out_rounds.csv", "w")  as outFile:
    with open(dataLoc + "out_rounds_sum.csv", "w")  as outSumFile:
        with open(dataLoc + "out_rounds_sum_from_here.csv", "w")  as outSumFromHereFile:
            
            outFile.write("team, role, player, " + roundsStr + "\n")
            outSumFile.write("team, role, player, " + roundsStr + "\n")
            outSumFromHereFile.write("team, role, player, 0, " + roundsStr + "\n")
            
            for key, value in teams_list.items():
                for p in value.players:
                    rounds = {}
                    with open(p.getFileName()) as player_json_file:
                        
                        total_games = 0
                        player_data = json.load(player_json_file)
                        for round in player_data['history']:
                            if round['round'] in rounds:
                                rounds[round['round']] = rounds[round['round']] + round['total_points']
                            else:
                                rounds[round['round']] = round['total_points']

                            if round['minutes']>0:
                                total_games = total_games+1       


                        total = 0
                        round_str = p.getTeam().name +  ", " + p.getRole() + ', ' + p.getName() + ", "
                        round_sum_str = p.getTeam().name +  ", " + p.getRole() + ', ' + p.getName() + ", "
                        
                        for i in copy.deepcopy(roundRanges):
                            if i+1 in rounds:
                                total = total + rounds[i+1]
                                round_str = round_str + str(rounds[i+1]) + ', '
                            else:
                                round_str = round_str + '-, '

                            round_sum_str = round_sum_str + str(total) + ', '

                        if total_games == 0:
                            total_games = 1
                        
                        outFile.write(round_str + str(total) + ","+str(total_games)+","+str(total/total_games)+"\n")
                        outSumFile.write(round_sum_str + "\n")

                        total_from_here_sum = p.getTeam().name +  ", " + p.getRole() + ', ' + p.getName() + ", " + str(total) + ", "

                        for i in copy.deepcopy(roundRanges):
                            if i+1 in rounds:
                                total = total - rounds[i+1]

                            total_from_here_sum = total_from_here_sum + str(total) + ', '
                        
                        outSumFromHereFile.write(total_from_here_sum + "\n")
                
    #data = json.load(json_file)
    #x = 12
    #data['history']
    #x = 3