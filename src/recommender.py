import csv
import os
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into a list of dicts with numeric fields converted."""
    # Relative paths resolve against the current directory first (e.g. running
    # `python src/main.py` from the project root), then against the project root.
    if not os.path.isabs(csv_path) and not os.path.exists(csv_path):
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csv_path = os.path.join(project_root, csv_path)

    print(f"Loading songs from {csv_path}...")

    float_fields = ("energy", "valence", "danceability", "acousticness", "tempo_bpm")
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["id"] = int(row["id"])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(row)
    return songs

GENRE_WEIGHT = 2.0
MOOD_WEIGHT = 1.5
SIMILAR_MOOD_WEIGHT = 0.75
NUMERIC_WEIGHTS = {"energy": 1.0, "valence": 0.5, "acousticness": 0.5}

# Moods that earn partial credit when the exact mood doesn't match.
SIMILAR_MOODS = {
    "chill": {"relaxed", "peaceful", "focused"},
}


def _moods_similar(a: str, b: str) -> bool:
    return b in SIMILAR_MOODS.get(a, set()) or a in SIMILAR_MOODS.get(b, set())


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences and return (score, reasons)."""
    # user_prefs keys: "genre", "mood", "energy", and optionally "valence" and
    # "acousticness" (numbers 0-1). A missing preference is not scored.
    # Maximum score with all five preferences: 5.5.
    score = 0.0
    reasons: List[str] = []

    user_genre = str(user_prefs.get("genre", "")).strip().lower()
    song_genre = str(song["genre"]).strip().lower()
    if user_genre and user_genre == song_genre:
        score += GENRE_WEIGHT
        reasons.append(f"genre match (+{GENRE_WEIGHT})")

    user_mood = str(user_prefs.get("mood", "")).strip().lower()
    song_mood = str(song["mood"]).strip().lower()
    if user_mood and user_mood == song_mood:
        score += MOOD_WEIGHT
        reasons.append(f"mood match (+{MOOD_WEIGHT})")
    elif user_mood and _moods_similar(user_mood, song_mood):
        score += SIMILAR_MOOD_WEIGHT
        reasons.append(f"similar mood (+{SIMILAR_MOOD_WEIGHT})")

    for feature, weight in NUMERIC_WEIGHTS.items():
        if user_prefs.get(feature) is None:
            continue
        closeness = 1 - abs(float(user_prefs[feature]) - float(song[feature]))
        points = weight * closeness
        score += points
        reasons.append(f"{feature} closeness (+{points:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort by score (highest first), and return the top k."""
    # Expected return format: (song_dict, score, explanation)
    if k <= 0:
        return []

    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, "; ".join(reasons)))

    # sorted() returns a new list, leaving the caller's songs untouched.
    # It is stable, so tied scores keep their catalog order.
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)
    return ranked[:k]
