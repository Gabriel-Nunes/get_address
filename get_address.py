
import pandas as pd
from geopy.geocoders import Nominatim
import os


loc_dict = {}

input('''\nInstructions:

1 - Save all '.xlsx' files to 'dados' folder.
2 - Rename all coordinates columns to "latitude" and "longitude"

Press any key to continue...''')

def get_address(user_agent, file, coordinates) -> str:
    print(f"==> Fetching coordinates ({coordinates})")
    if coordinates in loc_dict:
        return loc_dict.get(coordinates)
    try:
        user_agent = f'get_address_{file}'
        geolocator = Nominatim(user_agent=user_agent)
        location = geolocator.reverse(coordinates)
        loc_dict.update({coordinates: location})
        return location.address
    except:
        return 'Address could not be fetched.'


for file in os.listdir('dados'):
    if (file.endswith('xlsx')) and not (file.endswith('_ok.xlsx')) and ('$' not in file):
        print(f'\nReading file "{file}", wait...\n')    
        excel_content = pd.read_excel(os.path.join('dados', file), dtype='str')
        try:
            excel_content['latitude'] = excel_content['latitude'].str.replace(',', '.')
            excel_content['longitude'] = excel_content['longitude'].str.replace(',', '.')
        except:
            pass
        
        excel_content['address'] = excel_content['latitude'] + ', ' + excel_content['longitude']
        excel_content.dropna(subset=['address'], inplace=True)
        excel_content['address'] = excel_content['address'].apply(lambda x: get_address('test', file, x))
        
        print("\nSaving results...\n")
        excel_content.to_excel(f"{os.path.join('dados', file).strip('.xlsx')}_ok.xlsx", index=False)

input('\nPress any key to finish...')