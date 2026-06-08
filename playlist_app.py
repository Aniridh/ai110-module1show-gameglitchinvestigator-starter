import streamlit as st
from playlist_utils import (
    normalize_song,
    classify_song,
    search_songs,
    get_playlist_stats,
    lucky_pick,
)

st.set_page_config(page_title="Mood Playlist Manager", page_icon="🎵")
st.title("🎵 Mood Playlist Manager")
st.caption("Automatically sorts your songs into Hype, Chill, and Mixed playlists.")

# ── Sidebar: user profile ────────────────────────────────────────────────────
st.sidebar.header("Your Profile")
favorite_genre = st.sidebar.text_input("Favorite Genre", value="pop")
hype_min_energy = st.sidebar.slider("Hype Min Energy", min_value=1, max_value=10, value=7)
chill_max_energy = st.sidebar.slider("Chill Max Energy", min_value=1, max_value=10, value=3)

profile = {
    "favorite_genre": favorite_genre.strip().lower(),
    "hype_min_energy": hype_min_energy,
    "chill_max_energy": chill_max_energy,
}

# ── Session state ────────────────────────────────────────────────────────────
if "songs" not in st.session_state:
    st.session_state.songs = []

# ── Add a song ───────────────────────────────────────────────────────────────
st.subheader("Add a Song")
with st.form("add_song_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        new_title = st.text_input("Title")
        new_artist = st.text_input("Artist")
    with col2:
        new_genre = st.text_input("Genre")
        new_energy = st.slider("Energy Level", min_value=1, max_value=10, value=5)
    submitted = st.form_submit_button("Add Song 🎶")

if submitted:
    if new_title.strip():
        song = normalize_song(
            {"title": new_title, "artist": new_artist, "genre": new_genre, "energy": new_energy}
        )
        song["mood"] = classify_song(song, profile)
        st.session_state.songs.append(song)
        st.success(f"Added **{song['title']}** → {song['mood']}")
    else:
        st.error("Please enter a song title.")

# Re-classify every song on each render so profile changes take effect immediately
for song in st.session_state.songs:
    song["mood"] = classify_song(song, profile)

songs_by_mood: dict = {"Hype": [], "Chill": [], "Mixed": []}
for song in st.session_state.songs:
    songs_by_mood[song["mood"]].append(song)

# ── Search ───────────────────────────────────────────────────────────────────
st.divider()
st.subheader("Search Songs")
scol1, scol2 = st.columns([1, 3])
with scol1:
    search_field = st.selectbox("Search by", ["title", "artist", "genre"])
with scol2:
    search_query = st.text_input("Search query")

if search_query.strip():
    results = search_songs(st.session_state.songs, search_query, search_field)
    if results:
        st.write(f"**{len(results)} result(s):**")
        for s in results:
            st.write(
                f"- **{s['title']}** by {s['artist']} | "
                f"genre: {s['genre']} | energy: {s['energy']} → *{s['mood']}*"
            )
    else:
        st.info("No matching songs.")

# ── Playlists ────────────────────────────────────────────────────────────────
st.divider()
st.subheader("Your Playlists")
tabs = st.tabs(["🔥 Hype", "😌 Chill", "🎲 Mixed"])
for tab, mood in zip(tabs, ["Hype", "Chill", "Mixed"]):
    with tab:
        playlist = songs_by_mood[mood]
        if playlist:
            for s in playlist:
                st.write(
                    f"**{s['title']}** — {s['artist']} | {s['genre']} | energy: {s['energy']}"
                )
        else:
            st.info(f"No {mood} songs yet.")

# ── Stats ────────────────────────────────────────────────────────────────────
st.divider()
st.subheader("Playlist Stats")
stats = get_playlist_stats(st.session_state.songs)
c1, c2, c3 = st.columns(3)
c1.metric("Total Songs", stats["total"])
c2.metric("Avg Energy", f"{stats['avg_energy']:.1f}")
c3.metric("Hype Ratio", f"{stats['hype_ratio']:.1f}%")

# ── Lucky Pick ───────────────────────────────────────────────────────────────
st.divider()
st.subheader("Lucky Pick 🎲")
pick_mode = st.selectbox("Pick from playlist", ["Any", "Hype", "Chill"])
if st.button("Lucky Pick!"):
    picked = lucky_pick(songs_by_mood, pick_mode)
    if picked:
        st.success(f"🎵 **{picked['title']}** by {picked['artist']} ({picked['mood']})")
    else:
        st.warning(f"No songs available in the **{pick_mode}** playlist.")
