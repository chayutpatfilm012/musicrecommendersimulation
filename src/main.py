"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    # Works with `python -m src.main` from the project root.
    from src.recommender import load_songs, recommend_songs
except ImportError:
    # Works with `python src/main.py`.
    from recommender import load_songs, recommend_songs


WIDTH = 60


def print_profile(user_prefs: dict) -> None:
    print("=" * WIDTH)
    print("  MUSIC RECOMMENDER".center(WIDTH))
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


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded {len(songs)} songs.\n")

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print_profile(user_prefs)
    print_recommendations(recommendations)


if __name__ == "__main__":
    main()
