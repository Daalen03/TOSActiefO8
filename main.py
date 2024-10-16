import random

class Player:
  def __init__(self, name, id):
    self.name = name
    self.id = id

# Lucie = Player("Lucie", 1)
# Eliah = Player("Eliah", 2)
# Victor = Player("Victor", 3)
# Walter = Player("Walter", 4)
# Vidar = Player("Vidar", 5)
# Luis = Player("Elis", 6)
# Oscar = Player("Oscar", 7)
# Evan = Player("Evan", 8)
# Yahto = Player("Yahto", 9)


# Initialize player and goalkeeper lists
players = [Player("Lucie", 1), Player("Eliah", 2), Player("Victor", 3), Player("Walter", 4),
           Player("Vidar", 5), Player("Luis", 6), Player("Oscar", 7), Player("Evan", 8), Player("Yahto", 9)]
goalkeepers = [Player("Lucie", 1), Player("Walter", 4), Player("Vidar", 5)]

# Number of substitutions available
if len(players) == 6:
    num_subs = 0
elif len(players) == 7:
    num_subs = 1
elif len(players) == 8:
    num_subs = 2
elif len(players) == 9:
    num_subs = 3
elif len(players) == 10:
    num_subs = 4

def calculate_target_minutes(match_length, squad_size):
  return match_length * 6 / squad_size

def select_goalkeeper(candidates):
    """Randomly select and remove a goalkeeper from the candidate list."""
    goalkeeper = random.choice(candidates)
    return goalkeeper


def create_segments(players, goalkeepers, target_minutes):
    """Create lineups for each segment while satisfying constraints."""
    segments = []

    all_players = players + goalkeepers
    all_players_set = set(all_players)

    # Initialize playing time for all players
    playing_time = {p.name: 0 for p in all_players}


    for i in range(4):
        # Assign the remaining players to other positions
        goalkeeper = select_goalkeeper(goalkeepers)
        print(goalkeeper)

        # Ensure the goalkeeper is not selected as a substitute
        available_subs = list(all_players_set) #(all_players_set - {goalkeeper})
        available_subs.remove(goalkeeper)
        print(goalkeeper, goalkeeper.name, goalkeeper.id)
        available_sub_names = [p.name for p in available_subs]
        available_sub_ids = [p.id for p in available_subs]
        print(available_subs, available_sub_names, available_sub_ids)

        # Call the select_substitutes function to select the substitutes
        segment_subs = select_substitutes(available_subs)

        # Compute playing time so far
        # playing_time.update(compute_playing_time(segments))

        # Get players under target time
        options = [p for p in available_subs if playing_time[p.name] < target_minutes]

        # Select 5 field players with lowest time
        field_players = sorted(options, key=lambda p: playing_time[p.name])[:5]

        # field_players = list(all_players - set(segment_subs) - set([goalkeeper]))
        random.shuffle(field_players)

        segment = {
            "Goalkeeper": goalkeeper,
            "Defenders": {"Left": field_players[0], "Right": field_players[1]},
            "Midfielder": field_players[2],
            "Attackers": {"Left": field_players[3], "Right": field_players[4]},
            "Substitutes": segment_subs,
        }
        segments.append(segment)

    return segments, playing_time

# Track substitute usage
sub_counts = {player.name: 0 for player in players}

def select_substitutes(available_players):

    # Filter by eligibility
    eligible = [player for player in available_players if sub_counts[player.name] < num_subs]

    subs = random.sample(eligible, num_subs)

    # Update counts
    for sub in subs:
        sub_counts[sub.name] += 1

    return subs


# def compute_playing_time(segments):
#     playing_time = {}
#
#     for segment in segments:
#         try:
#             for position, pos_dict in segment.items():
#                 if position == "Substitutes" and isinstance(pos_dict, list):
#                     for sub in pos_dict:
#                         name = sub.name
#
#                         if name not in playing_time:
#                             playing_time[name] = 0
#
#                         playing_time[name] += 10
#
#                 elif position != "Substitutes":
#
#                     if isinstance(pos_dict, Player):
#                         name = pos_dict.name
#
#                         if name not in playing_time:
#                             playing_time[name] = 0
#
#                         playing_time[name] += 10
#
#                     elif isinstance(pos_dict, list):
#                         for player in pos_dict:
#                             name = player.name
#
#                             if name not in playing_time:
#                                 playing_time[name] = 0
#
#                             playing_time[name] += 10
#
#                     else:
#                         raise ValueError("Invalid position dict")
#
#                 else:
#                     raise ValueError("Invalid position dict")
#
#         except ValueError as e:
#             print("Invalid segment:", segment)
#             raise e
#
#     return playing_time

# Run the function to create segments
target_minutes = calculate_target_minutes(40, len(players))
print(target_minutes)

segments, playing_time = create_segments(players, goalkeepers, target_minutes)
for i, segment in enumerate(segments, 1):
    print(f"Segment {i}:")
    print(f"  Goalkeeper: {segment['Goalkeeper'].name}")
    print(f"  Defenders: Left - {segment['Defenders']['Left'].name}, Right - {segment['Defenders']['Right'].name}")
    print(f"  Midfielder: {segment['Midfielder'].name}")
    print(f"  Attackers: Left - {segment['Attackers']['Left'].name}, Right - {segment['Attackers']['Right'].name}")
    print(f"  Substitutes: {', '.join(sub.name for sub in segment['Substitutes'])}")
    print()
# segment_time = compute_playing_time(segments)
# for p in segment_time:
#     playing_time[p] = segment_time[p]
