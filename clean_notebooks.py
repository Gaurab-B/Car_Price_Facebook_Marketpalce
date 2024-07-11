import pandas as pd
import os
df = pd.read_csv("Datasets/NewingtonCT7-10.csv")
filtered_df = df[df['Model'].str.contains('Honda|Toyota', case=False)]
def check_dealership(miles):
    if isinstance(miles, str) and "Dealership" in miles:
        return True
    else:
        return False

# Apply the function to create a new column
filtered_df['Dealership'] = df['Miles'].astype(str).apply(check_dealership)
def clean_miles(miles):
    if isinstance(miles, str):
        # Remove 'Dealership', '·', strip any leading or trailing whitespace,
        # remove 'miles' at the end, and convert 'K' to 1000
        cleaned_miles = miles.replace('Dealership', '').replace('·', '').strip().rstrip('miles').strip()
        if 'K' in cleaned_miles:
            cleaned_miles = float(cleaned_miles.replace('K', '')) * 1000
        return int(cleaned_miles)
    else:
        return miles

# Apply the function to update the Miles column
filtered_df['Miles'] = filtered_df['Miles'].apply(clean_miles)

new_df = filtered_df[filtered_df.Miles <= 150000]
year_df = new_df[new_df.Year >= 2005]
sorted_df = year_df.sort_values(by='Year')
sorted_df['Link'] =sorted_df['Link'].apply(lambda x: f'[Link]({x})')
sorted_df.to_markdown('Datasets/Markdowns/newsorted' '.md', index=False)