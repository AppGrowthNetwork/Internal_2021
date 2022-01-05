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
    client_id = "SEARCHADS.fa046fb6-3884-44b8-a9df-2c1fa5ebaf1f"
    client_secret = "eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6ImYzNTBjZGUxLTI2YTItNGViNy1iYTFjLWUyZWFjNWNmMzY0YSJ9.eyJzdWIiOiJTRUFSQ0hBRFMuZmEwNDZmYjYtMzg4NC00NGI4LWE5ZGYtMmMxZmE1ZWJhZjFmIiwiYXVkIjoiaHR0cHM6Ly9hcHBsZWlkLmFwcGxlLmNvbSIsImlhdCI6MTYzMjc5NzU0MSwiZXhwIjoxNjQ4MzQ5NTQxLCJpc3MiOiJTRUFSQ0hBRFMuZmEwNDZmYjYtMzg4NC00NGI4LWE5ZGYtMmMxZmE1ZWJhZjFmIn0.JG9z7bvXyztckqxnGExt272zkpwRzdOLHbEe9NK4WZ5s4qVth5BGBjGgf7vwaNvxzwHG9D8xDbAktGPsjxTJ0Q"
    main(client_id, client_secret)