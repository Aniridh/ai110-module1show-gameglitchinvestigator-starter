import random

HYPE_GENRE_KEYWORDS = {"rock", "punk", "party"}
CHILL_TITLE_KEYWORDS = {"lofi", "ambient", "sleep"}


def normalize_song(song: dict) -> dict:
    """Trim whitespace; lowercase artist and genre for consistent comparison."""
    return {
        "title": song["title"].strip(),
        "artist": song["artist"].strip().lower(),
        "genre": song["genre"].strip().lower(),
        "energy": int(song["energy"]),
    }


def classify_song(song: dict, profile: dict) -> str:
    """
    Returns "Hype", "Chill", or "Mixed".

    Hype: energy >= hype_min_energy, OR genre == favorite_genre,
          OR genre contains a hype keyword (rock/punk/party).
    Chill: energy <= chill_max_energy, OR title contains a chill keyword
           (lofi/ambient/sleep).
    Mixed: everything else.
    Hype takes priority over Chill when both criteria are met.
    """
    genre = song["genre"].lower()
    title = song["title"].lower()
    energy = song["energy"]

    hype_min = profile.get("hype_min_energy", 7)
    chill_max = profile.get("chill_max_energy", 3)
    fav = profile.get("favorite_genre", "").strip().lower()

    is_hype = (
        energy >= hype_min
        or (fav != "" and genre == fav)
        or any(kw in genre for kw in HYPE_GENRE_KEYWORDS)
    )
    if is_hype:
        return "Hype"

    is_chill = energy <= chill_max or any(kw in title for kw in CHILL_TITLE_KEYWORDS)
    if is_chill:
        return "Chill"

    return "Mixed"


def search_songs(songs: list, query: str, field: str) -> list:
    """Case-insensitive partial match of query against the given field."""
    q = query.strip().lower()
    if not q:
        return []
    return [s for s in songs if q in str(s.get(field, "")).lower()]


def get_playlist_stats(songs: list) -> dict:
    """
    Returns:
        total     – unique song count across all playlists
        avg_energy – mean energy of all songs
        hype_ratio – percentage of songs classified as Hype
    """
    if not songs:
        return {"total": 0, "avg_energy": 0.0, "hype_ratio": 0.0}

    total = len(songs)
    avg_energy = sum(s["energy"] for s in songs) / total
    hype_count = sum(1 for s in songs if s.get("mood") == "Hype")
    hype_ratio = (hype_count / total) * 100

    return {"total": total, "avg_energy": avg_energy, "hype_ratio": hype_ratio}


def lucky_pick(songs_by_mood: dict, mode: str):
    """
    Pick a random song.
      "Hype"  → from Hype playlist only
      "Chill" → from Chill playlist only
      "Any"   → from the combined pool of Hype + Chill + Mixed
    Returns None when the target pool is empty.
    """
    if mode == "Hype":
        pool = songs_by_mood.get("Hype", [])
    elif mode == "Chill":
        pool = songs_by_mood.get("Chill", [])
    else:
        pool = (
            songs_by_mood.get("Hype", [])
            + songs_by_mood.get("Chill", [])
            + songs_by_mood.get("Mixed", [])
        )

    if not pool:
        return None
    return random.choice(pool)
