import requests
import base64
import pandas as pd
import time

CLIENT_ID = '*'
ALT_CLIENT_ID = '*'
CLIENT_SECRET = '*'
ALT_CLIENT_SECRET = '*'

# Base64 encode the client ID and client secret
client_credentials = f"{ALT_CLIENT_ID}:{ALT_CLIENT_SECRET}"
client_credentials_base64 = base64.b64encode(client_credentials.encode())

# Request the access token
token_url = 'https://accounts.spotify.com/api/token'
headers = {
    'Authorization': f'Basic {client_credentials_base64.decode()}'
}
data = {
    'grant_type': 'client_credentials'
}
response = requests.post(token_url, data=data, headers=headers)

if response.status_code == 200:
    access_token = response.json()['access_token']
    print("Access token obtained successfully.")
else:
    print("Error obtaining access token.")
    exit()

#Default headers
headers = {
    'Authorization': 'Bearer ' + str(access_token),
}

#Attribute lists
song_data = []
track_name = []
artists = []
album_name = []
album_id = []
track_id = []
popularity = []
release_date = []
genre = []
duration_ms = []
explicit = []
external_urls = []
danceability = []
energy = []
key = []
loudness = []
mode = []
speechiness = []
acousticness = []
instrumentalness = []
liveness = []
valence = []
tempo = []

#Top songs of Eve
response = requests.get('https://api.spotify.com/v1/artists/58oPVy7oihAEXE0Ott6JOf/top-tracks', headers=headers)
for i in response.json()['tracks']:
    song_data.append(i)
for song in song_data[0:10]:
    # print(song_data)
    response_recommended = requests.get(f"https://api.spotify.com/v1/recommendations?limit=100&seed_tracks={song['id']}", headers=headers)
    for i in response_recommended.json()['tracks']:
        song_data.append(i)
    print(len(song_data))

print(len(song_data))
# df = pd.DataFrame(song_data).drop_duplicates()
# unique_list_of_dicts = df.to_dict(orient='records')
# print(len(song_data))
check = 0
for song in song_data:
  check += 1
  if check % 100 == 0:
    time.sleep(60)
  print(check)
  ind_artist = []
  track_name.append(song['name'])
  for artist in song['artists']:
    ind_artist.append(((artist['name'], artist['id'])))
  artists.append(str(ind_artist))
  album_name.append(song['album']['name'])
  album_id.append(song['album']['id'])
  track_id.append(song['id'])
  popularity.append(song['popularity'])
  release_date.append(song['album']['release_date'])
  print(song['id'])
  response_audio = requests.get(f"https://api.spotify.com/v1/audio-features/{song['id']}", headers=headers)
  print(response_audio.text)
  duration_ms.append(response_audio.json()['duration_ms'])
  explicit.append(song['explicit'])
  external_urls.append(str(song['external_urls']))
  danceability.append(response_audio.json()['danceability'])
  energy.append(response_audio.json()['energy'])
  key.append(response_audio.json()['key'])
  loudness.append(response_audio.json()['loudness'])
  mode.append(response_audio.json()['mode'])
  speechiness.append(response_audio.json()['speechiness'])
  acousticness.append(response_audio.json()['acousticness'])
  instrumentalness.append(response_audio.json()['instrumentalness'])
  liveness.append(response_audio.json()['liveness'])
  valence.append(response_audio.json()['valence'])
  tempo.append(response_audio.json()['tempo'])

track_data = {
            'Track Name': track_name,
            'Artists': artists,
            'Album Name': album_name,
            'Album ID': album_id,
            'Track ID': track_id,
            'Popularity': popularity,
            'Release Date': release_date,
            'Duration (ms)': duration_ms,
            'Explicit': explicit,
            'External URLs': external_urls,
            'Danceability': danceability,
            'Energy': energy,
            'Key': key,
            'Loudness': loudness,
            'Mode': mode,
            'Speechiness': speechiness,
            'Acousticness': acousticness,
            'Instrumentalness': instrumentalness,
            'Liveness': liveness,
            'Valence': valence,
            'Tempo': tempo,
            # Add more attributes as needed
        }

df = pd.DataFrame(track_data)
df.to_excel('song_data.xlsx')
print(df[df.columns[0]].count())
df_no_duplicates = df.drop_duplicates(subset=['Track ID'])
df_no_duplicates.to_excel('song_data_no_duplicates.xlsx')
print(df_no_duplicates[df_no_duplicates.columns[0]].count())