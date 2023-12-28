import random


def select_goalkeeper(candidates):
    """Randomly select and remove a goalkeeper from the candidate list."""
    goalkeeper = random.choice(candidates)
    candidates.remove(goalkeeper)
    return goalkeeper


def create_segments(players, goalkeepers):
    """Create lineups for each segment while satisfying constraints."""
    segments = []
    selected_substitutes = set()

    # Assign substitutes for each segment first
    all_players = set(players)
    for i in range(4):
        # Assign the remaining players to other positions
        goalkeeper = select_goalkeeper(goalkeepers)

        # Ensure the goalkeeper is not selected as a substitute
        available_subs = list(all_players - selected_substitutes - set([goalkeeper]))
        segment_subs = random.sample(available_subs, 2)
        for sub in segment_subs:
            selected_substitutes.add(sub)

        field_players = list(all_players - set(segment_subs) - set([goalkeeper]))
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


# Initialize player and goalkeeper lists
players = ["Abou", "Lucie", "Eliah", "Victor", "Walter", "Oscar", "Vidar", "Elis", "Leroy"]
goalkeepers = ["Lucie", "Walter", "Vidar", "Elis"]

# Run the function to create segments
segments = create_segments(players, goalkeepers)
for i, segment in enumerate(segments, 1):
    print(f"Segment {i}: {segment}")

playing_time = compute_playing_time(segments)
print(playing_time)
