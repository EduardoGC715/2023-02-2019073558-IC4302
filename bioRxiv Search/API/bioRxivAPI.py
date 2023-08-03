import requests

def get_biorxiv_data(query=None):
    base_url = 'https://api.biorxiv.org'
    endpoint = '/covid19/0'
    headers = {'Content-Type': 'application/json'}

    # You can use the `query` parameter to filter data, for example, by subject or author.
    params = {'subject': query} if query else {}

    response = requests.get(base_url + endpoint, params=params, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None


# Example 1: Retrieve all preprints from bioRxiv
data = get_biorxiv_data()
print(data)

# Example 2: Retrieve preprints filtered by subject
subject = 'genomics'
data = get_biorxiv_data(query=subject)
print(data)
