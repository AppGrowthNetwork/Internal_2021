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
    client_id = "SEARCHADS.1e11ea09-3711-4728-8aac-40bf5c650ac0"
    client_secret = "eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6IjBlMjNjOTQ3LTE3ZGItNGRkMS1hMmY2LThlYjBhYmVlN2NiNyJ9.eyJzdWIiOiJTRUFSQ0hBRFMuMWUxMWVhMDktMzcxMS00NzI4LThhYWMtNDBiZjVjNjUwYWMwIiwiYXVkIjoiaHR0cHM6Ly9hcHBsZWlkLmFwcGxlLmNvbSIsImlhdCI6MTYzMzM3OTY5MSwiZXhwIjoxNjQ4OTMxNjkxLCJpc3MiOiJTRUFSQ0hBRFMuMWUxMWVhMDktMzcxMS00NzI4LThhYWMtNDBiZjVjNjUwYWMwIn0.kFNk48URupYQxtjESX1s1c0ggRvH3knYnT5MVLTlInuV4VShbyxohta5FQXlWXHmklOrGZhDjNCcS5ADiHcS9g"
    main(client_id, client_secret)