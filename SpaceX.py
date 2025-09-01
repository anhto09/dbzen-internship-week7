import requests
import csv

API_URL_LAUNCHES = "https://api.spacexdata.com/v4/launches"
API_URL_ROCKETS = "https://api.spacexdata.com/v4/rockets"

def fetch_spacex_launches():
    try:
        # Fetch launches
        response = requests.get(API_URL_LAUNCHES)
        response.raise_for_status()
        launches = response.json()

        # Sort launches by date (descending) to get latest
        launches = sorted(launches, key=lambda x: x['date_utc'], reverse=True)[:5]

        # Fetch all rockets once and map ID -> name
        rockets_response = requests.get(API_URL_ROCKETS)
        rockets_response.raise_for_status()
        rockets = rockets_response.json()
        rocket_dict = {rocket['id']: rocket['name'] for rocket in rockets}

        launch_data = []

        for launch in launches:
            mission_name = launch.get('name', 'N/A')
            launch_date = launch.get('date_utc', 'N/A')
            rocket_id = launch.get('rocket')
            rocket_name = rocket_dict.get(rocket_id, 'N/A')

            print(f"Mission Name: {mission_name}")
            print(f"Launch Date: {launch_date}")
            print(f"Rocket: {rocket_name}")
            print("-" * 30)

            launch_data.append({
                "Mission Name": mission_name,
                "Launch Date": launch_date,
                "Rocket": rocket_name
            })

        # Save to CSV
        csv_file = "spacex_launches.csv"
        with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["Mission Name", "Launch Date", "Rocket"])
            writer.writeheader()
            writer.writerows(launch_data)

        print(f"Launch data saved to {csv_file}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching SpaceX launches: {e}")

# Run the function
fetch_spacex_launches()
