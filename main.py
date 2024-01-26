import random

class Player:
  def __init__(self, name, id):
    self.name = name
    self.id = id

Lucie = Player("Lucie", 1)
Eliah = Player("Eliah", 2)
Victor = Player("Victor", 3)
Walter = Player("Walter", 4)
Vidar = Player("Vidar", 5)
Elis = Player("Elis", 6)
Oscar = Player("Oscar", 7)
Evan = Player("Evan", 8)
Abou = Player("Abou", 9)
Luis = Player("Luis", 10)

# Initialize player and goalkeeper lists
players = [Player("Lucie", 1), Player("Eliah", 2), Player("Victor", 3), Player("Walter", 4),
           Player("Vidar", 5), Player("Elis", 6), Player("Oscar", 7), Player("Evan", 8),
           Player("Abou", 9), Player("Luis", 10)]
goalkeepers = [Player("Lucie", 1), Player("Walter", 4), Player("Vidar", 5), Player("Elis", 6)]

# Number of substitutions available
if len(players) == 6:
    num_subs = 0
    MAX_SUBS = 0
elif len(players) == 7:
    num_subs = 1
    MAX_SUBS = 1
elif len(players) == 8:
    num_subs = 2
    MAX_SUBS = 1
elif len(players) == 9:
    num_subs = 3
    MAX_SUBS = 2
elif len(players) == 10:
    num_subs = 4
    MAX_SUBS = 2


def calculate_target_minutes(match_length, squad_size):
  return match_length * 6 / squad_size

def select_goalkeeper(candidates):
    """Randomly select and remove a goalkeeper from the candidate list."""
    goalkeeper = random.choice(candidates)
    candidates.remove(goalkeeper)
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

        # Ensure the goalkeeper is not selected as a substitute
        available_subs = list(all_players_set - set([goalkeeper]))

        # Call the select_substitutes function to select the substitutes
        segment_subs = select_substitutes(available_subs)

        # Compute playing time so far
        playing_time.update(compute_playing_time(segments))

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
    eligible = [player for player in available_players if sub_counts[player.name] < MAX_SUBS]

    subs = random.sample(eligible, num_subs)

    # Update counts
    for sub in subs:
        sub_counts[sub.name] += 1

    return subs


def compute_playing_time(segments):

    playing_time = {}

    for segment in segments:
        for position, pos_dict in segment.items():
            if position != "Substitutes":
                player = pos_dict
                name = pos_dict['name']

                if name not in playing_time:
                    playing_time[name] = 0

                playing_time[name] += 10

    return playing_time


# Run the function to create segments
target_minutes = calculate_target_minutes(40, len(players))
print(target_minutes)

segments, playing_time = create_segments(players, goalkeepers, target_minutes)
for i, segment in enumerate(segments, 1):
    print(f"Segment {i}: {segment}")

segment_time = compute_playing_time(segments)
for p in segment_time:
    playing_time[p] = segment_time[p]
