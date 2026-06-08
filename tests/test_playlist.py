import pytest
from playlist_utils import (
    normalize_song,
    classify_song,
    search_songs,
    get_playlist_stats,
    lucky_pick,
)

PROFILE = {"favorite_genre": "pop", "hype_min_energy": 7, "chill_max_energy": 3}


# ── Classification ────────────────────────────────────────────────────────────

class TestClassifySong:
    def test_hype_by_energy(self):
        song = {"title": "Banger", "artist": "dj", "genre": "edm", "energy": 8}
        assert classify_song(song, PROFILE) == "Hype"

    def test_hype_at_exact_min_energy(self):
        song = {"title": "Edge", "artist": "x", "genre": "blues", "energy": 7}
        assert classify_song(song, PROFILE) == "Hype"

    def test_hype_by_favorite_genre(self):
        song = {"title": "Soft Pop", "artist": "singer", "genre": "pop", "energy": 4}
        assert classify_song(song, PROFILE) == "Hype"

    def test_hype_by_genre_keyword_rock(self):
        song = {"title": "Guitar Hero", "artist": "band", "genre": "rock", "energy": 5}
        assert classify_song(song, PROFILE) == "Hype"

    def test_hype_by_genre_keyword_punk(self):
        song = {"title": "Street", "artist": "x", "genre": "punk", "energy": 5}
        assert classify_song(song, PROFILE) == "Hype"

    def test_hype_by_genre_keyword_party(self):
        song = {"title": "Dance", "artist": "dj", "genre": "party beats", "energy": 5}
        assert classify_song(song, PROFILE) == "Hype"

    def test_hype_priority_over_chill(self):
        # genre=rock always triggers Hype even at low energy
        song = {"title": "Quiet Rock", "artist": "a", "genre": "rock", "energy": 2}
        assert classify_song(song, PROFILE) == "Hype"

    def test_chill_by_energy(self):
        song = {"title": "Soft", "artist": "a", "genre": "jazz", "energy": 2}
        assert classify_song(song, PROFILE) == "Chill"

    def test_chill_at_exact_max_energy(self):
        song = {"title": "Quiet", "artist": "a", "genre": "classical", "energy": 3}
        assert classify_song(song, PROFILE) == "Chill"

    def test_chill_by_title_keyword_lofi(self):
        song = {"title": "lofi study beats", "artist": "a", "genre": "electronic", "energy": 5}
        assert classify_song(song, PROFILE) == "Chill"

    def test_chill_by_title_keyword_ambient(self):
        song = {"title": "ambient dreams", "artist": "a", "genre": "electronic", "energy": 5}
        assert classify_song(song, PROFILE) == "Chill"

    def test_chill_by_title_keyword_sleep(self):
        song = {"title": "Sleep Well", "artist": "a", "genre": "classical", "energy": 5}
        assert classify_song(song, PROFILE) == "Chill"

    def test_mixed(self):
        song = {"title": "Neutral Track", "artist": "a", "genre": "jazz", "energy": 5}
        assert classify_song(song, PROFILE) == "Mixed"

    def test_no_favorite_genre_does_not_false_match(self):
        profile_no_fav = {"favorite_genre": "", "hype_min_energy": 7, "chill_max_energy": 3}
        song = {"title": "Track", "artist": "a", "genre": "", "energy": 5}
        assert classify_song(song, profile_no_fav) == "Mixed"


# ── Normalization ─────────────────────────────────────────────────────────────

class TestNormalizeSong:
    def test_strips_title_whitespace(self):
        s = normalize_song({"title": "  My Song  ", "artist": "x", "genre": "pop", "energy": 5})
        assert s["title"] == "My Song"

    def test_lowercases_artist(self):
        s = normalize_song({"title": "Track", "artist": "AC/DC", "genre": "Rock", "energy": 9})
        assert s["artist"] == "ac/dc"

    def test_lowercases_genre(self):
        s = normalize_song({"title": "Track", "artist": "x", "genre": "  Rock  ", "energy": 9})
        assert s["genre"] == "rock"

    def test_energy_coerced_to_int(self):
        s = normalize_song({"title": "T", "artist": "a", "genre": "g", "energy": "8"})
        assert s["energy"] == 8
        assert isinstance(s["energy"], int)


# ── Search ────────────────────────────────────────────────────────────────────

class TestSearchSongs:
    @pytest.fixture(autouse=True)
    def songs(self):
        self.songs = [
            {"title": "Thunderstruck", "artist": "ac/dc", "genre": "rock", "energy": 9},
            {"title": "Bohemian Rhapsody", "artist": "queen", "genre": "rock", "energy": 7},
            {"title": "Blue Moon", "artist": "artist3", "genre": "jazz", "energy": 4},
        ]

    def test_partial_match(self):
        results = search_songs(self.songs, "thunder", "title")
        assert len(results) == 1
        assert results[0]["title"] == "Thunderstruck"

    def test_case_insensitive(self):
        results = search_songs(self.songs, "AC", "artist")
        assert len(results) == 1
        assert results[0]["artist"] == "ac/dc"

    def test_multiple_results(self):
        results = search_songs(self.songs, "rock", "genre")
        assert len(results) == 2

    def test_no_results(self):
        assert search_songs(self.songs, "xyz", "title") == []

    def test_empty_query_returns_empty(self):
        assert search_songs(self.songs, "   ", "title") == []


# ── Stats ─────────────────────────────────────────────────────────────────────

class TestGetPlaylistStats:
    def test_empty_list(self):
        stats = get_playlist_stats([])
        assert stats["total"] == 0
        assert stats["avg_energy"] == 0.0
        assert stats["hype_ratio"] == 0.0

    def test_total_is_unique_count(self):
        songs = [
            {"title": "A", "energy": 8, "mood": "Hype"},
            {"title": "B", "energy": 2, "mood": "Chill"},
            {"title": "C", "energy": 5, "mood": "Mixed"},
        ]
        assert get_playlist_stats(songs)["total"] == 3

    def test_avg_energy(self):
        songs = [
            {"title": "A", "energy": 8, "mood": "Hype"},
            {"title": "B", "energy": 2, "mood": "Chill"},
            {"title": "C", "energy": 6, "mood": "Mixed"},
        ]
        assert get_playlist_stats(songs)["avg_energy"] == pytest.approx(16 / 3)

    def test_hype_ratio_50_percent(self):
        songs = [
            {"title": "A", "energy": 8, "mood": "Hype"},
            {"title": "B", "energy": 8, "mood": "Hype"},
            {"title": "C", "energy": 2, "mood": "Chill"},
            {"title": "D", "energy": 5, "mood": "Mixed"},
        ]
        assert get_playlist_stats(songs)["hype_ratio"] == pytest.approx(50.0)

    def test_hype_ratio_all_hype(self):
        songs = [{"title": str(i), "energy": 9, "mood": "Hype"} for i in range(4)]
        assert get_playlist_stats(songs)["hype_ratio"] == pytest.approx(100.0)

    def test_hype_ratio_no_hype(self):
        songs = [{"title": "A", "energy": 2, "mood": "Chill"}]
        assert get_playlist_stats(songs)["hype_ratio"] == pytest.approx(0.0)


# ── Lucky Pick ────────────────────────────────────────────────────────────────

class TestLuckyPick:
    @pytest.fixture(autouse=True)
    def songs_by_mood(self):
        self.sbm = {
            "Hype": [{"title": "H1", "mood": "Hype"}, {"title": "H2", "mood": "Hype"}],
            "Chill": [{"title": "C1", "mood": "Chill"}],
            "Mixed": [{"title": "M1", "mood": "Mixed"}],
        }

    def test_hype_mode_only_picks_hype(self):
        for _ in range(30):
            pick = lucky_pick(self.sbm, "Hype")
            assert pick is not None
            assert pick["mood"] == "Hype"

    def test_chill_mode_only_picks_chill(self):
        for _ in range(30):
            pick = lucky_pick(self.sbm, "Chill")
            assert pick is not None
            assert pick["mood"] == "Chill"

    def test_any_mode_returns_a_song(self):
        pick = lucky_pick(self.sbm, "Any")
        assert pick is not None

    def test_empty_hype_returns_none(self):
        sbm = {"Hype": [], "Chill": [{"title": "C1", "mood": "Chill"}], "Mixed": []}
        assert lucky_pick(sbm, "Hype") is None

    def test_empty_chill_returns_none(self):
        sbm = {"Hype": [{"title": "H1", "mood": "Hype"}], "Chill": [], "Mixed": []}
        assert lucky_pick(sbm, "Chill") is None

    def test_empty_any_returns_none(self):
        empty = {"Hype": [], "Chill": [], "Mixed": []}
        assert lucky_pick(empty, "Any") is None
