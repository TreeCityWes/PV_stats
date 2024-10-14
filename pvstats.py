import requests
import csv

def get_token_info(pair_address):
    url = f"https://api.dexscreener.com/latest/dex/pairs/solana/{pair_address}"
    response = requests.get(url)
    
    # Debugging: Print status and raw response
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
    
    if response.status_code == 200:
        data = response.json()
        if data['pairs'] is not None:
            if len(data['pairs']) > 0:
                return data['pairs'][0]  # Return the first pair's data
            else:
                print("No pairs found in the response.")
                return None
        else:
            print("No data available for the provided token pair.")
            return None
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None

def write_to_csv(token_data, filename="token_info.csv"):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Token Name", "Price (USD)", "Market Cap", "Liquidity (USD)", "Base Liquidity", "Quote Liquidity"])
        
        # Writing token data to CSV
        writer.writerow([
            token_data['baseToken']['name'],
            token_data.get('priceUsd', 'N/A'),
            token_data.get('marketCap', 'N/A'),
            token_data['liquidity'].get('usd', 'N/A'),
            token_data['liquidity'].get('base', 'N/A'),
            token_data['liquidity'].get('quote', 'N/A')
        ])

# Example usage
pair_address = "89gyMPfqRZHcU9oPpQfTQLuuj98zYt1ckyf5QrxKatc7"
token_data = get_token_info(pair_address)

if token_data:
    write_to_csv(token_data)
    print("Token info written to CSV.")
else:
    print("Failed to retrieve token info.")
