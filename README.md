# Chess Rating Discord Bot
This Discord bot is used to access chess ratings and challenge others on Lichess.org. 

The following ratings are displayed:<br>
Bullet<br>
Blitz<br>
Rapid<br>
Classical<br>
Puzzle<br>

# Commands 
# !set (Lichess user)
Allows the current member the ability to link their Lichess profile.<br>
![Shows an example use of the command](Set.png)

# !ratings (Lichess user)
Utilizes the Lichess API to access the specified users ratings, embedding the information in an organized manner.<br>
![Shows an example use of the command](Ratings.png)

# !usernames
Embeds the information of all linked profiles, displaying Discord and Lichess usernames in columns. This allows members to view other members ratings without the need of asking for a Lichess username.<br>
![Shows an example use of the command](Usernames.png)

# !challenge (variant) (initial clock time) (increment)
Requests the creation of a game with the specified parameters via the Lichess API. The open challenge link is then embedded for use.<br>
![Shows an example use of the command](Challenge.png)
