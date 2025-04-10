# TeleNews — Real-Time News Trends Analysis from Telegram Channels 

**TeleNews** is a real-time news trend analytics system powered by streaming technologies.

For demonstration purposes, I have created Telegram channel (3-4 news per minute) where I aggregate global news from various sources using an external @AutoForwardMe bot.
This streming pipline could be effective for high-traffic news channels like crypto-signals or financial-news to extract important trends. 

IMPORTANT: Due to Telegram’s policy, bots are not allowed to scrape content from the channels unless they are administrators of those channels.

Therefore, the final user is expected to:\
	•	Create their own aggregation channel.\
	•	Add a third-party forwarding bot-service (@AutoForwardMe for example), to forward the messages from the channels of interest to their own channel
    where bot have admin rights.\
  • Insert their own Bot API Key into .env file to connect pipeline to their personal news stream.

This way, users can tailor the incoming news to their own interests while staying compliant with Telegram’s API rules.

UPDATE 1.01: Added filter to ignore href/https links to appear in WordCloud

REQUIREMENTS:

  • Python 3.10+\
  • Docker

**How to Start?**

  Clone or Download Repo\
  run Docker\
  Go to folder in Terminal `cd yourfilesystem/DLMDSEDE02_TeleNews`\
  run Docker Compose `docker compose up --build`\
  Open `http://localhost:3000` to access Grafana Dashboard\

  OR 
  run run.sh file for auto-init:\
  `chmod +x run.sh`\
  `./run.sh`

  !!! Please refresh appeared browser window, Grafana might take some time to load !!!\
  

You should be able to see 3 Panels with various data: WordCloud, Frequency Chart, NewsFeed

![Example of Panel (WordCloud)](https://github.com/DarkhanTurtayev/DLMDSEDE02_TeleNews/blob/main/Images/WordCloudExample.png)

**Default Access** 

	• Grafana: http://localhost:3000
	• Username: admin
	• Password: admin
	• PostgreSQL: http://localhost:5432
	• Database: spark_db
	• Username: admin
	• Password: admin


PLANS:

Add NLP Translation tool to autotranslate and extract info from even more channels\
Integrate NLP model for extracting actionable insights from news, such as detecting key events, entities, and sentiment trends formt the newsstream. 

