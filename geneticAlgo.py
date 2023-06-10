import csv
import random

# Load user balance and desired rates
with open('./csv/user_money_rates.csv', 'r') as user_file:
    user_data = list(csv.reader(user_file))

# Load album prices
with open('./csv/album_price.csv', 'r') as album_file:
    album_data = list(csv.reader(album_file))

# Convert album prices to integers
album_prices = [int(float(price[0])) for price in album_data]

# Get the total number of albums
num_albums = len(album_prices)

# Generate a list of album IDs based on the row numbers
album_ids = list(range(1, num_albums + 1))

# Shuffle the album IDs to select 50 random discs
random.shuffle(album_ids)
selected_albums = album_ids[:50]

# Initialize a list to store the selected albums and total spending for each user
user_selections = []

# Iterate over each user
for user in user_data:
    available_balance = int(float(user[0]))
    desired_rates = [int(float(rate)) for rate in user[1:]]

    # Create a list of (album_id, album_price) tuples
    albums = list(zip(selected_albums, album_prices))

    # Sort albums based on the desired rates (in descending order)
    albums.sort(key=lambda x: desired_rates[x[1] - 1], reverse=True)

    # Select albums that can be afforded within the available balance
    selected = []
    total_spending = 0
    for album in albums:
        if available_balance >= album[1]:
            selected.append(album[0])
            total_spending += album[1]
            available_balance -= album[1]

    # Store the selected albums and total spending for the user
    user_selections.append((selected, total_spending))

# Export the selected albums and total spending for each user to a file
output_file = './csv/user_selections.csv'
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for i, (albums, total_spending) in enumerate(user_selections):
        user_id = i + 1
        writer.writerow([f"User {user_id}"] + albums + [total_spending])
