## A. Text to Speech

\*\***Write your own shell file to use your favorite of these TTS engines to have your Pi greet you by name.**\*\*
(This shell file should be saved to your own repo for this lab.)

\*\***Then answer: Is the same greeting, in these different voices, the same greeting? Describe one concrete way the voice changed what the utterance seemed to mean or who seemed to be speaking.**\*\*

The same greeting did not feel exactly the same across different voices. eSpeak sounded more robotic and like a system notification, while Piper sounded more natural and personal.

## B. Speech to Text

\*\***Record a few seconds of your own speech (`arecord -d 5 -f cd -c 1 -r 16000 test.wav`) and transcribe it with at least two model sizes. Report the real-time factor for each. At what point does the accuracy improvement stop being worth the delay, for a system that has to answer you?**\*\*

tiny.en achieved an RTF of 0.22x, while base.en achieved 0.37x. Both correctly transcribed “Hello, I’m Cynthia.” Since base.en was slower without improving accuracy on this sample, I would use tiny.en for an interactive system. I also created ask_number.sh to verbally ask for a numerical input and record the user’s response.

\*\***Write your own script that verbally asks for a numerical input (a phone number, zipcode, number of pets) and records the answer the respondent provides.**\*\* Numbers are a good stress test — transcription systems make characteristic errors on digit strings, and you will want to know what they are before you design around them.

## C. Turn-taking: knowing when someone has stopped talking

\*\***Try both extremes, and something in between. Describe what each one feels like to talk to. Note specifically: at 0.2s, what kinds of normal speech get cut off? At 1.5s, what does the delay make the system seem like?**\*\*

At 0.2 seconds, the system often treated normal hesitation or short pauses as the end of my turn, so it could cut me off too early.
At 0.7 seconds, the interaction felt more natural and responsive.
At 1.5 seconds, the system waited noticeably after I stopped speaking, which made the interaction feel slower and less responsive.

## D. Storyboard

Storyboard and/or use a Verplank diagram to design a speech-enabled device. (Stuck? Make a device that talks for dogs. If that is too stupid, find an application that is better than that.)

\*\***Post your storyboard and diagram here.**\*\*
<img width="1422" height="389" alt="Okng, T sggetn" src="https://github.com/user-attachments/assets/09e3bbfc-1ef4-4856-b33a-8d9b43ddc1e9" />


Write out what you imagine the dialogue to be. Use cards, post-its, or whatever method helps you develop alternatives or group responses.

\*\***Please describe and document your process.**\*\*

I designed the dialogue to move from a broad question to more specific preferences. The assistant first asks what kind of meal the user wants, then asks about how filling the meal should be and any dietary preferences. After collecting enough information, it gives a small number of recommendations instead of overwhelming the user with too many choices. I used a silence threshold of around 0.7 seconds because it felt more natural than 0.2 seconds while still being more responsive than 1.5 seconds.

## E. Acting out the dialogue

\*\***Describe if the dialogue seemed different than what you imagined when it was acted out, and how.**\*\*

https://github.com/user-attachments/assets/bccbb266-a54c-4b81-88ae-47be06ce553c

The acted-out interaction was less predictable than my storyboard. The participant gave different answers than I expected, so the conversation did not follow the script exactly. This showed me that a voice assistant should be flexible and able to adapt to unexpected user responses.

---

# Lab 3 Part 2

For Part 2, you will redesign the interaction with the speech-enabled device using the data collected, as well as feedback from part 1.

## Prep for Part 2

1. What are concrete things that could use improvement in the design of your device? For example: wording, timing, anticipation of misunderstandings.
2. What are other modes of interaction *beyond speech* that you might also use to clarify how to interact? In particular: how does someone know when the device is listening, and when it is thinking? You have a screen and an LED.
3. Make a new storyboard, diagram and/or script based on these reflections.
4. (optional) Integrate [input devices](inputs.md) in the system

## Prototype your system

The system should:
* use the Raspberry Pi
* use one or more sensors
* require participants to speak to it

*Document how the system works.*

*Include videos or screencaptures of both the system and the controller.*

## Test the system

Try to get at least two people to interact with your system. (Ideally, you would inform them that there is a wizard *after* the interaction, but we recognize that can be hard.)

Answer the following:

### What worked well about the system and what didn't?
\*\**your answer here*\*\*

### What worked well about the controller and what didn't?
\*\**your answer here*\*\*

### What lessons can you take away from the WoZ interactions for designing a more autonomous version of the system?
\*\**your answer here*\*\*

### How could you use your system to create a dataset of interaction? What other sensing modalities would make sense to capture?
\*\**your answer here*\*\*

<details>
  <summary><strong>Submission Cleanup Reminder (Click to Expand)</strong></summary>

  **Before submitting your README.md:**
  - This readme.md file has a lot of extra text for guidance.
  - Remove all instructional text and example prompts from this file.
  - You may either delete these sections or use the toggle/hide feature in VS Code to collapse them for a cleaner look.
  - Your final submission should be neat, focused on your own work, and easy to read for grading.
</details>
