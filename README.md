## **Music Mixer**

This Python project automates the process of downloading audio from YouTube, applying audio effects (sped-up, slowed, and muffled versions), rendering corresponding video files, and uploading the results to YouTube. Currently, the project is being used on this YouTube channel: https://www.youtube.com/@zwayz228.

## **Installation** 

1. Download Python 3.12.1 .

2. Install all the necessary libraries:
   
```bash
pip install pedalboard
pip install pytube
pip install moviepy
pip install apiclient
pip install googleapiclient
pip install google_auth_oauthlib
pip install httplib2
```

3. Clone this repository:

```bash
git clone https://github.com/Thomas-Kr/music-mixer
```

4. Get Youtube API v3 keys:
- Log in to Google Developers Console.
- Create a new project.
- On the new project dashboard, click Explore & Enable APIs.
- In the library, navigate to YouTube Data API v3 under YouTube APIs.
- Enable the API.
- Create a credential.
- A screen will appear with the API key.

5. Create *client_secrets.json* and enter your data from Youtube API v3:

```json
{
    "web": {
        "client_id": "your client id",
        "client_secret": "your client secret",
        "redirect_uris": [],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://accounts.google.com/o/oauth2/token"
    }
}
```

6. Open the project's directory in the console.

7. Launch *music_mixer.py*.

## **Usage** 

1. After the script is launched, enter the link to a song you want to process.
2. Enter the name of your future video.
3. Authorize the application by opening a link given in your console.
4. Wait for video rendering and uploading on YouTube!

## **Possible Error**

```bash
pytube.exceptions.RegexMatchError: get_throttling_function_name: could not find match for multiple
```

If this error occurs:

1. Open file cipher.py.
2. In cipher.py locate these lines:
```python
r'a\.[a-zA-Z]\s*&&\s*\([a-z]\s*=\s*a\.get\("n"\)\)\s*&&.*?\|\|\s*([a-z]+)',
r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])?\([a-z]\)',
```
3. Replace the lines with these lines:
```python
r'a\.[a-zA-Z]\s*&&\s*\([a-z]\s*=\s*a\.get\("n"\)\)\s*&&.*?\|\|\s*([a-z]+)',
r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])\([a-z]\)',
```


