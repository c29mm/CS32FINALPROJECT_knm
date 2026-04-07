sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id="4a2e25ccb49d4a06be2008874f09a91a",
        client_secret="1e6faae316a54646937b5272da7460c8",
        redirect_uri="http://127.0.0.1:8888/callback",
        scope="user-read-private",
        open_browser=True
    )
)
