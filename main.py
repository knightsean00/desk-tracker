import pandas as pd
import datetime
import json

CONFIG_PATH = './config.json'
PACKAGES_PATH = './packages.csv'

# Creates a new config.json file storing the path to roster CSV file
# so that you don't need to re-enter the path every time you open the app
def set_roster_path(new_path):
    json_obj = {'ROSTER_PATH': new_path}
    with open(CONFIG_PATH, 'w') as f:
        json.dump(json_obj, f)

def log_package(packages_df, kerb, tracking_number, location):
    incoming_package_df = pd.DataFrame.from_dict({
        'kerb': kerb,
        'tracking_number': tracking_number,
        'time_received': datetime.now(),
        'time_delivered': None,
        'location': location, 
        'delivered': False
    })
    updated_packages_df = pd.concat(packages_df, incoming_package_df)
    updated_packages_df.to_csv(PACKAGES_PATH)

def deliver_package(packages_df, kerb, tracking_number):
    search_filter = (packages_df['kerb']==kerb) & (packages_df['tracking_number']==tracking_number)
    # TODO what if there are multiple packages with same kerb and tracking number?
    # Currently just treating them as the same package
    packages_df.loc[search_filter, 'delivered'] = True
    packages_df.loc[search_filter, 'time_delivered'] = datetime.now()
    packages_df.to_csv(PACKAGES_PATH)

if __name__ == '__main__':
    # Keep prompting for a new path to roster csv until one works
    while True:
        try:
            with open(CONFIG_PATH, 'r') as f:
                roster_path = json.load(f)
            roster_df = pd.read_csv(roster_path, header=0)
            # TODO assert that the roster_df columns here are correct
            break
        except:
            roster_path = input('Current path invalid. Enter new path to roster csv:\n')
            set_roster_path(roster_path)
    
    packages_df = pd.read_csv(PACKAGES_PATH, header=0)