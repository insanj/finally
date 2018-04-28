<p align="center">
   <img src="resources/drum.png" width=75 height=75 />
   <h3 align="center">finally</h3>
   <h4 align="center">personal music library CRM</h4>
</p>

## Usage

### Import

#### 🎵 iTunes
- File > Library > Export Library...

Take the XML file(s) and drag them into `finally/imports` directory.

#### 🎵 Spotify
- Generate an authorization token on [Spotify's developer site](https://beta.developer.spotify.com/console/get-current-user-saved-tracks/). Plug that into the "Get Current User's Saved Tracked" endpoint, `https://api.spotify.com/v1/me/tracks`.

Take the output of that response and drag it into the `imports` directory. You can do this all in one command like so (once you are in the finally directory):
```bash
curl -X "GET" "https://api.spotify.com/v1/me/tracks" -H "Accept: application/json" -H "Content-Type: application/json" -H "Authorization: Bearer <TOKEN>" >> finally/imports/spotify_library.json
```

### Run

To run finally, which will allow you to import, aggregate, and export all of your music libraries, run `python finally/finally.py` or `make`. Have fun! :drum: 


## Built with

- Python

## License

See [LICENSE](LICENSE). Please reach out to me on [🐤 Twitter](https://twitter.com/insanj) or [🚀 GitHub](https://github.com/insanj) if you'd like to use dial for something cool!
