import zulip
import os
import csv
import json
from openai import OpenAI
with open('prompts/intro_summarize.txt', 'r') as _f:
    summarize_prompt = _f.read()
with open('prompts/intro_interests_normalize.txt', 'r') as _f:
    condense_list_prompt = _f.read()
import random

# Configuration
ZULIP_SECRET = os.environ.get('ZULIP_SECRET')
DATA_DIR = 'data'
INTROS_CSV_FILE_NAME = f'{DATA_DIR}/raw_introductions.csv'
INTROS_JSON_FILE_NAME = f'{DATA_DIR}/zulip_intros_json.json'
INTEREST_MAPPINGS_FILE = f'{DATA_DIR}/interest_mappings.json'
NETWORK_DATA_FILE = f'{DATA_DIR}/network_data.json'
MODEL = 'gpt-4o-mini'

# Data processing fields
FIELDS = ['other', 'non_technical_hobbies_and_interest', 'role_and_institution', 
          'technical_skills_and_interests', 'goals']

# Initialize clients
zulip_client = zulip.Client(api_key=ZULIP_SECRET, email='dena.mwangi@gmail.com', site='https://recurse.zulipchat.com')
openai_client = OpenAI()

# Ensure data directory exists for outputs
os.makedirs(DATA_DIR, exist_ok=True)

def get_zulip_data():
    """
    Fetch introduction messages from Recurse Center's Zulip chat.
    
    Retrieves messages from the '👋 welcome!' channel with the topic 
    'introductions for Summer 1, 2025' to collect batchmate introductions.
    
    Returns:
        dict: Zulip API response containing messages list, or empty dict on error
        
    Note:
        Requires ZULIP_SECRET environment variable to be set for authentication.
    """
    try:
        request = {
            "anchor": "newest",
            "num_before": 100,
            "num_after": 0,
            "narrow": [
                {"operator": "channel", "operand": "👋 welcome!"},
                {"operator": "topic", "operand": "introductions for Summer 1, 2025"}
            ]
        }
        result = zulip_client.get_messages(request)
        return result
    except Exception as e:
        print(f"❌ Error fetching Zulip data: {e}")
        return {"messages": []}


def save_zulip_data(data):
    """
    Save Zulip messages to CSV format for further processing.
    
    Filters messages to only include those with content longer than 600 characters
    to ensure substantial introductions, then saves as CSV with name and content columns.
    
    Args:
        data (list): List of Zulip message objects containing sender info and content
    """
    with open(INTROS_CSV_FILE_NAME, 'w', newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["name", "content"])
        for msg in data:
            name = msg["sender_full_name"]
            content = msg['content']
            if len(content) > 600:
                writer.writerow([name, content])


def save_intro_json(name, structured_intro):
    """
    Save structured introduction data to the main JSON file.
    
    Appends or updates a person's structured introduction data in the main JSON file.
    Creates the file if it doesn't exist, otherwise loads existing data and updates it.
    
    Args:
        name (str): Person's name (used as the key in the JSON structure)
        structured_intro (dict): Structured data extracted by LLM containing person's info
    """
    try:
        if os.path.exists(INTROS_JSON_FILE_NAME):
            with open(INTROS_JSON_FILE_NAME, 'r') as f:
                data = json.load(f)
        else:
            data = {}
        
        data[name] = structured_intro

        with open(INTROS_JSON_FILE_NAME, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"❌ Error saving introduction for {name}: {e}")

def process_with_llm(data, prompt, model: str = MODEL):
    """
    Process data using OpenAI's language model with error handling.
    
    Args:
        data: The input data to be processed (can be text, list, or other format)
        prompt: The system prompt/instructions for the LLM
        model (str): Optional model name to use. Defaults to global MODEL.
        
    Returns:
        str: The LLM's response as a string (typically JSON format)
        
    Note:
        If the LLM call fails, returns a default JSON structure for structured data extraction.
    """
    try:
        response = openai_client.chat.completions.create(
            model=model,
            messages=[{
                "role": "developer",
                "content": f" {prompt}"
            }, 
            {
                "role": "user",
                "content": f"Here is the info: {data}"
            }]
        )
        content = response.choices[0].message.content
        return content
    except Exception as e:
        print(f"❌ Error processing with LLM: {e}")
        # Return a default structure if LLM fails
        return '{"name": "Unknown", "technical_skills_and_interests": [], "non_technical_hobbies_and_interest": []}'
    

def get_llm_structured_output():
    """
    Process raw introduction CSV data using LLM to extract structured information.
    
    Reads the CSV file containing raw introductions and uses OpenAI's language model
    to extract structured data (name, technical skills, hobbies, goals, etc.) from
    each person's introduction text. Saves the structured data to JSON format.
    
    Note:
        Requires the raw_introductions.csv file to exist (created by save_zulip_data).
        Each introduction is processed individually and saved incrementally.
    """
    try:
        with open(INTROS_CSV_FILE_NAME, 'r') as f:
            reader = csv.reader(f)
            processed_count = 0
            for row in reader:
                if len(row) < 2:  # Skip header or malformed rows
                    continue
                    
                name, content = row[0], row[1]
                print(f"  Processing: {name}")
                
                structured_output = process_with_llm([name, content], summarize_prompt)
                
                try:
                    structured_output_json = json.loads(structured_output)
                    save_intro_json(structured_output_json.get('name', f'nameless_{random.random()}'), structured_output_json)
                    processed_count += 1
                except json.JSONDecodeError as e:
                    print(f"    ⚠️ Failed to parse LLM output for {name}: {e}")
                    continue
                    
        print(f"✅ Processed {processed_count} introductions")
    except FileNotFoundError:
        print(f"❌ CSV file {INTROS_CSV_FILE_NAME} not found. Run data fetching first.")
    except Exception as e:
        print(f"❌ Error processing introductions: {e}")

def combine_all_interests():
    """
    Collect and aggregate all unique interests from processed introductions.
    
    Scans through all processed introduction data and extracts unique interests
    from all relevant fields to create a comprehensive list for normalization.
    
    Returns:
        set: Set of unique interest strings found across all introductions
        
    Note:
        Processes all fields defined in the global 'FIELDS' constant for comprehensive coverage.
    """
    interests = set()
    try:
        with open(INTROS_JSON_FILE_NAME, 'r') as f:
            data = json.load(f)

            for _, info in data.items():
                for field in FIELDS:
                    if field in info and isinstance(info[field], list):
                        interests.update(info[field])
        
        print(f"  Found {len(interests)} unique interests")
        return interests
    except FileNotFoundError:
        print(f"❌ File {INTROS_JSON_FILE_NAME} not found")
        return set()
    except Exception as e:
        print(f"❌ Error combining interests: {e}")
        return set()

def get_llm_condensed_output():
    """
    Normalize and standardize all collected interests using LLM.
    
    Takes the raw list of interests collected from all introductions and uses the LLM
    to group similar interests into standardized categories. This creates a mapping
    from original interest terms to normalized tags for consistent relationship building.
    
    Saves the result as interest_mappings.json containing:
    - standardized_tags: List of normalized interest categories
    - mappings: Dictionary mapping original terms to standardized tags
    """
    try:
        raw_interests = combine_all_interests()
        if not raw_interests:
            print("⚠️ No interests found to normalize")
            return

        print(f"  Normalizing {len(raw_interests)} interests...")
        response = process_with_llm(raw_interests, condense_list_prompt)
        try:
            response_json = json.loads(response)
            with open(INTEREST_MAPPINGS_FILE, 'w') as f:
                json.dump(response_json, f, indent=2)
            print("✅ Interest mappings saved")
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse LLM response for interest normalization: {e}")
            
    except Exception as e:
        print(f"❌ Error normalizing interests: {e}")


def build_nodes():
    """
    Build a network graph of people and their shared interests.
    
    Creates nodes for both people and standardized interests, then finds connections
    between people who share common interests. The resulting network can be visualized
    as a graph showing how batchmates are connected through shared skills and hobbies.
    
    Generates:
    - Person nodes: Individual batchmates
    - Interest nodes: Standardized interest categories  
    - Links: Connections between people who share interests
    
    Saves the complete network data as network_data.json for visualization.
    """
    try:
        # Load interest mappings
        with open(INTEREST_MAPPINGS_FILE, 'r') as f:
            condensed_tags = json.load(f)
            standardized_tags = condensed_tags['standardized_tags']
            mappings = condensed_tags['mappings']
        
        # Load processed introductions
        with open(INTROS_JSON_FILE_NAME, 'r') as f:
            intros = json.load(f)
        
        nodes = []
        links = []
        person_to_interest = {}
        
        # Add interest nodes
        for tag in standardized_tags:
            nodes.append({'id': tag, 'type': "interest"})
        
        # Add person nodes and map their interests
        for name, info in intros.items():
            nodes.append({'id': name, 'type': 'person'})
            person_to_interest[name] = set()
            
            for field in FIELDS:
                if field in info and isinstance(info[field], list):
                    for item in info[field]:
                        normalized_interest = mappings.get(item)
                        if normalized_interest: 
                            person_to_interest[name].add(normalized_interest)
        
        # Find connections between people
        people = list(person_to_interest.keys())
        seen_pairs = set()
        connection_count = 0
        
        for i in range(len(people)):
            for j in range(i + 1, len(people)):
                person1, person2 = people[i], people[j]
                pairing = tuple(sorted([person1, person2]))
                
                if pairing in seen_pairs:
                    continue
                    
                shared_interests = person_to_interest[person1].intersection(person_to_interest[person2])
                if shared_interests:
                    links.append({
                        "source": person1,
                        "target": person2,
                        "label": ', '.join(shared_interests)
                    })
                    seen_pairs.add(pairing)
                    connection_count += 1
        
        # Save network data
        network_data = {'nodes': nodes, 'links': links}
        with open(NETWORK_DATA_FILE, 'w') as f:
            json.dump(network_data, f, indent=2)
        
        print(f"✅ Built network with {len(nodes)} nodes and {connection_count} connections")
        
    except FileNotFoundError as e:
        print(f"❌ Required file not found: {e}")
    except Exception as e:
        print(f"❌ Error building network: {e}")



def process_all_data():
    """
    Execute the complete BatchMates data processing pipeline.
    
    Orchestrates the entire workflow from raw Zulip data to network visualization:
    1. Fetches introduction messages from Zulip
    2. Saves raw data to CSV format
    3. Processes introductions with LLM to extract structured data
    4. Normalizes and standardizes all interests
    5. Builds network connections between people with shared interests
    
    Each step includes progress indicators and error handling. The pipeline
    generates multiple output files for different stages of processing.
    """
    print("🚀 Starting BatchMates data processing...")
    
    # Step 1: Fetch data from Zulip
    print("📡 Fetching data from Zulip...")
    zulip_data = get_zulip_data()
    messages = zulip_data.get('messages', [])
    if not messages:
        print("⚠️ No messages found from Zulip")
        return
    print(f"✅ Fetched {len(messages)} messages")
    
    # Step 2: Save raw data to CSV
    print("💾 Saving raw data to CSV...")
    save_zulip_data(messages)
    print("✅ Raw data saved")
    
    # Step 3: Process introductions with LLM
    print("🤖 Processing introductions with LLM...")
    get_llm_structured_output()
    print("✅ Introductions processed")
    
    # Step 4: Normalize interests
    print("🏷️ Normalizing interests...")
    get_llm_condensed_output()
    print("✅ Interests normalized")
    
    # Step 5: Build network connections
    print("🔗 Building network connections...")
    build_nodes()
    print("✅ Network connections built")
    
    print("🎉 Data processing pipeline complete!")

if __name__ == "__main__":
    # Run the complete data processing pipeline
    process_all_data()
    
    # Optional: Print summary of generated files
    print("\n📁 Generated files:")
    files_to_check = [
        INTROS_CSV_FILE_NAME,
        INTROS_JSON_FILE_NAME, 
        INTEREST_MAPPINGS_FILE,
        NETWORK_DATA_FILE
    ]
    
    for filename in files_to_check:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"  ✅ {filename} ({size} bytes)")
        else:
            print(f"  ❌ {filename} (not found)")