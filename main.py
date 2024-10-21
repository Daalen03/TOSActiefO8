import random

class Player:
  def __init__(self, name, id):
    self.name = name
    self.id = id

# Initialize player and goalkeeper lists
players = [Player("Lucie", 1), Player("Eliah", 2), Player("Victor", 3), Player("Walter", 4),
           Player("Vidar", 5), Player("Luis", 6), Player("Oscar", 7), Player("Evan", 8), Player("Yahto", 9)]
goalkeepers = [player for player in players if player.name in ["Lucie", "Walter", "Vidar"]]

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

def create_segments(players, goalkeepers):
    # segments, playing_time = create_segments(players, goalkeepers, target_minutes)
    """Create lineups for each segment while satisfying constraints."""
    segments = []

    for i in range(4):
        # Assign the remaining players to other positions
        all_players = players.copy()
        goalkeeper = select_goalkeeper(goalkeepers)
        all_players.remove(goalkeeper)
        print(goalkeeper)

        field_players = select_field_players(all_players, num_field_players=5)
        for player in field_players:
            all_players.remove(player)

        substitutes = select_substitutes(all_players, num_subs)

        segment = {
            "Goalkeeper": goalkeeper,
            "Defenders": {"Left": field_players[0], "Right": field_players[1]},
            "Midfielder": field_players[2],
            "Attackers": {"Left": field_players[3], "Right": field_players[4]},
            "Substitutes": substitutes,
        }
        segments.append(segment)

    return segments

# Track substitute usage
sub_counts = {player.name: 0 for player in players}

def select_substitutes(available_players, num_subs):
    if len(available_players) < num_subs:
        return available_players  # Return all available players if not enough
    return random.sample(available_players, num_subs)

def select_field_players(players, num_field_players):
    if len(players) < num_field_players:
        return players  # Return all available players if not enough
    return random.sample(players, num_field_players)


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

# segments, playing_time = create_segments(players, goalkeepers, target_minutes)
segments = create_segments(players, goalkeepers)
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
