import re
import requests
import os
from pathlib import Path
import json

# Define constants for better maintainability
DISCOURSE_BASE_URL = "https://discourse.onlinedegree.iitm.ac.in/t/{topic_id}.json"
DISCOURSE_URL_PATTERN = r'https://discourse\.onlinedegree\.iitm\.ac\.in/t/[^/]+/(\d+)'

def fetch_missing_discourse_topics(test_suite_path: str, output_directory: str):
    """
    Parses a test suite file to find required Discourse topic URLs,
    checks if they exist locally in the output directory, and fetches
    any missing topics from the Discourse API.
    """
    print("🚀 Starting to fetch missing Discourse topics...")
    
    test_file = Path(test_suite_path)
    output_dir = Path(output_directory)
    output_dir.mkdir(exist_ok=True)

    if not test_file.exists():
        print(f"❌ Test suite file not found at {test_suite_path}")
        return

    try:
        content = test_file.read_text(encoding='utf-8')
    except Exception as e:
        print(f"❌ Error reading test file {test_suite_path}: {e}")
        return
    
    # Find all unique discourse topic IDs from the test file content
    required_topic_ids = set(re.findall(DISCOURSE_URL_PATTERN, content))
    
    if not required_topic_ids:
        print("🤷 No Discourse topic IDs found in the test suite file.")
        return

    print(f"Found {len(required_topic_ids)} unique topic IDs required by tests: {', '.join(sorted(required_topic_ids))}")

    for topic_id in required_topic_ids:
        topic_file_path = output_dir / f"topic-{topic_id}.json"
        
        if topic_file_path.exists():
            print(f"✅ Topic {topic_id} already exists locally.")
            continue

        print(f"⏳ Topic {topic_id} not found locally. Fetching...")
        topic_url = DISCOURSE_BASE_URL.format(topic_id=topic_id)
        
        try:
            response = requests.get(topic_url, timeout=15)
            response.raise_for_status()
            
            # Ensure the response is valid JSON before writing
            topic_data = response.json()

            with open(topic_file_path, 'w', encoding='utf-8') as f:
                json.dump(topic_data, f, indent=2)
            
            print(f"✅ Successfully fetched and saved topic {topic_id}.")
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching topic {topic_id} from {topic_url}: {e}")
        except json.JSONDecodeError:
            print(f"❌ Error decoding JSON for topic {topic_id}. The content from {topic_url} might not be valid JSON.")

if __name__ == "__main__":
    # Example usage: Point to the test file and the directory for raw data
    fetch_missing_discourse_topics(
        test_suite_path="test_virtual_ta_api.py", 
        output_directory="scripts/raw"
    )