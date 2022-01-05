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
    client_id = "SEARCHADS.17f971a7-e0ca-47f9-b303-5d23ec0349ef"
    client_secret = "eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6IjUzYmM0ZDk0LTVhZWMtNDA1OS04NGNkLTY0YmY3NzQ5YTMwYyJ9.eyJzdWIiOiJTRUFSQ0hBRFMuMTdmOTcxYTctZTBjYS00N2Y5LWIzMDMtNWQyM2VjMDM0OWVmIiwiYXVkIjoiaHR0cHM6Ly9hcHBsZWlkLmFwcGxlLmNvbSIsImlhdCI6MTYyNjE0NjE3NywiZXhwIjoxNjQxNjk4MTc3LCJpc3MiOiJTRUFSQ0hBRFMuMTdmOTcxYTctZTBjYS00N2Y5LWIzMDMtNWQyM2VjMDM0OWVmIn0.ebAJY45Umo_LGTMOz6-mbZ8BIF10E9H5tlnt-qIYTEHpgorWWvp3q47Gpq0C-eBtTqd2hQgrJprt44SOspVJDg"
    main(client_id, client_secret)
