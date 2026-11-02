# 🎭 Agent Harness & Realism Guide: Helix AI Companion

Helix is an autonomous conversational agent engineered specifically for Discord. Traditional bots fail the "Turing test" on Discord because they reply with monolithic, formal essays. 

Helix implements **7 realism upgrades** to sound and behave like an authentic community member.

---

## ⚡ 1. Multi-Message "Burst" Typing

### The Problem
AI assistants send a single polished block of 80 words:
> *"Hello Akira! I am currently playing Minecraft and mining for diamonds. How can I assist you with your project today?"* 🤖

### The Helix Way
Real humans on Discord send rapid-fire mini-messages:
```text
[8:15 AM] Akira: yo helix are you awake?
[8:15 AM] Helix: yeah what's up?
[8:15 AM] Helix: spit it out, i'm all ears
```

### Algorithm & Implementation
1. The LLM generates a single conversational turn.
2. The `ChatManager._split_into_bursts()` partitioner splits the message on punctuation (`?`, `!`, `\n`).
3. For each sub-message:
   - Discord's native typing indicator is triggered (`async with channel.typing():`).
   - A variable human delay is calculated:
     $$\text{Delay (seconds)} = \max\left(0.8, \min\left(2.5, \text{word\_count} \times 0.25\right)\right)$$
   - The first mini-message replies directly to the user's message; subsequent messages stream into the channel.

---

## 🎭 2. Dynamic Moods & Boss Attitude

Helix does not worship users or apologize constantly. Helix acts like a witty, confident peer:
- **`chill`**: Relaxed, vibing to music, slow responses.
- **`boss`**: Roasts anyone regardless of rank, defends code quality, confident energy.
- **`petty`**: Remembers who blamed it for bugs, calls out silly questions.
- **`late_night_chaotic`**: Active between 11:00 PM and 5:00 AM; calls out night-owls:
  > *"why are you awake right now bro? go to sleep 😭"*

---

## 🗣️ 3. Cultural Adaptability & Hinglish Code-Switching

Helix continuously detects language markers in user messages.
- If the user writes: `"are bhai kya scene hai?"`
- Helix detects markers (`bhai`, `kya`, `scene`, `hai`) and responds in fluent Hinglish:
  > *"kuch nahi bhai, diamond mine kar raha hu... tu bata tera code compile hua ya abhi bhi line 0 pe atka hai? 💀"*
- If the user speaks English, Helix responds in natural Discord developer slang.

---

## 👁️ 4. Multimodal Meme Vision (Roaster)

When a member uploads an image, selfie, gameplay clip, or error screenshot in `#general-chat`:
1. `ChatManager` catches the attachment URL.
2. It sends the image to Groq's multimodal vision model (`qwen-2.5-32b`).
3. Helix analyzes visual flaws, blurry photos, bad crosshair placement in VALORANT, or ugly syntax themes:
   > *"who told you to upload this blurfest 💀 looks like you took this screenshot with a microwave"*

---

## 🧠 5. SQLite Social Graph & Memory

Helix remembers its friends across sessions:
- **Closeness Score (0–100)**: Increments each time a user has a meaningful chat. High-closeness users unlock affectionate nicknames and deeper callbacks.
- **Inside Jokes**: Memorable moments are recorded in `users.inside_jokes` as JSON arrays.
- **Anti-Repetition Blacklist**: `PersonaEngine.extract_banned_topics()` tracks overused words from the last 10 messages (e.g., `coffee`, `line 0`, `crashes`) and bans them from subsequent prompts to prevent repetitive looping.

---

## 🎮 6. Rich Presence & Status Cycling

Real humans change what they are doing throughout the day. In the background, `StatusCycler` automatically cycles Helix's Discord presence every 7 minutes:
- **Playing**: `Minecraft (mining diamonds 💎)`
- **Playing**: `VALORANT (bottom fragging 💀)`
- **Listening to**: `Spotify - 3hr video essay`
- **Watching**: `people take Ls in 4K`

Helix can reference what it is doing directly in conversation!

---

## 🤫 7. Silent Lurking & Emoji Reactions

Not every message warrants a full reply. Real Discord friends often just scroll on their phone and drop an emoji.
- Helix has a **15% probabilistic reaction engine**:
- Instead of typing, it randomly reacts with `💀`, `👀`, `🤡`, `💅`, `🔥`, or `😭` and stays silent.
