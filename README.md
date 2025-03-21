# TeleNews — Real-Time News Trends & Analys from Telegram Channels 

**TeleNews** is a real-time news trend analytics system powered by streaming technologies.

For demonstration purposes, I have created Telegram channel (3-4 news per minute) where I aggregate global news from various sources using an external @AutoForwardMe bot.
This streming pipline could be effective for high-traffic news channels like crypto-signals or financial-news to extract important trends. 

IMPORTANT: Due to Telegram’s policy, bots are not allowed to scrape content from the channels unless they are administrators of those channels.

Therefore, the final user is expected to:
	•	Create their own aggregation channel.
	•	Add a third-party forwarding bot-service (@AutoForwardMe for example), to forward the messages from the channels of interest to their own channel
    where bot have admin rights.
  • Insert their own Bot API Key into .env file to connect pipeline to their personal news stream.

This way, users can tailor the incoming news to their own interests while staying compliant with Telegram’s API rules.

REQUIREMENTS:

  • Python 3.10+
  • Docker

**How to Start?**

  Clone or Download Repo
  run Docker
  Go to folder in Terminal `cd yourfilesystem/DLMDSEDE02_TeleNews`
  run Docker Compose `docker compose up --build`

TODO:
Create bash file for auto setup of containers in one click.

PLANS:

Add NLP Translation tool to autotranslate and extract info from even more channels
Integrate NLP model for extracting actionable insights from news, such as detecting key events, entities, and sentiment trends formt the newsstream. 

