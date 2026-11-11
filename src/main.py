"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import argparse

try:
    # Works with `python -m src.main` from the project root.
    from src.recommender import load_songs, recommend_songs
except ImportError:
    # Works with `python src/main.py`.
    from recommender import load_songs, recommend_songs


WIDTH = 60

# Profiles used by `--stress` to probe the scoring logic.
STRESS_PROFILES = {
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.90},
    "Chill Lofi": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.35,
        "valence": 0.60,
        "acousticness": 0.80,
    },
    "Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.95},
    "Conflicting Preferences": {"genre": "metal", "mood": "peaceful", "energy": 0.90},
}


def print_profile(user_prefs: dict, title: str = "MUSIC RECOMMENDER") -> None:
    print("=" * WIDTH)
    print(f"  {title}".center(WIDTH))
    print("=" * WIDTH)
    print("User profile:")
    for key, value in user_prefs.items():
        print(f"  - {key:<13}: {value}")
    print()


def print_recommendations(recommendations: list) -> None:
    print(f"Top {len(recommendations)} recommendations")
    print("-" * WIDTH)
    if not recommendations:
        print("  No songs to recommend.")
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']} - {song['artist']}")
        print(f"   Genre: {song['genre']} | Mood: {song['mood']}")
        print(f"   Score: {score:.2f}")
        print("   Reasons:")
        for reason in explanation.split("; "):
            if reason:
                print(f"     * {reason}")
        print("-" * WIDTH)


def run_stress_test(songs: list) -> None:
    for number, (name, user_prefs) in enumerate(STRESS_PROFILES.items(), start=1):
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_profile(user_prefs, title=f"STRESS TEST {number}: {name}")
        print_recommendations(recommendations)
        print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Music Recommender Simulation")
    parser.add_argument(
        "--stress",
        action="store_true",
        help="run the top 5 for each stress-test profile instead of the default profile",
    )
    args = parser.parse_args()

    songs = load_songs("data/songs.csv")
    print(f"Loaded {len(songs)} songs.\n")

    if args.stress:
        run_stress_test(songs)
        return

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print_profile(user_prefs)
    print_recommendations(recommendations)


if __name__ == "__main__":
    main()
