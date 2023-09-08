import json
import csv

# Open the input and output files
def export_jsonl_to_csv(infile, outfile):
    with open(infile, 'r') as jsonl_file, open(outfile, 'w', newline='') as csv_file:
        # Create a CSV writer object
        csv_writer = csv.writer(csv_file)
        
        # Initialize header
        header_written = False
        
        for line in jsonl_file:
            # Parse the JSON line to get a dictionary
            data = json.loads(line)
            
            # Write header if not done already
            if not header_written:
                csv_writer.writerow(data.keys())
                header_written = True
            
            # Write the actual data
            csv_writer.writerow(data.values())

export_jsonl_to_csv("output.jsonl", "output.csv")
export_jsonl_to_csv("search_results_output.jsonl", "search_results_output.csv")