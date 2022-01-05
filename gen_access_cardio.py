import requests


def main(client_id, client_secret):
    url = "https://appleid.apple.com/auth/oauth2/token?grant_type=client_credentials&client_id=" + client_id + "&client_secret=" + client_secret + "&scope=searchadsorg"

    payload={}
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload)

# Id status code is not 200 - something went wrong. We stop the program and show exact mistake
    if response.status_code != 200:
        raise ValueError(response.content)

# If we ger here - the status is 200 and response contains our report
# So we need to get it from JSON and ask json_normalize() to convert it to the table

    print (response.text)
    return response.text

if __name__ == "__main__":
    client_id = "SEARCHADS.74d58e63-a7f9-45a5-a98c-0f9d5f15ea6d"
    client_secret = "eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6IjQ1NzI0MjY0LTE4ZjktNDFkMC1iMjUyLTkyNDUxZGFjMWNlMCJ9.eyJzdWIiOiJTRUFSQ0hBRFMuNzRkNThlNjMtYTdmOS00NWE1LWE5OGMtMGY5ZDVmMTVlYTZkIiwiYXVkIjoiaHR0cHM6Ly9hcHBsZWlkLmFwcGxlLmNvbSIsImlhdCI6MTYzODk5MjMxMCwiZXhwIjoxNjU0NTQ0MzEwLCJpc3MiOiJTRUFSQ0hBRFMuNzRkNThlNjMtYTdmOS00NWE1LWE5OGMtMGY5ZDVmMTVlYTZkIn0.2egjSk9QL__WTyJtM8HI4SWm5WWucSAQJSHt9v8IFttfokTpkfMSozeE9rTMOgLTYSnGdTPjt-mgdbCJsM7dxA"
    main(client_id, client_secret)