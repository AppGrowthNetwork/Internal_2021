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
    client_id = "SEARCHADS.a91f0c91-bde0-4cf8-99d8-9be54503c042"
    client_secret = "eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6IjA3ZTExNDhkLTMwMDUtNDg4Yy05N2NjLWRiOTI1MmRhMDQ2OSJ9.eyJzdWIiOiJTRUFSQ0hBRFMuYTkxZjBjOTEtYmRlMC00Y2Y4LTk5ZDgtOWJlNTQ1MDNjMDQyIiwiYXVkIjoiaHR0cHM6Ly9hcHBsZWlkLmFwcGxlLmNvbSIsImlhdCI6MTYzNTMxMDg5OCwiZXhwIjoxNjUwODYyODk4LCJpc3MiOiJTRUFSQ0hBRFMuYTkxZjBjOTEtYmRlMC00Y2Y4LTk5ZDgtOWJlNTQ1MDNjMDQyIn0.d5VY1q_VpDqvcatI1W63WgMGy3bLBUm3UYf-6XasOMw4mP9iIsBKGP_MQZ7Q3VX9GUJ2ZeW4kSxHi38UN5CS2A"
    main(client_id, client_secret)