import google_auth_oauthlib.flow 
import googleapiclient.discovery 
import googleapiclient.errors
import pickle
import flask

app = flask.Flask(__name__)

SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
creds = None

with open('token.pickle', 'rb') as token:
    creds = pickle.load(token)

with open('token.pickle', 'wb') as token:
    pickle.dump(creds, token)

def insert_commas(in_str):
    return(
        '{:,}'.format(int(in_str))
    )

def get_data(channel_id):
    data = googleapiclient.discovery.build(
        'youtube', 'v3', credentials=creds
    ).channels().list(
        part='snippet,statistics',
        id=channel_id
    ).execute()['items'][0]

    data['statistics']['subscriberCount'] = insert_commas(data['statistics']['subscriberCount'].replace('-', ''))
    data['statistics']['viewCount'] = insert_commas(data['statistics']['viewCount'].replace('-', ''))
    return(data)

pewdiepie = 'UC-lHJZR3Gqxm24_Vd_AJ5Yw'
cocomelon = 'UCbCmjCuTUZos6Inko4u57UQ'

@app.route('/')
def main():
    pewdiepie_data = get_data(pewdiepie)
    cocomelon_data = get_data(cocomelon)
    difference = {
        'subscriberCount': insert_commas(int(pewdiepie_data['statistics']['subscriberCount'].replace(',', '')) - int(cocomelon_data['statistics']['subscriberCount'].replace(',', ''))),
        'viewCount': insert_commas(int(pewdiepie_data['statistics']['viewCount'].replace(',', '')) - int(cocomelon_data['statistics']['viewCount'].replace(',', '')))
    }
    return(flask.render_template('index.html', pewdiepie=get_data(pewdiepie), cocomelon=get_data(cocomelon), difference=difference))

@app.errorhandler(404)
def page_not_found(err):
    return(flask.render_template('404.html'))