"""
Name: Logan McDavid
Filename: scrimmage.py    
Purpose: Contains scrimamge class for
scrimmage_commands
"""

class Scrimmage:
    def __init__(self):
        self.purple_team = []
        self.gold_team = []
        self.cutters = []
        self.handlers = []
        self.hybrids = []
        
    """
    Function: split_even
    Purpose: Split the number of players 
    in a list in half 
    """
    def split_even(self, player_list):
        # half = len(player_list) // 2
        # Odd number of players
        if len(player_list) % 2 != 0:
            odd_player = player_list.pop()
            return player_list[:len(player_list) // 2], player_list[len(player_list) //2:], odd_player
        else:
            return player_list[:len(player_list) // 2], player_list[len(player_list) //2:], None
        
