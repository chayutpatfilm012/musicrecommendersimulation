# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeFinder 1.0**

---

## 2. Intended Use  

**Goal:** VibeFinder recommends songs that match a listener's taste. The listener gives a favorite genre, a mood, and an energy level from 0 (very calm) to 1 (very intense). They can also give a valence level (how happy or sad the music sounds) and an acousticness level (how acoustic or electronic it sounds). The system returns the top 5 songs, each with a score and a list of reasons.

**Intended use:** This is an educational simulation for a classroom project. It shows how a simple content-based recommender turns song features and user preferences into ranked suggestions.

**Not intended for:** It is not a real streaming service, and it should not be used to make recommendations for real users. It does not learn from listening history, likes, or skips. It assumes a listener's taste can be described by one genre, one mood, and a few numbers, which is not true for most people. It cannot predict what everyone will enjoy.

---

## 3. How the Model Works  

VibeFinder gives every song a score based on how well it matches the listener. Points are added like this:

- **Genre:** 2.0 points if the song's genre is exactly the listener's favorite genre.
- **Mood:** 1.5 points if the mood matches exactly. If it doesn't, a similar mood earns 0.75 points. Right now, "relaxed", "peaceful", and "focused" count as similar to "chill".
- **Energy:** up to 1.0 point. The closer the song's energy is to what the listener wants, the more points it gets. A perfect match gets the full point, and a very different song gets close to zero.
- **Valence:** up to 0.5 points, using the same "closer is better" rule.
- **Acousticness:** up to 0.5 points, using the same rule.

The best possible score is 5.5 points. If the listener leaves out valence or acousticness, those parts are skipped, and the best possible score becomes 4.5. After every song is scored, the songs are sorted from highest to lowest score, and the top 5 are recommended. Each recommendation shows the reasons that earned it points, such as "genre match (+2.0)".

**Changes from the starter code:** The starter version just returned the first songs in the file. I added the scoring rules above, partial credit for similar moods, optional valence and acousticness, sorting by score, readable reasons, and a stress-test mode for trying several listener profiles at once.

---

## 4. Data  

The catalog has 20 fictional songs stored in `data/songs.csv`. The first 10 songs came with the starter project, and I added 10 more to cover new genres and moods. Each song has 10 columns: id, title, artist, genre, mood, energy, tempo_bpm, valence, danceability, and acousticness. Tempo and danceability are in the file, but the scoring does not use them.

The songs cover 16 genres, including pop, lofi, rock, jazz, classical, metal, country, reggae, R&B, hip hop, folk, EDM, and blues. They also cover 14 moods, such as happy, chill, intense, peaceful, angry, and sad.

**Limitations of the data:**

- The catalog is very small. Lofi has 3 songs, pop and jazz have 2, and the other 13 genres have only 1 song each.
- Only 3 songs have medium energy (between 0.45 and 0.7), so listeners who want medium energy have few close matches.
- Two artists appear twice (LoRoom and Neon Echo), and every other artist appears once.
- The data has no lyrics, language, release year, or popularity, and it is missing many real-world genres, such as K-pop and Latin music.
- All the values were made up for this project, so they do not come from real audio analysis.

---

## 5. Strengths  

- **It clearly separates calm and intense music.** The High-Energy Pop and Chill Lofi listeners got completely different top 5 lists with no shared songs. The same was true for Chill Lofi and Intense Rock.
- **The top pick is usually a strong match.** Sunrise City for High-Energy Pop, Library Rain for Chill Lofi, and Storm Runner for Intense Rock all match the listener's genre, mood, and energy.
- **Similar moods help a little with variety.** Because "relaxed" and "focused" count as similar to "chill", Focus Flow (lofi) and Coffee Shop Stories (jazz) still made the Chill Lofi top 5.
- **The results are easy to explain.** Every recommendation lists exactly where its points came from, so it is easy to see why a song ranked where it did.

---

## 6. Limitations and Bias 

Genre gets the most points (2.0), so a song with the right genre but the wrong mood can beat a better match, like Gym Hero (pop, intense) ranking above Rooftop Lights (indie pop, happy) for a happy pop listener. This creates a filter bubble: the Chill Lofi user got three lofi songs in a row, two by the same artist, while similar calm songs from ambient and jazz were pushed lower. The catalog has only 20 songs, and 13 of its 16 genres have just one song, so a rock or metal fan gets one good match and the rest of the list is ranked mostly by energy. When I lowered the genre weight to 1.0 and raised energy to 2.0, genre bias went down, but energy became the biggest factor and very different songs like rock, edm, and pop started to rank as if they were the same.

---

## 7. Evaluation  

I tested the recommender with four very different listener profiles and looked at the top 5 songs for each. I checked whether the songs matched the listener's taste, whether the reasons made sense, and whether the list had any variety. The full results are in the "Stress Test Results" section of the README.

### Profiles Tested

| Profile | Preferences | Top 5 (score) |
|---|---|---|
| High-Energy Pop | pop, happy, energy 0.90 | Sunrise City (4.42), Gym Hero (2.97), Rooftop Lights (2.36), Storm Runner (0.99), Neon Pulse (0.95) |
| Chill Lofi | lofi, chill, energy 0.35, valence 0.60, acousticness 0.80 | Library Rain (5.47), Midnight Coding (5.37), Focus Flow (4.69), Spacewalk Thoughts (3.35), Coffee Shop Stories (2.63) |
| Intense Rock | rock, intense, energy 0.95 | Storm Runner (4.46), Gym Hero (2.48), Neon Pulse (1.00), Iron Tempest (0.98), Sunrise City (0.87) |
| Conflicting Preferences | metal, peaceful, energy 0.90 | Iron Tempest (2.93), Winter Nocturne (1.78), Midnight Coding (1.27), Library Rain (1.20), Spacewalk Thoughts (1.13) |

Chill Lofi has higher scores because it gave five preferences instead of three, so its best possible score is 5.5 instead of 4.5.

### Comparing the Profiles

**1. High-Energy Pop vs. Chill Lofi:** The two lists share no songs. Pop got loud, upbeat songs like Sunrise City, while Lofi got quiet, acoustic songs like Library Rain. This shows the system can clearly tell energetic music from calm music.

**2. High-Energy Pop vs. Intense Rock:** These lists share four songs: Sunrise City, Gym Hero, Storm Runner, and Neon Pulse. Each profile put its own genre first, so Sunrise City is #1 for Pop but only #5 for Rock, and Storm Runner is #1 for Rock but #4 for Pop. Gym Hero is #2 in both lists for different reasons: it is pop for the Pop listener and intense for the Rock listener. Because both users want high energy, the remaining spots go to the same high-energy songs.

**3. High-Energy Pop vs. Conflicting Preferences:** Both users asked for energy 0.90, but their lists share no songs. The Pop list is all high-energy music, while the Conflicting list is filled with calm "peaceful" and "chill" songs after Iron Tempest. This shows that a matching mood label can matter more than matching energy.

**4. Chill Lofi vs. Intense Rock:** These lists also share no songs. Lofi got soft songs with energy around 0.3 to 0.4, while Rock got loud songs with energy around 0.9. This is the expected result for two opposite listeners.

**5. Chill Lofi vs. Conflicting Preferences:** Three songs appear in both lists: Library Rain, Midnight Coding, and Spacewalk Thoughts. For the Lofi listener they rank #1, #2, and #4 with high scores (5.47, 5.37, 3.35). For the Conflicting listener they rank #3 to #5 with low scores (1.20 to 1.27), only because "chill" counts as similar to "peaceful". A user who asked for energy 0.90 ended up with the same quiet songs as a lofi fan.

**6. Intense Rock vs. Conflicting Preferences:** Both users want high energy, and they share only Iron Tempest. It ranks #1 for Conflicting (2.93) because it is metal, but only #4 for Rock (0.98) because it matches on energy alone. The Rock list stays loud from top to bottom, while the Conflicting list drops to calm songs after its first pick.

### What Surprised Me

- **Gym Hero ranked above Rooftop Lights for High-Energy Pop.** Gym Hero is pop but intense, and Rooftop Lights is happy but labeled "indie pop". Gym Hero scored 2.97 (2.0 for genre plus 0.97 for energy), and Rooftop Lights scored 2.36 (1.5 for mood plus 0.86 for energy). The system does not see "indie pop" as pop, so the genre points won.
- **Chill Lofi had very little variety.** The top three songs are all lofi, and two of them are by the same artist, LoRoom. The best non-lofi song, Spacewalk Thoughts (3.35), was more than a full point behind, even though it sounds very similar.
- **Low-energy songs appeared for the Conflicting profile.** Winter Nocturne ranked #2 with 1.78 even though its energy is only 0.18. It got 1.5 points for the "peaceful" mood but only 0.28 for energy. The system adds up points separately, so it cannot tell that "peaceful metal" is a contradiction.

### Tests

I ran the four profiles with `python -m src.main --stress` and checked that the default run still gave the same results. The two starter unit tests (`python -m pytest -q`) passed.

---

## 8. Future Work  

1. **Add more diverse songs.** Each genre should have at least 3 songs, and there should be more medium-energy songs. This would give every type of listener more than one good match.
2. **Improve genre and mood similarity.** Related genres like pop and indie pop, or rock and metal, should earn partial points, the same way similar moods do. Moods like intense, angry, and energetic should also be grouped together. Mood points could depend on energy too, so a "peaceful" song with very low energy would not be recommended to someone who wants intense music.
3. **Check the listener's input and add variety rules.** The system should make sure numbers stay between 0 and 1 and warn the listener if a value is missing or not a number. The top 5 could also allow at most one song per artist, so one artist cannot fill the list.

---

## 9. Personal Reflection  

My biggest learning moment was the conflicting profile test, where someone who wanted high-energy metal got calm classical and lofi songs just because "peaceful" matched, which showed me how much one weight, like 1.5 points for mood, can control the results. AI helped me write the scoring code, create 10 new songs, and run the stress tests quickly, but I still had to double-check its work, like making sure the README showed real terminal output, that the original weights were back after the experiment, and that the song names and scores in my comparisons were correct. I was surprised that such a simple algorithm, just adding up points for genre, mood, and energy, could already create a filter bubble, like the Chill Lofi list with three lofi songs and two by the same artist. The weight-shift experiment surprised me too, because lowering genre to 1.0 and raising energy to 2.0 didn't remove the bias, it just moved it from genre to energy. Next, I would add more songs for each genre, give partial points for related genres like pop and indie pop, and allow only one song per artist in the top 5. I would also check user input, so values like 1.5 or "high" can't break the scores.
