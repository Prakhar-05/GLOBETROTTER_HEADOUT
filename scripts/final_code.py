import json
import requests
import time
import os
import re
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load environment variables from .env
load_dotenv()

# Set API key and headers for OpenAI and Unsplash
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai_headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}

# Configurable parameters
target_total = 120      # final total unique destinations required (including originals)
generation_delay = 5    # delay after each generation call (in seconds)
processing_delay = 5    # delay after processing (in seconds)
max_generation_attempts = 50 # maximum overall attempts for generating unique cities

def sanitize_json_string(s):
    """
    Sanitize the raw JSON string by extracting all complete double-quoted strings 
    and rebuilding a valid JSON array. This avoids issues with trailing or incomplete entries.
    """
    items = re.findall(r'"([^"]+)"', s)
    return json.dumps(items)

def fallback_extract_strings(s):
    """Fallback method: extract all double-quoted strings from s."""
    return re.findall(r'"([^"]+)"', s)

def generate_destination_names(count, exclude_list, retries=3):
    """
    Generate a JSON array containing 'count' famous international destination city names
    using GPT-3.5-turbo. The exclude_list is used to guide the model.
    """
    exclude_str = ", ".join(exclude_list)
    prompt = (
        f"Provide a JSON array containing {count} famous international destination city names "
        f"that are well-known around the globe. Exclude these if possible: [{exclude_str}]. "
        'Return only the city names as strings. For example: '
        '["Sydney", "Rio de Janeiro", "Cape Town", "New York City", "London", "Dubai", "Tokyo"]'
    )
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 300,
        "temperature": 0.7,
    }
    for attempt in range(retries):
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=openai_headers, json=data)
        if response.status_code == 200:
            raw_text = response.json()['choices'][0]['message']['content'].strip()
            sanitized_text = sanitize_json_string(raw_text)
            try:
                destination_names = json.loads(sanitized_text)
                if isinstance(destination_names, list) and all(isinstance(n, str) for n in destination_names):
                    return destination_names
                else:
                    print("Error: Generated output is not a valid list of strings.")
            except json.JSONDecodeError:
                print("Error: Unable to decode JSON after sanitization.")
                print("Sanitized text:", sanitized_text)
                fallback = fallback_extract_strings(sanitized_text)
                if fallback:
                    print("Using fallback extraction method.")
                    return fallback
        else:
            print(f"Error: API returned status code {response.status_code}")
            print("Response:", response.text)
        time.sleep(2)
    return []

def fix_inner_quotes(text):
    """
    Attempt to fix unescaped inner quotes in the trivia array of the JSON text.
    This function finds the content within "trivia": [...] and reprocesses each element.
    """
    match = re.search(r'"trivia":\s*\[(.*?)\]', text, flags=re.DOTALL)
    if not match:
        return text
    array_content = match.group(1)
    # Find all elements between double quotes.
    elements = re.findall(r'"(.*?)"', array_content)
    fixed_elements = []
    for elem in elements:
        # Escape any inner double quotes.
        fixed_elem = elem.replace('"', '\\"')
        fixed_elements.append(f'"{fixed_elem}"')
    fixed_array = ", ".join(fixed_elements)
    fixed_text = re.sub(r'("trivia":\s*\[).*?(\])', r'\1' + fixed_array + r'\2', text, flags=re.DOTALL)
    return fixed_text

def generate_details(destination_name, retries=3):
    """
    Generate creative clues, fun fact, trivia, and country info for a destination using GPT-3.5-turbo.
    Retries up to 'retries' times if JSON decoding fails.
    """
    prompt = (
        f"Provide details for the destination {destination_name} in the following JSON format:\n"
        'Ensure that the output is valid JSON with all inner double quotes properly escaped:\n'
        '{"city": "<city name>", "country": "<country>", "clues": ["<clue1>", "<clue2>"], '
        '"fun_fact": "<fun fact>", "trivia": ["<trivia1>", "<trivia2>"]}'
    )
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 200,
        "temperature": 0.7,
    }
    for attempt in range(retries):
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=openai_headers, json=data)
        if response.status_code == 200:
            result_text = response.json()['choices'][0]['message']['content'].strip()
            try:
                details = json.loads(result_text)
                return details
            except json.JSONDecodeError:
                print(f"Error decoding JSON for {destination_name} (attempt {attempt+1}).")
                print("Raw response:", result_text)
                # Attempt to fix inner quotes in the trivia array and try again.
                fixed_text = fix_inner_quotes(result_text)
                try:
                    details = json.loads(fixed_text)
                    return details
                except json.JSONDecodeError:
                    print(f"Failed to fix JSON for {destination_name} on attempt {attempt+1}.")
        else:
            print(f"Error: API returned status code {response.status_code} for {destination_name}.")
        time.sleep(2)
    return {
        "city": destination_name,
        "country": "",
        "clues": ["No clue available."],
        "fun_fact": "No fun fact available.",
        "trivia": ["No trivia available."]
    }

def fetch_image_url(destination_name):
    """
    Fetch an image URL for the destination using the Unsplash API.
    """
    UNSPLASH_ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY')
    url = f"https://api.unsplash.com/search/photos?query={destination_name}&per_page=1"
    unsplash_headers = {"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"}
    response = requests.get(url, headers=unsplash_headers)
    if response.status_code == 200:
        results = response.json().get('results')
        if results:
            return results[0]['urls']['regular']
    return ""

def process_destination(name):
    """
    Process a single destination: generate details and fetch its image URL.
    """
    details = generate_details(name)
    details['city'] = name
    details.setdefault('country', "")
    details['image_url'] = fetch_image_url(name)
    return details

if __name__ == '__main__':
    # Step 1: Load the original dataset (with 3 destinations)
    with open('data.json', 'r') as f:
        original_data = json.load(f)
    
    # Build a dictionary of unique cities (lowercase -> proper case) from the original data.
    unique_cities = {}
    expanded = []
    for entry in original_data:
        name = (entry.get('city') or entry.get('name') or "").strip()
        if name:
            unique_cities[name.lower()] = name
        # Enrich original entry if needed.
        if not (entry.get('clues') and entry.get('fun_fact') and entry.get('trivia') and entry.get('country')):
            details = generate_details(name)
            entry.update(details)
        if not entry.get('image_url'):
            entry['image_url'] = fetch_image_url(name)
        expanded.append(entry)
    
    print(f"Original dataset provides {len(unique_cities)} unique cities.")
    
    # Step 2: Generate additional unique city names until we have at least target_total unique names
    # or until we've made max_generation_attempts overall.
    attempts = 0
    while len(unique_cities) < target_total and attempts < max_generation_attempts:
        attempts += 1
        needed = target_total - len(unique_cities)
        print(f"\nAttempt {attempts}: Generating {needed} additional unique city names...")
        new_names = generate_destination_names(needed, list(unique_cities.keys()))
        if new_names:
            for name in new_names:
                cleaned = name.strip()
                lc = cleaned.lower()
                if cleaned and lc not in unique_cities:
                    unique_cities[lc] = cleaned
                    print(f"Accepted new city: {cleaned}")
        else:
            print("No names returned in this generation call.")
        print(f"Waiting {generation_delay} seconds after generation attempt {attempts}...")
        time.sleep(generation_delay)
    
    # If still below target_total, use fallback cities to fill in the gap.
    if len(unique_cities) < target_total:
        fallback_cities = [
            "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
            "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose",
            "Austin", "Jacksonville", "Fort Worth", "Columbus", "Charlotte",
            "San Francisco", "Indianapolis", "Seattle", "Denver", "Washington"
        ]
        for city in fallback_cities:
            if len(unique_cities) >= target_total:
                break
            if city.lower() not in unique_cities:
                unique_cities[city.lower()] = city
                print(f"Added fallback city: {city}")
    
    final_city_list = list(unique_cities.values())[:target_total]
    print(f"\nFinal list of unique city names collected ({len(final_city_list)}):")
    print(final_city_list)
    
    # Step 3: Process details for all unique cities concurrently.
    processed_destinations = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(process_destination, name): name for name in final_city_list}
        for future in as_completed(futures):
            try:
                result = future.result()
                processed_destinations.append(result)
                print(f"Processed: {result['city']}")
            except Exception as e:
                print(f"Error processing {futures[future]}: {e}")
    print(f"Waiting {processing_delay} seconds after processing...")
    time.sleep(processing_delay)
    
    final_count = len(processed_destinations)
    print(f"\nFinal dataset has {final_count} destinations (expected: {target_total}).")
    
    # Step 4: Save the final dataset to a JSON file.
    with open('expanded_dataset.json', 'w') as f:
        json.dump(processed_destinations, f, indent=2)
    
    print("Dataset expansion complete. Check 'expanded_dataset.json' for the unique destinations.")

