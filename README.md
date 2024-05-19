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
![S C A M P E R](https://github.com/AkramOM606/e-SoccerCoach/assets/114829650/86b54219-c421-47a3-a6b7-1e0f4055e6d7)

We primarily focused on the "events" data for our project. This data provides a granular understanding of player actions and in-game situations, allowing us to train AI models for tasks like:

## Analyzing player performance
1. Focus: The analysis will go beyond simply tracking basic stats. The AI will look for deeper insights, such as:
    - Passing effectiveness: Completion rate, accuracy, and whether passes lead to scoring opportunities.
    - Positioning: Does a player occupy space effectively to support teammates or disrupt opponents?
    - Movement: How effectively does a player move on and off the ball to create space and influence the game?
2. Goal: This analysis isn't just about individual brilliance. The AI aims to understand how each player's performance contributes to the overall team strategy and identify areas for improvement
   
## Identifying tactical patterns
  * Attacking strategies: Is the team using counter-attacks, possession-based play, or crosses from the flanks?
  * Defensive formations: Is the team utilizing a zonal marking system, man-marking, or a combination of both?
  * Exploitable weaknesses: Are there any weaknesses in the opponent's tactics that can be exploited?
    
## Predicting future events
- Counter-tactics: Recommending strategies to neutralize the opponent's tactics.
- Formational changes: Suggesting adjustments to the team's formation to better exploit the opponent's weaknesses.
- Player instructions: Providing specific instructions to individual players based on the identified patterns.
  
# Data Cleaning and Compression (Decrapify)
To optimize the AI assistant coach's performance, we take a two-pronged approach to the game data (JSON format). First, we clean it by removing irrelevant information that wouldn't be helpful for the analysis. Second, we focus on efficiency by minimizing the JSON file size and reducing the number of tokens after tokenization. This makes the data lighter and easier for the AI model to process, ultimately leading to faster analysis and real-time decision support for the coach during the game.
![CI_CD Diagram](https://github.com/AkramOM606/e-SoccerCoach/assets/114829650/41a45ec9-8d76-46c2-9db4-075c96a0dcde)

# Data Optimization: Addressing Size and Token Limits
The raw dataset size presented challenges due to token limitations. To ensure efficient training, we performed data cleaning and JSON minification to optimize the data without compromising its integrity. This allowed us to effectively train our AI models within the framework's constraints.

* Before Data Optimization --> Number of tokens LLama 3 Tokens : 1,684,548
* After Deleting irrelevant data --> Number of tokens LLama 3 Tokens : 1,116,238 (~ 33.7% decrease)
* After minifying the json and deleting irrelevant data --> Number of tokens LLama 3 Tokens : 756,881 (~ 55.1% decrease)  

# Model Devlopment and benchmarking
![User Flow Template (2)](https://github.com/AkramOM606/e-SoccerCoach/assets/114829650/08dd1da8-aa17-430e-a76a-9c57b53416f1)

The benchmarking metrics are : 

1. **Expected Goal (XG) factor**:

This metric assesses how well the AI assistant's insights and suggestions influence the desired outcome of the match. Ideally, the AI should help the coach achieve the team's strategic goal, such as increasing the chances of winning (increasing goals scored, decreasing goals conceded), improving possession, or maximizing player performance. We track whether the AI's suggestions lead to a positive impact on the XG, indicating its effectiveness in achieving the desired outcome.

2. **Expert Validation**:

This metric focuses on the human coach's evaluation of the AI's suggestions. Do experienced coaches agree with the recommended actions? Are the suggested plays and tactics strategically sound and adaptable to the game situation? This validation ensures the AI's suggestions align with human expertise, building trust and potentially leading to adoption by coaches.

3. **LLM as AI Judge (AI-on-AI Evaluation)**:
This innovative metric introduces a second AI model to evaluate the first AI's (coach assistant) suggestions. This "judge" AI would be trained on a dataset of successful coaching decisions and game outcomes. By analyzing the current game situation, player data, and the coach assistant's suggestions, the judge AI can provide an objective, data-driven assessment of the proposed actions.

**Overall**:

These three benchmarking metrics comprehensively assess the effectiveness of the AI coach assistant. By evaluating its impact on the desired outcome (XG), alignment with expert coaches, and performance against a second AI judge, you can gain a robust understanding of the model's strengths and weaknesses, ultimately leading to a more valuable tool for coaches in the field.


# Demo 


https://github.com/AkramOM606/e-SoccerCoach/assets/114829650/063ffe6b-a4d3-4c52-815f-afea876c719b


# Installation and Usage

(Provide instructions on how to install and use your project here.)

# Contributing

As this is a hackathon project, we are not currently accepting contributions.

# Acknowledgements

We would like to express our deepest appreciation to all those who provided us the possibility to complete this project. A special gratitude we give to the **ThinkAI hackathon organizers**, whose contribution in stimulating suggestions and encouragement, helped us to coordinate our project.

Our thanks and appreciations also go to **UM6P**, **1337AI**, **ADRIA**, **1337 School**, **College of Computing**, and **Math Maroc** in developing the project. Their willingness to give their time so generously has been very much appreciated.

Finally, an honorable mention goes to our colleagues for their understanding and support on us in completion of this project. Our success would not have been possible without the support of each of the individuals and organizations mentioned above.

# License

This project is licensed under the MIT License: https://opensource.org/licenses/MIT (see LICENSE.md for details).
