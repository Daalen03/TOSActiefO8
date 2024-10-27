import random

class Player:
    def __init__(self, name, id):
        self.name = name
        self.id = id

# Initialize player and goalkeeper lists
players = [Player("Lucie", 1), Player("Eliah", 2), Player("Victor", 3), Player("Walter", 4),
           Player("Vidar", 5), Player("Luis", 6), Player("Oscar", 7), Player("Evan", 8), Player("Yahto", 9)]
goalkeepers = [player for player in players if player.name in ["Walter", "Vidar"]]

random.shuffle(players)
random.shuffle(goalkeepers)

# Number of substitutions available
num_subs = 3 if len(players) == 9 else 0  # Adjust other cases if needed

def calculate_target_minutes(match_length, squad_size):
    return match_length * 6 / squad_size

def select_goalkeeper(goalkeepers, playing_time):
    return min(goalkeepers, key=lambda x: playing_time[x.name])

def create_segments(players, goalkeepers, target_minutes):
    segments = []
    playing_time = {player.name: 0 for player in players}
    mid_segment_subs = {player.name: False for player in players}
    segment_duration = 10

    for i in range(4):
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

        # Mid-segment substitution check
        if i > 0:  # No substitution in the first segment
            for position, player in list(segment.items()):
                if position not in ["Substitutes", "Goalkeeper"]:
                    if isinstance(player, dict):
                        for sub_position, sub_player in player.items():
                            if playing_time[sub_player.name] >= target_minutes and not mid_segment_subs[sub_player.name]:
                                substitute = min(substitutes, key=lambda x: playing_time[x.name])
                                if playing_time[substitute.name] < target_minutes:
                                    # Perform substitution and print details
                                    print(f"Mid-segment substitution in Segment {i+1}:")
                                    print(f"  Substituting {sub_player.name} (playing time: {playing_time[sub_player.name]} min)")
                                    print(f"  With {substitute.name} (playing time: {playing_time[substitute.name]} min)")

                                    # Substitute players
                                    segment[position][sub_position] = substitute
                                    substitutes.remove(substitute)
                                    substitutes.append(sub_player)
                                    mid_segment_subs[sub_player.name] = True
                                    # Update playing time
                                    playing_time[sub_player.name] += segment_duration // 2
                                    playing_time[substitute.name] += segment_duration // 2
                    elif playing_time[player.name] >= target_minutes and not mid_segment_subs[player.name]:
                        substitute = min(substitutes, key=lambda x: playing_time[x.name])
                        if playing_time[substitute.name] < target_minutes:
                            # Perform substitution and print details
                            print(f"Mid-segment substitution in Segment {i+1}:")
                            print(f"  Substituting {player.name} (playing time: {playing_time[player.name]} min)")
                            print(f"  With {substitute.name} (playing time: {playing_time[substitute.name]} min)")

                            # Substitute players
                            segment[position] = substitute
                            substitutes.remove(substitute)
                            substitutes.append(player)
                            mid_segment_subs[player.name] = True
                            # Update playing time
                            playing_time[player.name] += segment_duration // 2
                            playing_time[substitute.name] += segment_duration // 2

        segments.append(segment)

        # Update playing time for all players in the segment
        for position, player in segment.items():
            if position != "Substitutes":
                if isinstance(player, dict):
                    for sub_player in player.values():
                        if not mid_segment_subs[sub_player.name]:
                            playing_time[sub_player.name] += segment_duration
                else:
                    if not mid_segment_subs[player.name]:
                        playing_time[player.name] += segment_duration

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

print("Script has run successfully.")
