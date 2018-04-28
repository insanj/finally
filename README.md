<p align="center">
   <img src="drum.png" width=75 height=75 />
   <h3 align="center">finally</h3>
   <h4 align="center">personal music library CRM</h4>
</p>

## Usage

### Import

Offline and online libraries can all be integrated into finally before using it.

- iTunes: File > Library > Export Library...

Take the XML file(s) and drag them into `imports` directory.

- Spotify: Generate an authorization token on [Spotify's developer site](https://beta.developer.spotify.com/console/get-current-user-saved-tracks/). Plug that into the "Get Current User's Saved Tracked" endpoint. The URL will look like this:
```bash
curl -X "GET" "https://api.spotify.com/v1/me/tracks" -H "Accept: application/json" -H "Content-Type: application/json" -H "Authorization: Bearer <TOKEN>"
```

Take the output of that response and drag it into the `imports` directory. This is easy via command line using `> spotify_library.json`, which will redirect the contents into a newly generated JSON file.

### Run

To run finally, which will allow you to import, aggregate, and export all of your music libraries, run `python finally.py` or `make`. Have fun! :drums: 


## Built with

- Python

## License

See [LICENSE](LICENSE). Please reach out to me on [🐤 Twitter](https://twitter.com/insanj) or [🚀 GitHub](https://github.com/insanj) if you'd like to use dial for something cool!
