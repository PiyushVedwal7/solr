from ipywidgets import Text, Dropdown, Button, Output, VBox
import requests
import json

# Create input widgets
search_query = Text(value='', description='Search Query:')
job_type = Dropdown(description='Job Type:', options=('', 'Full-Time', 'Part-Time', 'Remote'))
location = Text(value='', description='Location:')
sort_by = Text(value='', description='Sort By:')
search_button = Button(description='Search')

# Output area for results
output = Output()

# Function to handle search button click
def on_search_clicked(b):
    output.clear_output()  # Clear previous output
    
    # Construct the Solr query
    query_string = f"title:{search_query.value} OR description:{search_query.value}"
    filter_queries = []
    
    if job_type.value:
        filter_queries.append(f"type:{job_type.value}")
    if location.value:
        filter_queries.append(f"location:{location.value}")
    
    solr_query = {
        "q": query_string,
        "fq": filter_queries,
        "sort": sort_by.value if sort_by.value else "date_posted desc"
    }
    
    # Send the request to Solr
    url = "http://localhost:8983/solr/job_search/select"
    print(f"Sending request to Solr with query: {solr_query}")  # Debugging line
    response = requests.get(url, params=solr_query)
    
    # Process and display results
    with output:
        if response.status_code == 200:
            results = response.json().get('response', {}).get('docs', [])
            if results:
                for job in results:
                    print(f"Title: {job.get('title')}\nDescription: {job.get('description')}\nLocation: {job.get('location')}\n")
            else:
                print("No results found.")
        else:
            print(f"Error: {response.status_code} - {response.text}")

# Attach the search function to the button click
search_button.on_click(on_search_clicked)

# Layout the widgets
layout = VBox([search_query, job_type, location, sort_by, search_button, output])
layout
