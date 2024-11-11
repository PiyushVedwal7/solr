import requests
import streamlit as st

# Solr search function
def search(url, core_name, user_query, start=0, rows=10):
  
    params = {
        'q': user_query,  
        'wt': 'json',
        'rows': rows,
        'start': start
    }


    search_url = f"{url}/{core_name}/select"
    
   
    response = requests.get(search_url, params=params)

    if response.status_code == 200:
        return response.json().get('response', {}).get('docs', [])
    else:
        return []


def app():
    st.set_page_config(page_title="Job Search Engine", page_icon="🔍", layout="wide")

   
    st.title("🔍 Job Search Engine")

  
    st.markdown("""
    ### How to Use:
    - Enter a job title, keyword, or location in the search box below.
    - Examples:
        - `Software Engineer`
        - `full-time Bangalore`
        - `data scientist remote`
    - Combine keywords and filters to narrow down your search!
    """)

   
    user_query = st.text_input(
        "Search for jobs...",
        "*:*", 
        placeholder="e.g., 'Software Engineer in Bangalore'",
        help="Enter job titles, locations, or job types. Use *:* for all jobs."
    )

    
    with st.spinner('Searching for jobs...'):
        if user_query:
           
            core_name = 'job_search'  
            solr_url = 'http://localhost:8983/solr' 

       
            results = search(solr_url, core_name, user_query)

            
            if results:
                st.subheader(f"Found results for: **{user_query}**")
                
              
                for job in results:
                   
                    job_title = job.get('title', ['No title'])[0]
                    job_description = job.get('description', ['No description available'])[0]
                    job_type = job.get('type', ['No type specified'])[0]
                    job_location = job.get('location', ['No location specified'])[0]
                    job_date_posted = job.get('date_posted', ['No date specified'])[0]

                   
                    with st.container():
                        st.markdown(f"### {job_title}")
                        st.markdown(f"**Location:** {job_location} | **Type:** {job_type} | **Posted on:** {job_date_posted}")
                        
                       
                        with st.expander("Job Description"):
                            st.write(job_description)

                        
                        st.write("---")
            else:
                st.warning(f"No jobs found for '{user_query}'. Try a different query.")
                
               
                st.markdown("""
                You can try:
                - Searching with specific job titles like *"Software Engineer"*, *"Data Scientist"*, etc.
                - Using filters like *"remote"* or *"Bangalore"*.
                """)


if __name__ == "__main__":
    app()
