import bz2
import ijson
from collections import Counter
import time
import requests

# Download the file if you haven't already. It's about 1.5GB, so it may take a while.
def download_file(url, dest_path):
    print(f"Downloading {url} to {dest_path}...")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(dest_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    print("Download complete.")

def analyze_disks(filepath):
    print(f"Opening {filepath} for streaming analysis...")
    model_counts = Counter()
    start_time = time.time()
    
    # Open the compressed file in Read Text mode
    with bz2.open(filepath, 'rt', encoding='utf-8') as f:
        # ijson.items() takes a file stream and a prefix. 
        # The prefix 'item' tells it to yield individual items inside the root array [ ... ]
        disk_stream = ijson.items(f, 'item')
        
        # Iterate through the stream one object at a time
        for count, disk in enumerate(disk_stream, 1):
            
            # Extract the model and add it to our tally
            model = disk.get('model', 'UNKNOWN')
            model_counts[model] += 1
            
            # Print a status update every 500,000 disks so we can monitor speed
            if count % 500_000 == 0:
                elapsed = time.time() - start_time
                print(f"Processed {count:,} disks... (Elapsed: {elapsed:.2f}s)")

    print(f"\nFinished parsing! Total time: {time.time() - start_time:.2f} seconds.")
    return model_counts

if __name__ == "__main__":
    url = "***REMOVED***"
    file_name = "bigf.json.bz2"
    
    # Uncomment to download if needed
    # download_file(url, file_name)
    
    counts = analyze_disks(file_name)
    
    print("\n--- FINAL RESULTS ---")
    print(f"Total Unique Models Found: {len(counts)}")
    print("-" * 30)
    
    # Print the models sorted by most common to least common
    for model, count in counts.most_common():
        print(f"Model: {model:<15} Count: {count:,}")