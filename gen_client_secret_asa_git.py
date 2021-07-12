import jwt
import datetime as dt

client_id = 'INPUT YOUR CLIENT ID'
team_id = 'INPUT YOUR TEAM ID' 
key_id = 'INPUT YOUR KEY ID' 
audience = 'https://appleid.apple.com'
alg = 'ES256'

# Define issue timestamp.
issued_at_timestamp = int(dt.datetime.utcnow().timestamp())
# Define expiration timestamp. May not exceed 180 days from issue timestamp.
expiration_timestamp = issued_at_timestamp + 86400*180 

# Define JWT headers.
headers = dict()
headers['alg'] = alg
headers['kid'] = key_id

# Define JWT payload.
payload = dict()
payload['sub'] = client_id
payload['aud'] = audience
payload['iat'] = issued_at_timestamp
payload['exp'] = expiration_timestamp
payload['iss'] = team_id 

# Path to signed private key.
KEY_FILE = 'private-key.pem' 

with open(KEY_FILE,'r') as key_file:
     key = ''.join(key_file.readlines())

client_secret = jwt.encode(
payload=payload,  
headers=headers,
algorithm=alg,  
key=key
)

with open('client_secret.txt', 'w') as output: 
     output.write(client_secret)