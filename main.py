import random

# Initialize player and goalkeeper lists
players = ["Lucie", "Eliah", "Victor", "Walter", "Vidar", "Elis", "Oscar", "Evan", "Abou", "Luis"]
goalkeepers = ["Lucie", "Walter", "Vidar", "Elis"]

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

    # Assign substitutes for each segment first
    all_players = set(players)
    for i in range(4):
        # Assign the remaining players to other positions
        goalkeeper = select_goalkeeper(goalkeepers)

        # Ensure the goalkeeper is not selected as a substitute
        available_subs = list(all_players - set([goalkeeper]))

        # Call the select_substitutes function to select the substitutes
        segment_subs = select_substitutes(available_subs)

        # Compute playing time so far
        playing_time = compute_playing_time(segments)

        # Get players under target time
        options = [p for p in available_subs if playing_time[p] < target_minutes]

        # Select 5 field players with lowest time
        field_players = sorted(options, key=lambda p: playing_time[p])[:5]

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

    return segments

# Track substitute usage
sub_counts = {players: 0 for players in players}

def select_substitutes(available_players):

    # Filter by eligibility
    eligible = [player for player in available_players if sub_counts[player] < MAX_SUBS]

    subs = random.sample(eligible, num_subs)

    # Update counts
    for sub in subs:
        sub_counts[sub] += 1

    return subs


def compute_playing_time(segments):
    playing_time = {player: 0 for player in players}

    for segment in segments:
        for position, player in segment.items():
            if position != "Substitutes":
                if isinstance(player, dict):
                    for _, sub_player in player.items():
                        playing_time[sub_player] += 10
                else:
                    playing_time[player] += 10

    return playing_time


# Run the function to create segments
target_minutes = calculate_target_minutes(40, len(players))
print(target_minutes)
segments = create_segments(players, goalkeepers, target_minutes)
for i, segment in enumerate(segments, 1):
    print(f"Segment {i}: {segment}")

playing_time = compute_playing_time(segments)
print(playing_time)
