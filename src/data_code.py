import requests
import pandas as pd
import time

def collect_light_novels(max_pages=5):
    all_novels = []
    base_url = "https://api.jikan.moe/v4/manga"
    
    # Loop through the page numbers
    for page in range(1, max_pages + 1):
        print(f"Requesting Page {page}...")
        
        # Set the parameters: We want light novels, and we want a specific page
        params = {
            "type": "lightnovel",
            "page": page
        }
        
        # Send the request
        response = requests.get(base_url, params=params)
        
         # Checking if seveer sucessfully responded if response.status_code == 200: then sucessfully responded and if response.status_code=404 then not found
        if response.status_code == 200:
            data = response.json()
            novels_on_page = data.get('data', []) # [] is used as a default value in case 'data' key is missing in the response, which prevents KeyError and allows the code to continue running even if the expected data is not present.
            
            # If the page is empty, we've reached the end of the database
            if not novels_on_page:
                print("End of data reached.")
                break
                
            # Extract the specific columns we want for our EDA
            for novel in novels_on_page:
                all_novels.append({
                    'MAL_ID': novel.get('mal_id'),
                    'Title': novel.get('title'),
                    'Score': novel.get('score'),
                    'Favorites': novel.get('favorites'),
                    'Synopsis': novel.get('synopsis'),
                    'Genres': ", ".join([g['name'] for g in novel.get('genres', [])]),
                    'Themes': ", ".join([t['name'] for t in novel.get('themes', [])]),
                    'Demographics': ", ".join([d['name'] for d in novel.get('demographics', [])]),
                    'Chapters': novel.get('chapters', None),
                    'Status': novel.get('status', None),
                    'Rank': novel.get('rank', None)
                })
            # pause of 2
            time.sleep(2) 
            
        else:
            print(f"Failed to retrieve page {page}. Status Code: {response.status_code}")
            break
            
    # Convert the list of dictionaries into a Pandas DataFrame
    return pd.DataFrame(all_novels)

if __name__ == "__main__":
    # Run the function (Let's start with just 5 pages to test it)
    df = collect_light_novels(max_pages=5)

    # Save the data to a CSV file so you don't have to re-download it!
    df.to_csv("light_novel_dataset2.csv", index=False)

    print(f"\nSuccessfully collected {len(df)} light novels.")
    print(df.head(3))