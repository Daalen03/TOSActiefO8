import random
import pandas as pd

list_even = ["Lucie", "Walter", "Vidar", "Elis"]
list_odd = ["Oscar", "Walter", "Eliah", "Lucie"]

list_all = ["Abou", "Lucie", "Eliah", "Victor", "Walter", "Oscar", "Vidar", "Elis"]

selected_substitutes = []

# Segment 1
random.shuffle(list_even)
goalkeeper = list_even.pop(0)
# print(goalkeeper)

goalkeeper = pd.Series(goalkeeper)
list_all = pd.Series(list_all.copy())

mask = ~list_all.isin(goalkeeper)
result_segment1 = list_all[mask]
segment1 = result_segment1.to_list()

random.shuffle(segment1)

# Initial setup for Segment 1
segments = [
    {
        "Goalkeeper": goalkeeper[0],
        "Defenders": {"Left": segment1[0], "Right": segment1[1]},
        "Midfielder": segment1[2],
        "Attackers": {"Left": segment1[3], "Right": segment1[4]},
        "Substitutes": segment1[5:],
    }
]

substitutes = segment1[5:]
selected_substitutes.extend(substitutes)
print(segments)
# print(selected_substitutes)

# Segment 2
goalkeeper2 = list_even.pop(0)

goalkeeper2 = pd.Series(goalkeeper2)
list_all2 = pd.Series(list_all.copy())
already_substituted = pd.Series(selected_substitutes)

mask = ~list_all2.isin(goalkeeper2)
result_segment2 = list_all2[mask]
mask_subs = ~result_segment2.isin(already_substituted)
available_subs = result_segment2[mask_subs]
available_subs = available_subs.tolist()
# print(f"Available Subs {available_subs}")
subs_segment2 = available_subs[0:2]
# print(f"Subs for Segment 2 are {subs_segment2}")

subs = pd.Series(subs_segment2)
mask_lineup_players = ~result_segment2.isin(subs)
lineup = result_segment2[mask_lineup_players]
segment2 = lineup.to_list()
# print(f"Segment 2 {segment2}")

random.shuffle(segment2)

# Initial setup for Segment 2
segments = [
    {
        "Goalkeeper": goalkeeper2[0],
        "Defenders": {"Left": segment2[0], "Right": segment2[1]},
        "Midfielder": segment2[2],
        "Attackers": {"Left": segment2[3], "Right": segment2[4]},
        "Substitutes": subs_segment2[0:],
    }
]

print(segments)
selected_substitutes.extend(subs_segment2)
# print(selected_substitutes)


# Segment 3
goalkeeper3 = list_even.pop(0)
# print(goalkeeper3)

goalkeeper3 = pd.Series(goalkeeper3)
list_all3 = pd.Series(list_all.copy())
already_substituted_2 = pd.Series(selected_substitutes)
# print(f"Already Subbed {already_substituted_2}")

mask_2 = ~list_all3.isin(goalkeeper3)
result_segment3 = list_all3[mask_2]
mask_subs_2 = ~result_segment3.isin(already_substituted_2)
available_subs_2 = result_segment3[mask_subs_2]
available_subs_2 = available_subs_2.tolist()
# print(f"Available Subs {available_subs_2}")
subs_segment3 = available_subs_2[0:2]
# print(f"Subs for Segment 3 are {subs_segment3}")

subs_2 = pd.Series(subs_segment3)
mask_lineup_players_2 = ~result_segment3.isin(subs_2)
lineup_2 = result_segment3[mask_lineup_players_2]
segment3 = lineup_2.to_list()
# print(f"Segment 3 {segment3}")

random.shuffle(segment3)

# Initial setup for Segment 3
segments = [
    {
        "Goalkeeper": goalkeeper3[0],
        "Defenders": {"Left": segment3[0], "Right": segment3[1]},
        "Midfielder": segment3[2],
        "Attackers": {"Left": segment3[3], "Right": segment3[4]},
        "Substitutes": subs_segment3[0:],
    }
]

print(segments)
selected_substitutes.extend(subs_segment3)
# print(selected_substitutes)

# Segment 4
goalkeeper4 = list_even.pop(0)
# print(goalkeeper4)

goalkeeper4 = pd.Series(goalkeeper4)
list_all4 = pd.Series(list_all.copy())
already_substituted_3 = pd.Series(selected_substitutes)
# print(f"Already Subbed {already_substituted_3}")

mask_3 = ~list_all4.isin(goalkeeper4)
result_segment4 = list_all4[mask_3]
mask_subs_3 = ~result_segment4.isin(already_substituted_3)
available_subs_3 = result_segment4[mask_subs_3]
available_subs_3 = available_subs_3.tolist()
# print(f"Available Subs {available_subs_3}")
subs_segment4 = available_subs_3[0:2]
# print(f"Subs for Segment 4 are {subs_segment4}")

subs_3 = pd.Series(subs_segment4)
mask_lineup_players_3 = ~result_segment4.isin(subs_3)
lineup_3 = result_segment4[mask_lineup_players_3]
segment4 = lineup_3.to_list()
# print(f"Segment 4 {segment4}")

random.shuffle(segment4)

# Initial setup for Segment 4
segments = [
    {
        "Goalkeeper": goalkeeper4[0],
        "Defenders": {"Left": segment4[0], "Right": segment4[1]},
        "Midfielder": segment4[2],
        "Attackers": {"Left": segment4[3], "Right": segment4[4]},
        "Substitutes": subs_segment4[0:],
    }
]

print(segments)
selected_substitutes.extend(subs_segment4)
print(selected_substitutes)
