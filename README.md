<p align="center">
   <img src="finally/static/drum.png" width=75 height=75 />
   <h3 align="center">finally</h3>
   <h4 align="center">personal music library CRM</h4>
</p>

<h2>Usage</h2>

<p align="center">
   <img src="/example1.png" width=45% height=auto />
   <img src="/example2.png" width=45% height=auto >
</p>

<h3>Import</h3>

<h4>🎵 iTunes</h4>
<ul>
   <li>File > Library > Export Library...</li>
</ul>

Take the XML file(s) and drag them into <pre>finally/imports</pre> directory.

<h4>🎵 Spotify</h4>
<ul>
   <li>Generate an authorization token on <a href="https://beta.developer.spotify.com/console/get-current-user-saved-tracks/">Spotify's developer site</a>. Plug that into the "Get Current User's Saved Tracked" endpoint, <pre>https://api.spotify.com/v1/me/tracks</pre>.</li>
</ul>

Take the output of that response and drag it into the `imports` directory. You can do this all in one command like so (once you are in the finally directory):
```bash
curl -X "GET" "https://api.spotify.com/v1/me/tracks" -H "Accept: application/json" -H "Content-Type: application/json" -H "Authorization: Bearer <TOKEN>" >> finally/imports/spotify_library.json
```

<h3>Run</h3>

To run finally, which will allow you to import, aggregate, and export all of your music libraries...

<ul>
   <li><pre>python finally/finally_flask.py</pre></li>
   <li>or <pre>make</pre></li>
</ul>

You may need to install the dependencies at <pre>make deps</pre>. Have fun! :drum: 

<h2>Built with</h2>

<ul>
   <li><a href="https://github.com/python/cpython">python/cpython</a></li>
   <li><a href="https://github.com/pallets/flask">pallets/flask</a></li>
   <li><a href="https://github.com/jquery/jquery">jquery/jquery</a></li>
   <li><a href="https://github.com/olifolkerd/tabulator">olifolkerd/tabulator</a></li>
   <li><a href="https://github.com/ishikawa/python-plist-parser">ishikawa/python-plist-parser</a></li>
   <li><a href="https://gist.github.com/seanh/93666">https://gist.github.com/seanh/93666</a></li>
</ul>

<h2>License</h2>

See <a href="LICENSE">LICENSE</a>. Please reach out to me on <a href="https://twitter.com/insanj">🐤 Twitter</a> or <a href="https://github.com/insanj">🚀 GitHub</a> if you'd like to use dial for something cool!
