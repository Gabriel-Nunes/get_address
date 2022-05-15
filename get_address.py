
import pandas as pd
from geopy.geocoders import Nominatim
import os


def get_address(file: str, coordinates: str, addr_dict: dict) -> str:
    print(f"==> Fetching coordinates ({coordinates})")
    
    # Check if the coordinate was already fetched
    if coordinates in addr_dict:
        return addr_dict.get(coordinates)
    
    try:
        u_agent = f'get_address_{file}'
        geolocator = Nominatim(user_agent=u_agent)
        location = geolocator.reverse(coordinates)
        addr_dict.update({coordinates: location})
        return location.address
    except:
        return 'Address could not be fetched.'


if __name__ == '__main__':

    input('''\nInstructions:

    1 - Save all '.xlsx' files to 'dados' folder.
    2 - Rename all coordinates columns to "latitude" and "longitude"

    Press any key to continue...''')

    # Dictionary to store fetched addresses
    addr_dict = {}

    for file in os.listdir('dados'):
        
        # Exclude temporary files and "_ok.xlsx" that are already with addresses
        if (file.endswith('xlsx')) and not (file.endswith('_ok.xlsx')) and ('$' not in file):
            print(f'\nReading file "{file}", wait...\n')    
            excel_content = pd.read_excel(os.path.join('dados', file), dtype='str')
            try:
                # Replace ',' for '.' on coordinates
                excel_content['latitude'] = excel_content['latitude'].str.replace(',', '.')
                excel_content['longitude'] = excel_content['longitude'].str.replace(',', '.')
            except KeyError as k:
                print(f"\nCan't find coordinate {k}. Rename all coordinates columns to 'latitude' and 'longitude'.\n")
                input("Press any key to finish...")
            
            # Create an "address" column with coordinates, drop empty values and get addresses
            excel_content['address'] = excel_content['latitude'] + ', ' + excel_content['longitude']
            excel_content.dropna(subset=['address'], inplace=True)  
            excel_content['address'] = excel_content['address'].apply(lambda x: get_address(file, x, addr_dict))
            
            # Save results to new '.xlsx'
            print("\nSaving results...\n")
            excel_content.to_excel(f"{os.path.join('dados', file).strip('.xlsx')}_ok.xlsx", index=False)

    input('\nPress any key to finish...')