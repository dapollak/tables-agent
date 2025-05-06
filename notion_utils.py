import requests

def fetch_notion_titles(database_id, notion_api_key):
    """
    Fetch all title properties from a Notion database with pagination support.
    Handles the 100 item per page limit of the Notion API.
    """
    
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    
    headers = {
        "Authorization": f"Bearer {notion_api_key}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    titles = []
    has_more = True
    next_cursor = None
    page_count = 0
    
    # Loop through all API pages with pagination
    while has_more:
        # Prepare payload with pagination cursor if available
        payload = {"page_size": 100}  # Maximum allowed page size per API request
        if next_cursor:
            payload["start_cursor"] = next_cursor
            
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            page_count += 1
            
            # Extract titles from this batch of results
            for page in data["results"]:
                # Find the title property (could be named anything in Notion)
                for prop_name, prop_value in page["properties"].items():
                    if prop_value["type"] == "title" and len(prop_value["title"]) > 0:
                        title_text = "".join([text_obj["plain_text"] for text_obj in prop_value["title"]])
                        titles.append(title_text)
                        break  # Found the title property, move to next page
            
            # Check if there are more pages to fetch
            has_more = data.get("has_more", False)
            next_cursor = data.get("next_cursor")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            break
    
    print(f"Pagination complete. Retrieved {len(titles)} titles across {page_count} API pages.")
    return titles
