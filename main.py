import random

class Player:
    def __init__(self, name, id):
        self.name = name
        self.id = id

# Initialize player and goalkeeper lists
players = [Player("Eliah", 2), Player("Victor", 3), Player("Walter", 4),
           Player("Vidar", 5), Player("Luis", 6), Player("Oscar", 7), Player("Evan", 8), Player("Yahto", 9)]
goalkeepers = [player for player in players if player.name in ["Walter", "Vidar"]]

random.shuffle(players)
random.shuffle(goalkeepers)

# Number of substitutions available
num_subs = len(players) - 6

def calculate_target_minutes(match_length, squad_size):
    return match_length * 6 / squad_size

def select_goalkeeper(goalkeepers, playing_time):
    return min(goalkeepers, key=lambda x: playing_time[x.name])


def create_segments(players, goalkeepers, target_minutes):
    segments = []
    playing_time = {player.name: 0 for player in players}

    for _ in range(4):
        random.shuffle(players)
        all_players = players.copy()
        goalkeeper = select_goalkeeper(goalkeepers, playing_time)
        all_players.remove(goalkeeper)

        field_players = select_field_players(all_players, 5, playing_time)
        for player in field_players:
            all_players.remove(player)

        substitutes = select_substitutes(all_players, num_subs, playing_time)

        segment = {
            "Goalkeeper": goalkeeper,
            "Defenders": {"Left": field_players[0], "Right": field_players[1]},
            "Midfielder": field_players[2],
            "Attackers": {"Left": field_players[3], "Right": field_players[4]},
            "Substitutes": substitutes,
        }
        segments.append(segment)

        # Update playing time
        for position, player in segment.items():
            if position != "Substitutes":
                if isinstance(player, dict):
                    for sub_player in player.values():
                        playing_time[sub_player.name] += 10
                else:
                    playing_time[player.name] += 10

    return segments, playing_time


def track_playing_time(players, segments):
    playing_time = {player.name: 0 for player in players}
    segment_duration = 10

    for segment in segments:
        for position, player in segment.items():
            if position != "Substitutes":
                if isinstance(player, dict):
                    for sub_position, sub_player in player.items():
                        playing_time[sub_player.name] += segment_duration
                else:
                    playing_time[player.name] += segment_duration

    return playing_time

def select_substitutes(available_players, num_subs, playing_time):
    # Sort players by playing time in descending order to select those with the most time
    available_players = sorted(available_players, key=lambda x: playing_time[x.name], reverse=True)
    return available_players[:num_subs]

def select_field_players(players, num_field_players, playing_time):
    # Sort players by playing time in ascending order to select those with the least time
    players = sorted(players, key=lambda x: playing_time[x.name])
    return players[:num_field_players]


def suggest_mid_segment_substitutions(segments, playing_time, target_minutes):
    suggestions = []
    for i, segment in enumerate(segments):
        segment_suggestions = []
        used_substitutes = set()
        for position, player in segment.items():
            if position not in ["Substitutes", "Goalkeeper"]:
                if isinstance(player, dict):
                    for sub_position, sub_player in player.items():
                        substitute = check_for_substitution(sub_player, segment["Substitutes"], playing_time,
                                                            target_minutes, used_substitutes)
                        if substitute:
                            segment_suggestions.append((i + 1, position, sub_position, sub_player, substitute))
                            used_substitutes.add(substitute.name)
                else:
                    substitute = check_for_substitution(player, segment["Substitutes"], playing_time, target_minutes,
                                                        used_substitutes)
                    if substitute:
                        segment_suggestions.append((i + 1, position, None, player, substitute))
                        used_substitutes.add(substitute.name)

        suggestions.extend(segment_suggestions[:len(segment["Substitutes"])])

    return suggestions


def process_player(player, substitutes, projected_time, target_minutes, substituted_players, segment_suggestions,
                   segment_index, position, sub_position=None):
    if player.name not in substituted_players:
        substitute = check_for_substitution(player, substitutes, projected_time, target_minutes)



def update_segment_projected_time(segment, projected_time, segment_duration, segment_suggestions):
    for position, player in segment.items():
        if position != "Substitutes":
            if isinstance(player, dict):
                for sub_player in player.values():
                    projected_time[sub_player.name] += segment_duration
            else:
                projected_time[player.name] += segment_duration

    # Adjust for suggested substitutions
    for _, _, _, player_out, player_in in segment_suggestions:
        projected_time[player_out.name] -= segment_duration / 2
        projected_time[player_in.name] += segment_duration / 2



def update_projected_time(projected_time, player_out, player_in, substitution_time):
    projected_time[player_out.name] -= substitution_time
    projected_time[player_in.name] += substitution_time

def check_for_substitution(player, substitutes, playing_time, target_minutes, used_substitutes):
    if playing_time[player.name] >= target_minutes:
        eligible_subs = [sub for sub in substitutes if playing_time[sub.name] < target_minutes and sub.name not in used_substitutes]
        if eligible_subs:
            return min(eligible_subs, key=lambda x: playing_time[x.name])
    return None


# Run the function to create segments
# target_minutes = 20
target_minutes = calculate_target_minutes(40, len(players))
print(f"Target minutes: {target_minutes}")
segments, playing_time = create_segments(players, goalkeepers, target_minutes)

for i, segment in enumerate(segments, 1):
    print(f"Segment {i}:")
    print(f"  Goalkeeper: {segment['Goalkeeper'].name}")
    print(f"  Defenders: Left - {segment['Defenders']['Left'].name}, Right - {segment['Defenders']['Right'].name}")
    print(f"  Midfielder: {segment['Midfielder'].name}")
    print(f"  Attackers: Left - {segment['Attackers']['Left'].name}, Right - {segment['Attackers']['Right'].name}")
    print(f"  Substitutes: {', '.join(sub.name for sub in segment['Substitutes'])}")
    print()

# Print final playing time for each player
for player, time in playing_time.items():
    print(f"{player}: {time} minutes")

# At the end of your script, after creating segments and calculating playing time:
substitution_suggestions = suggest_mid_segment_substitutions(segments, playing_time, target_minutes)

for suggestion in substitution_suggestions:
    segment, position, sub_position, player_out, player_in = suggestion
    if sub_position:
        print(f"Segment {segment}: Suggest substituting {player_out.name} with {player_in.name} at {position} {sub_position}")
    else:
        print(f"Segment {segment}: Suggest substituting {player_out.name} with {player_in.name} at {position}")

print("Script has run successfully.")
