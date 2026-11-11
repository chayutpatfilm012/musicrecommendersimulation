# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works
Real music recommendation systems like Spotify and YouTube use listening history, user behavior, and song features to recommend music. They combine collaborative filtering and content-based filtering. My simulation will focus on content-based filtering by comparing user preferences with song attributes such as genre, mood, and energy. Each song receives a score based on how closely it matches the user's preferences. Songs with higher scores will be recommended first.

### Features Used

**Song:**
- `id` – Song ID
- `title` – Song name
- `artist` – Artist name
- `genre` – Music genre
- `mood` – Song mood
- `energy` – Energy level (0–1)
- `valence` – Positivity level (0–1)
- `acousticness` – Acoustic sound level (0–1)

**UserProfile** (`user_prefs` dictionary keys):

Required:
- `genre` – Favorite music genre
- `mood` – Preferred mood
- `energy` – Preferred energy level (0–1)

Optional (not scored if missing):
- `valence` – Preferred positivity level (0–1)
- `acousticness` – Preferred acousticness level (0–1)

**Scoring Rule:**

Score = 2 × genre_match + 1.5 × mood_match + energy_closeness + 0.5 × valence_closeness + 0.5 × acousticness_closeness

For numerical features:

Closeness = 1 − |User Preference − Song Value|

The system ranks songs by score and recommends the highest-scoring songs.

### Final Algorithm Recipe

My music recommender uses content-based filtering to compare a user's preferences with 20 songs in songs.csv.

The user profile includes genre, mood, energy, valence, and acousticness.

The scoring system uses these weights:

- Genre match: 2.0 points
- Mood match: 1.5 points (0.75 for a similar mood)
- Energy similarity: 1.0 point
- Valence similarity: 0.5 points
- Acousticness similarity: 0.5 points

For numerical features, similarity is calculated as:

`Similarity = 1 - abs(user_value - song_value)`

The maximum score is 5.5 points. The program calculates a score for each song, sorts the songs from highest to lowest score, and recommends the top 5 songs.

### Potential Biases and Limitations

The system may favor songs from the user's preferred genre because genre has the highest weight. It may also miss good songs from other genres. Using similar moods helps reduce this problem, but recommendations may still lack variety. The dataset is also small, with only 20 songs, so the available recommendations are limited.
### Recommendation Flow

Input: User Profile + songs.csv (20 songs)
          ↓
Process: Loop through each song
          ↓
Calculate Score: Genre + Mood + Energy + Valence + Acousticness
          ↓
Store each song with its score
          ↓
Ranking: Sort songs by score (highest to lowest)
          ↓
Output: Top 5 Recommended Songs

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Actual terminal output from running `python -m src.main` with the default user profile (pop, happy, energy 0.8):

```text
Loading songs from data/songs.csv...
Loaded 20 songs.

============================================================
                      MUSIC RECOMMENDER
============================================================
User profile:
  - genre        : pop
  - mood         : happy
  - energy       : 0.8

Top 5 recommendations
------------------------------------------------------------
1. Sunrise City - Neon Echo
   Genre: pop | Mood: happy
   Score: 4.48
   Reasons:
     * genre match (+2.0)
     * mood match (+1.5)
     * energy closeness (+0.98)
------------------------------------------------------------
2. Gym Hero - Max Pulse
   Genre: pop | Mood: intense
   Score: 2.87
   Reasons:
     * genre match (+2.0)
     * energy closeness (+0.87)
------------------------------------------------------------
3. Rooftop Lights - Indigo Parade
   Genre: indie pop | Mood: happy
   Score: 2.46
   Reasons:
     * mood match (+1.5)
     * energy closeness (+0.96)
------------------------------------------------------------
4. Concrete Crown - Kid Meridian
   Genre: hip hop | Mood: confident
   Score: 0.98
   Reasons:
     * energy closeness (+0.98)
------------------------------------------------------------
5. Night Drive Loop - Neon Echo
   Genre: synthwave | Mood: moody
   Score: 0.95
   Reasons:
     * energy closeness (+0.95)
------------------------------------------------------------
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Stress Test Results

To check how the scoring logic behaves for very different listeners, I ran four profiles through the unchanged recommender:

```bash
python -m src.main --stress
```

The command first prints `Loading songs from data/songs.csv...` and `Loaded 20 songs.`, then the top 5 for each profile below. The output is copied from the terminal exactly.

### 1. High-Energy Pop

```text
============================================================
                STRESS TEST 1: High-Energy Pop
============================================================
User profile:
  - genre        : pop
  - mood         : happy
  - energy       : 0.9

Top 5 recommendations
------------------------------------------------------------
1. Sunrise City - Neon Echo
   Genre: pop | Mood: happy
   Score: 4.42
   Reasons:
     * genre match (+2.0)
     * mood match (+1.5)
     * energy closeness (+0.92)
------------------------------------------------------------
2. Gym Hero - Max Pulse
   Genre: pop | Mood: intense
   Score: 2.97
   Reasons:
     * genre match (+2.0)
     * energy closeness (+0.97)
------------------------------------------------------------
3. Rooftop Lights - Indigo Parade
   Genre: indie pop | Mood: happy
   Score: 2.36
   Reasons:
     * mood match (+1.5)
     * energy closeness (+0.86)
------------------------------------------------------------
4. Storm Runner - Voltline
   Genre: rock | Mood: intense
   Score: 0.99
   Reasons:
     * energy closeness (+0.99)
------------------------------------------------------------
5. Neon Pulse - Static Bloom
   Genre: edm | Mood: energetic
   Score: 0.95
   Reasons:
     * energy closeness (+0.95)
------------------------------------------------------------
```

### 2. Chill Lofi

```text
============================================================
                  STRESS TEST 2: Chill Lofi
============================================================
User profile:
  - genre        : lofi
  - mood         : chill
  - energy       : 0.35
  - valence      : 0.6
  - acousticness : 0.8

Top 5 recommendations
------------------------------------------------------------
1. Library Rain - Paper Lanterns
   Genre: lofi | Mood: chill
   Score: 5.47
   Reasons:
     * genre match (+2.0)
     * mood match (+1.5)
     * energy closeness (+1.00)
     * valence closeness (+0.50)
     * acousticness closeness (+0.47)
------------------------------------------------------------
2. Midnight Coding - LoRoom
   Genre: lofi | Mood: chill
   Score: 5.37
   Reasons:
     * genre match (+2.0)
     * mood match (+1.5)
     * energy closeness (+0.93)
     * valence closeness (+0.48)
     * acousticness closeness (+0.45)
------------------------------------------------------------
3. Focus Flow - LoRoom
   Genre: lofi | Mood: focused
   Score: 4.69
   Reasons:
     * genre match (+2.0)
     * similar mood (+0.75)
     * energy closeness (+0.95)
     * valence closeness (+0.49)
     * acousticness closeness (+0.49)
------------------------------------------------------------
4. Spacewalk Thoughts - Orbit Bloom
   Genre: ambient | Mood: chill
   Score: 3.35
   Reasons:
     * mood match (+1.5)
     * energy closeness (+0.93)
     * valence closeness (+0.47)
     * acousticness closeness (+0.44)
------------------------------------------------------------
5. Coffee Shop Stories - Slow Stereo
   Genre: jazz | Mood: relaxed
   Score: 2.63
   Reasons:
     * similar mood (+0.75)
     * energy closeness (+0.98)
     * valence closeness (+0.45)
     * acousticness closeness (+0.46)
------------------------------------------------------------
```

### 3. Intense Rock

```text
============================================================
                 STRESS TEST 3: Intense Rock
============================================================
User profile:
  - genre        : rock
  - mood         : intense
  - energy       : 0.95

Top 5 recommendations
------------------------------------------------------------
1. Storm Runner - Voltline
   Genre: rock | Mood: intense
   Score: 4.46
   Reasons:
     * genre match (+2.0)
     * mood match (+1.5)
     * energy closeness (+0.96)
------------------------------------------------------------
2. Gym Hero - Max Pulse
   Genre: pop | Mood: intense
   Score: 2.48
   Reasons:
     * mood match (+1.5)
     * energy closeness (+0.98)
------------------------------------------------------------
3. Neon Pulse - Static Bloom
   Genre: edm | Mood: energetic
   Score: 1.00
   Reasons:
     * energy closeness (+1.00)
------------------------------------------------------------
4. Iron Tempest - Grave Sentinel
   Genre: metal | Mood: angry
   Score: 0.98
   Reasons:
     * energy closeness (+0.98)
------------------------------------------------------------
5. Sunrise City - Neon Echo
   Genre: pop | Mood: happy
   Score: 0.87
   Reasons:
     * energy closeness (+0.87)
------------------------------------------------------------
```

### 4. Conflicting Preferences

```text
============================================================
            STRESS TEST 4: Conflicting Preferences
============================================================
User profile:
  - genre        : metal
  - mood         : peaceful
  - energy       : 0.9

Top 5 recommendations
------------------------------------------------------------
1. Iron Tempest - Grave Sentinel
   Genre: metal | Mood: angry
   Score: 2.93
   Reasons:
     * genre match (+2.0)
     * energy closeness (+0.93)
------------------------------------------------------------
2. Winter Nocturne - Clara Voss
   Genre: classical | Mood: peaceful
   Score: 1.78
   Reasons:
     * mood match (+1.5)
     * energy closeness (+0.28)
------------------------------------------------------------
3. Midnight Coding - LoRoom
   Genre: lofi | Mood: chill
   Score: 1.27
   Reasons:
     * similar mood (+0.75)
     * energy closeness (+0.52)
------------------------------------------------------------
4. Library Rain - Paper Lanterns
   Genre: lofi | Mood: chill
   Score: 1.20
   Reasons:
     * similar mood (+0.75)
     * energy closeness (+0.45)
------------------------------------------------------------
5. Spacewalk Thoughts - Orbit Bloom
   Genre: ambient | Mood: chill
   Score: 1.13
   Reasons:
     * similar mood (+0.75)
     * energy closeness (+0.38)
------------------------------------------------------------
```

### What Surprised Me and Limitations

- **Genre dominance:** A genre match (+2.0) is worth more than a mood match (+1.5). For the High-Energy Pop user, *Gym Hero* (pop, **intense**) ranks above *Rooftop Lights* (indie pop, **happy**), even though Rooftop Lights fits the happy mood better. Exact matching also treats `indie pop` and `pop` as completely different genres.
- **Conflicting preferences:** For metal + peaceful + energy 0.90, ranks 2–5 are calm classical, lofi, and ambient songs with energy far below 0.90. A mood match (+1.5 or +0.75) outweighs a large energy gap, which can cost at most 1.0 point. The system cannot tell that "peaceful metal" is a contradiction, so it mixes two very different styles.
- **Limited genre diversity:** Most genres have only one song in the 20-song catalog. After *Storm Runner*, the Intense Rock list falls back to pop, edm, and metal, ranked almost entirely by energy (scores around 1.0). The Chill Lofi user gets three lofi songs in a row, while every other profile runs out of matching songs after one or two picks.
- **Missing input validation:** The scoring code does not check inputs. An empty profile gives every song 0.00, an energy outside 0–1 (for example 1.5) can produce negative closeness points, and a non-number such as `"high"` crashes with a `ValueError`. Missing valence and acousticness are skipped, so the maximum score is 4.5 for three of these profiles but 5.5 for Chill Lofi, which means scores cannot be compared across profiles.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



