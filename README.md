# access-scripts
Scripts for various token generation

## ASA
First of all, make sure you have generated a public and a private key for your machine. You can generate a private key first by typing:
```
openssl ecparam -genkey -name prime256v1 -noout -out private-key.pem
```
Then generate a public key:
```
openssl ec -in private-key.pem -pubout -out public-key.pem
```
You need to make sure this public key is uploaded to Apple Search Ads so it knows who you are. Otherwise use, the public key provided.
Now you can run the python script to generate a client secret. Make sure to update file with the correct client_id, team_id and key_id from the ASA site. Also make sure your KEY_FILE points to your private key.
Finally you can request an access token, either using Curl or Postman. You need to call something like this:
```
curl -X POST \
-H 'Host: appleid.apple.com' \
-H 'Content-Type: application/x-www-form-urlencoded' \
https://appleid.apple.com/auth/oauth2/token?grant_type=client_credentials&
client_id=YOUR_CLIENT_ID&client_secret=YOUR_CLIENT_SECRET&scope=searchadsorg
```
For more info on API usage: https://developer.apple.com/documentation/apple_search_ads/call_the_apple_search_ads_api
