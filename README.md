# e-SoccerCoach

# Project Overview

e-SoccerCoach is an innovative project developed for the ThinkAI hackathon. It harnesses the power of generative AI to assist soccer coaches and enhance crowd attention retention during matches.

# Features

1. **AI Soccer Coach Assistant**: Utilizes generative AI to help coaches make informed decisions by providing real-time insights and recommendations.
2. **Crowd Attention Retention**: Employs AI to analyze and predict crowd behavior, aiming to improve the overall spectator experience.

# Team

This project is a collaborative effort by:

- AMZYL Mohammed Ali
- ADRANE Akram
- BELMOUSSA Abderrazak

# Data set

Our project leverages public data from the StatsBomb API to train and evaluate our AI models. This data provides a rich set of information about soccer matches, including:

> Match Events: The core of our dataset consists of detailed event data for each match. This data includes information like:
1. Event type (e.g., shot, pass, tackle)
2. Player involved (if applicable)
3. Time of the event
4. Location on the field (x, y coordinates)
5. Pressure on the player (during the event)
6. Related events (e.g., a shot might be linked to a block)
7. Match Structure: Data about the match structure is also available, including:
8. Competition and season information
9. Starting lineups and formations for each team
10. Tactical shifts made throughout the match (if any)

# Data Source:

The data is provided as JSON files exported from the StatsBomb Data API. You can find more details about the data format and event definitions in the StatsBomb documentation: https://statsbomb.com/what-we-do/hub/free-data/

# Specifics of Usage:

We primarily focused on the "events" data for our project. This data provides a granular understanding of player actions and in-game situations, allowing us to train AI models for tasks like:

## Analyzing player performance
## Identifying tactical patterns
## Predicting future events

# Data Cleaning and Compression (Decrapify)
# Data Optimization: Addressing Size and Token Limits
The raw dataset size presented challenges due to token limitations. To ensure efficient training, we performed data cleaning and JSON minification to optimize the data without compromising its integrity. This allowed us to effectively train our AI models within the framework's constraints.



# Installation and Usage

(Provide instructions on how to install and use your project here.)

# Contributing

As this is a hackathon project, we are not currently accepting contributions.

# Acknowledgements

We would like to express our gratitude to the ThinkAI hackathon organizers for giving us the opportunity to work on this exciting project.

# License

(Include any license information here.)
