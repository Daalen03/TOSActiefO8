import random

list_even = ["Lucie", "Victor", "Abou", "Elis"]
list_odd = ["Oscar", "Walter", "Malin", "Lucie"]
players_with_names = [
    "Abou",
    "Lucie",
    "Malin",
    "Victor",
    "Walter",
    "Oscar",
    "Eliah",
    "Elis",
]


def select_and_pop(
    match_type, list_even, list_odd, players_with_names, previous_selected=None
):
    # If there's a previously selected name, add it back to the players_with_names
    if previous_selected:
        players_with_names.append(previous_selected)

    # Determine which list to use based on the match_type
    current_list = list_even if match_type == "even" else list_odd

    # Shuffle the list
    random.shuffle(current_list)

    # Pop the first name
    selected_name = current_list.pop(0)

    # Remove the selected name from players_with_names
    players_with_names.remove(selected_name)

    return selected_name, list_even, list_odd, players_with_names


# First iteration
match_type = "odd"
first_selected, list_even, list_odd, players_with_names = select_and_pop(
    match_type, list_even, list_odd, players_with_names
)
print("1st Selected Name:", first_selected)

# Second iteration
second_selected, list_even, list_odd, players_with_names = select_and_pop(
    match_type, list_even, list_odd, players_with_names, first_selected
)
print("2nd Selected Name:", second_selected)

# Third iteration
third_selected, list_even, list_odd, players_with_names = select_and_pop(
    match_type, list_even, list_odd, players_with_names, second_selected
)
print("3rd Selected Name:", third_selected)

# Fourth iteration
fourth_selected, list_even, list_odd, players_with_names = select_and_pop(
    match_type, list_even, list_odd, players_with_names, third_selected
)
print("4th Selected Name:", fourth_selected)
print("Updated list_even:", list_even)
print("Updated list_odd:", list_odd)
print("Updated players_with_names:", players_with_names)
