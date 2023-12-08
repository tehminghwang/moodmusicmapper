Below are the code segments used for the GPT Fine-tuning and are python API calls to OpenAI. 
These are submitted in the Github repo for reference; API key has been removed for security reasons.

import csv
import json

def clean_csv(input_csv_path, cleaned_csv_path):
    with open(input_csv_path, 'r', encoding='ISO-8859-15', errors='replace') as infile, \
         open(cleaned_csv_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            outfile.write(line.replace('\x00', ''))


def csv_to_json(cleaned_csv_path, json_file_path):
    with open(cleaned_csv_path, mode='r', encoding='utf-8') as csvfile, \
         open(json_file_path, mode='w', encoding='utf-8') as jsonfile:
         csvreader = csv.DictReader(csvfile)

         for row in csvreader:
            # Create a list of message objects for each row
            messages = [
                {"role": row["role1"], "content": row["content1"]},
                {"role": row["role2"], "content": row["content2"]},
                {"role": row["role3"], "content": row["content3"]}
            ]
            data = {"messages": messages}

            # Write each group of messages as a separate line in the JSON file
            json.dump(data, jsonfile)
            jsonfile.write("\n")  # Add a newline after each JSON object


if __name__ == "__main__":
    original_csv_path = 'data/Book1.csv'  # Replace with your original CSV file path
    cleaned_csv_path = 'data/newfile.csv'  # Path for the cleaned CSV file
    json_file_path = 'data/trainings.json'  # Replace with your desired JSON file path

    clean_csv(original_csv_path, cleaned_csv_path)
    csv_to_json(cleaned_csv_path, json_file_path)




from openai import OpenAI

open_ai_key = "XX"

client = OpenAI(
  api_key = open_ai_key
)

try:
    with open("data/trainings.json", "rb") as file:
        response = client.files.create(file=file, purpose="fine-tune")
        print(response)  # This will print the response from the API
except Exception as e:
    print("An error occurred:", e)
)



FileObject(id='file-Q8zIKN9g0yjeOu2YjmKbYEm0', bytes=17896, created_at=1701447170, filename='trainings.json', object='file', purpose='fine-tune', status='processed', status_details=None)




from openai import OpenAI

open_ai_key = "XX"

client = OpenAI(
  api_key = open_ai_key
)

try:
    response = client.fine_tuning.jobs.create(
        training_file="file-Q8zIKN9g0yjeOu2YjmKbYEm0",
        model="gpt-3.5-turbo"
    )
    print(response)  # This will print the response from the API
except Exception as e:
    print("An error occurred:", e)


FineTuningJob(id='ftjob-fleKSpQCbZyvqCJpXJ8ilU7T', created_at=1701447416, error=None, fine_tuned_model=None, finished_at=None, hyperparameters=Hyperparameters(n_epochs='auto', batch_size='auto', learning_rate_multiplier='auto'), model='gpt-3.5-turbo-0613', object='fine_tuning.job', organization_id='org-1gHuUe4SMTUG6aFFAeNWgMrd', result_files=[], status='validating_files', trained_tokens=None, training_file='file-Q8zIKN9g0yjeOu2YjmKbYEm0', validation_file=None)



curl https://api.openai.com/v1/fine_tuning/jobs/ftjob-fleKSpQCbZyvqCJpXJ8ilU7T \
  -H "Authorization: Bearer XX"


{
  "object": "fine_tuning.job",
  "id": "ftjob-fleKSpQCbZyvqCJpXJ8ilU7T",
  "model": "gpt-3.5-turbo-0613",
  "created_at": 1701447416,
  "finished_at": 1701447787,
  "fine_tuned_model": "ft:gpt-3.5-turbo-0613:personal::8R0aC6w3",
  "organization_id": "org-1gHuUe4SMTUG6aFFAeNWgMrd",
  "result_files": [
    "file-u6y3uRHVBO1LAVjjeMvITJz2"
  ],
  "status": "succeeded",
  "validation_file": null,
  "training_file": "file-Q8zIKN9g0yjeOu2YjmKbYEm0",
  "hyperparameters": {
    "n_epochs": 6,
    "batch_size": 1,
    "learning_rate_multiplier": 2
  },
  "trained_tokens": 26838,
  "error": null



from openai import OpenAI

open_ai_key = "XX"

client = OpenAI(
  api_key = open_ai_key
)

response = client.chat.completions.create(
  model="ft:gpt-3.5-turbo-0613:personal::8R0aC6w3",
  messages=[
    {"role": "system", "content": "Assistant to recommend valency(songs with high valence sound more positive e.g. Happy, cheerful, euphoric)(0.0 to 1.0), energy(energetic tracks feel fast, loud, and noisy)(0.0 to 1.0), danceability(suitable for dancing based on musical elements including tempo, rhythm stability, beat strength)(0.0 to 1.0) and 3 recommended songs that resonates with a description of user's narrative of their sentiment, mood, context, description, feelings, or events."},
    {"role": "user", "content": "i feel energetic now"}
  ]
)

if response.choices:
    print(response.choices[0].message)
else:
    print("No response generated.")





Assistant to recommend valency(songs with high valence sound more positive e.g. Happy, cheerful, euphoric)(0.0 to 1.0), energy(energetic tracks feel fast, loud, and noisy)(0.0 to 1.0), danceability(suitable for dancing based on musical elements including tempo, rhythm stability, beat strength)(0.0 to 1.0) and 3 recommended songs that resonates with a description of user's narrative of their sentiment, mood, context, description, feelings, or events.



NEW TRAINING

FileObject(id='file-hJzazmRfqdPFY544VdasMRa6', bytes=14626, created_at=1701684299, filename='trainings2.json', object='file', purpose='fine-tune', status='processed', status_details=None)

FineTuningJob(id='ftjob-iPENCeRp1JwVK67YjTx7BXDn', created_at=1701684449, error=None, fine_tuned_model=None, finished_at=None, hyperparameters=Hyperparameters(n_epochs='auto', batch_size='auto', learning_rate_multiplier='auto'), model='gpt-3.5-turbo-0613', object='fine_tuning.job', organization_id='org-1gHuUe4SMTUG6aFFAeNWgMrd', result_files=[], status='validating_files', trained_tokens=None, training_file='file-hJzazmRfqdPFY544VdasMRa6', validation_file=None)

curl https://api.openai.com/v1/fine_tuning/jobs/ftjob-iPENCeRp1JwVK67YjTx7BXDn \
  -H "Authorization: Bearer XX"

{
  "object": "fine_tuning.job",
  "id": "ftjob-iPENCeRp1JwVK67YjTx7BXDn",
  "model": "gpt-3.5-turbo-0613",
  "created_at": 1701684449,
  "finished_at": 1701684803,
  "fine_tuned_model": "ft:gpt-3.5-turbo-0613:personal::8S0F2gyx",
  "organization_id": "org-1gHuUe4SMTUG6aFFAeNWgMrd",
  "result_files": [
    "file-039gu9QJJGEfUK1bq0EDD5Ru"
  ],
  "status": "succeeded",
  "validation_file": null,
  "training_file": "file-hJzazmRfqdPFY544VdasMRa6",
  "hyperparameters": {
    "n_epochs": 9,
    "batch_size": 1,
    "learning_rate_multiplier": 2
  },
  "trained_tokens": 35262,
  "error": null

from openai import OpenAI

open_ai_key = "XX"

client = OpenAI(
  api_key = open_ai_key
)

response = client.chat.completions.create(
  model="ft:gpt-3.5-turbo-0613:personal::8S0F2gyx",
  messages=[
    {"role": "system", "content": "Assistant to recommend valency(songs with high valence sound more positive e.g. Happy, cheerful, euphoric)(0.0 to 1.0), energy(energetic tracks feel fast, loud, and noisy)(0.0 to 1.0), danceability(suitable for dancing based on musical elements including tempo, rhythm stability, beat strength)(0.0 to 1.0) and 3 recommended songs that resonates with a description of user's narrative of their sentiment, mood, context, description, feelings, or events."},
    {"role": "user", "content": "Christmas is coming"}
  ]
)

if response.choices:
    print(response.choices[0].message)
else:
    print("No response generated.")



//sample of training datasets - these datasets will be converted to JSON via the above code

[Valency: 0.4] [Danceability: 0.6] [Energy: 0.8] [Mood: euphoric] [Genre: Power pop] [Song1: Cut to the Feeling] [Singer1: Carly Rae Jepsen] [Song2: On The Floor] [Singer2: Jennifer Lopez ft. Pitbull] [Song3: Shake It Off] [Singer3: Taylor Swift]
I had a dream, or was it real? We crossed the line and it was on. We crossed the line, it was on this time. I've been denying how I feel, you've been denying what you want. You want from me, talk to me, baby. I want some satisfaction, take me to the stars. Just like ah-ah-ah, ah-ah-ah. I wanna cut through the clouds, break the ceiling. I wanna dance on the roof, you and me alone. I wanna cut to the feeling, oh yeah. I wanna cut to the feeling, oh yeah (woo). I wanna play where you play with the angels. I wanna wake up with you all in tangles. 


27tNWlhdAryQY04Gb2ZhUI
[Valency: 0.4] [Danceability: 0.7] [Energy: 0.8] [Mood: empowering] [Genre: Power pop] [Song1: Roar] [Singer1: Katy Perry] [Song2: Fight Song] [Singer2: Rachel Platten] [Song3: Brave] [Singer3: Sara Bareilles]
I used to bite my tongue and hold my breath. Scared to rock the boat and make a mess. So I sat quietly, agreed politely. I guess that I forgot I had a choice. I let you push me past the breaking point. I stood for nothing, so I fell for everything. You held me down, but I got up (hey). Already brushing off the dust. You hear my voice, you hear that sound. Like thunder, gonna shake the ground. You held me down, but I got up (hey). Get ready 'cause I've had enough. I see it all, I see it now


60nZcImufyMA1MKQY3dcCH
[Valency: 1] [Danceability: 0.6] [Energy: 0.8] [Mood: joyful] [Genre: Pop] [Song1: Happy] [Singer1: Pharrell Williams] [Song2: Can't Stop The Feeling!] [Singer2: Justin Timberlake] [Song3: Uptown Funk] [Singer3: Mark Ronson ft. Bruno Mars]
It might seem crazy what I'm 'bout to say. Sunshine she's here, you can take a break. I'm a hot air balloon that could go to space. With the air, like I don't care baby by the way. Huh, because I'm happy. Clap along if you feel like a room without a roof. Because I'm happy. Clap along if you feel like happiness is the truth. Because I'm happy. Clap along if you know what happiness is to you. Because I'm happy. Clap along if you feel like that's what you wanna do


3bNv3VuUOKgrf5hu3YcuRo
[Valency: 0.3] [Danceability: 0.5] [Energy: 0.3] [Mood: emotional] [Genre: Pop] [Song1: Someone Like You] [Singer1: Adele] [Song2: When We Were Young] [Singer2: Adele] [Song3: Stay] [Singer3: Rihanna ft. Mikky Ekko]
I heard, that you're settled down. That you found a girl and you're, married now. I heard, that your dreams came true. Guess she gave you things. I didn't give to you. Old friend, why are you so shy. Ain't like you to hold back. Or hide from the light. I hate to turn up out of the blue uninvited but I. Couldn't stay away I couldn't fight it. I had hoped you'd see my face. And that you be reminded that for me it isn't over


1v7L65Lzy0j0vdpRjJewt1
[Valency: 0] [Danceability: 0.7] [Energy: 0.7] [Mood: intense] [Genre: Power pop] [Song1: Lose Yourself] [Singer1: Eminem] [Song2: Till I Collapse] [Singer2: Eminem ft. Nate Dogg] [Song3: Remember the Name] [Singer3: Fort Minor]
His palms are sweaty, knees weak, arms are heavy. There's vomit on his sweater already, mom's spaghetti. He's nervous, but on the surface he looks calm and ready to drops bombs, but he keeps on forgetting. what he wrote down, the whole crowd goes so loud. He opens his mouth but the words won't come out. He's chokin, how? Everybody's jokin now. The clock's run out, time's up, over - BLAOW! Snap back to reality, OHH! there goes gravity. OHH! there goes Rabbit, he choked. He's so mad, but he won't. Give up that easy nope, he won't have it. He knows, his whole back's to these ropes. It don't matter, he's dope. He knows that, but he's broke. He's so sad that he knows. when he goes back to this mobile home, that's when it's back to the lab again, yo, this whole rap shift. He better go capture this moment and hope it don't pass him


7qiZfU4dY1lWllzX7mPBI3
[Valency: 0.9] [Danceability: 0.8] [Energy: 0.7] [Mood: romantic] [Genre: Power pop] [Song1: Shape of You] [Singer1: Ed Sheeran] [Song2: Attention] [Singer2: Charlie Puth] [Song3: Senorita] [Singer3: Shawn Mendes and Camila Cabello]
The club isn't the best place to find a lover. So the bar is where I go (mmmm). Me and my friends at the table doing shots. Drinking fast and then we talk slow (mmmm). And you come over and start up a conversation with just me. And trust me I'll give it a chance now (mmmm). Take my hand, stop, put Van The Man on the jukebox. And then we start to dance. And now I'm singing like. Girl, you know I want your love. Your love was handmade for somebody like me. Come on now, follow my lead. I may be crazy, don't mind me. Say, boy, let's not talk too much. Grab on my waist and put that body on me. Come on now, follow my lead. Come, come on now, follow my lead (mmmm)


4u7EnebtmKWzUH433cf5Qv
[Valency: 0.2] [Danceability: 0.4] [Energy: 0.4] [Mood: dramatic] [Genre: Progressive Rock] [Song1: Bohemian Rhapsody] [Singer1: Queen] [Song2: Stairway to Heaven] [Singer2: Led Zeppelin] [Song3: Paradise by the Dashboard Light] [Singer3: Meat Loaf]
Is this the real life? Is this just fantasy? Caught in a landslide, no escape from reality. Open your eyes, look up to the skies and see. I'm just a poor boy, I need no sympathy. Because I'm easy come, easy go, little high, little low. Any way the wind blows doesn't really matter to me, to me. Mama, just killed a man. Put a gun against his head, pulled my trigger, now he's dead. Mama, life had just begun. But now I've gone and thrown it all away. Mama, ooh, didn't mean to make you cry. If I'm not back again this time tomorrow. Carry on, carry on as if nothing really matters


1mea3bSkSGXuIRvnydlB5b
[Valency: 0.4] [Danceability: 0.5] [Energy: 0.6] [Mood: introspective] [Genre: Alternative Rock] [Song1: Viva La Vida] [Singer1: Coldplay] [Song2: Bittersweet Symphony] [Singer2: The Verve] [Song3: Yellow] [Singer3: Coldplay]
I used to rule the world. Seas would rise when I gave the word. Now in the morning I sleep alone. Sweep the streets I used to own. I used to roll the dice. Feel the fear in my enemy’s eyes. Listened as the crowd would sing. Now the old king is dead long live the king. One minute I held the key. Next the walls were closed on me. And I discovered that my castles stand. Upon pillars of salt and pillars of sand


2Fxmhks0bxGSBdJ92vM42m
[Valency: 0.6] [Danceability: 0.7] [Energy: 0.4] [Mood: dark] [Genre: Electropop] [Song1: Bad Guy] [Singer1: Billie Eilish] [Song2: bury a friend] [Singer2: Billie Eilish] [Song3: Don't Start Now] [Singer3: Dua Lipa]
White shirt now red, my bloody nose. Sleeping, you're on your tippy toes. Creeping around like no one knows. Think you're so criminal. Bruises on both my knees for you. Don't say thank you or please, I do. What I want when I'm wanting to. My soul? So cynical. So you're a tough guy. Like-it-really-rough guy. Just-can't-get-enough guy. Chest-always-so-puffed guy. I'm that bad type. Make-your-mama-sad type. Make-your-girlfriend-mad type. Might-seduce-your-dad type. I'm the bad guy, duh


2374M0fQpWi3dLnB54qaLX
[Valency: 0.7] [Danceability: 0.7] [Energy: 0.4] [Mood: nostalgic] [Genre: Soft Rock] [Song1: Africa] [Singer1: Toto] [Song2: Don't Stop Believin] [Singer2: Journey] [Song3: The Boys of Summer] [Singer3: Don Henley]
I hear the drums echoing tonight. But she hears only whispers of some quiet conversation. She's coming in twelve-thirty flight. Her moonlit wings reflect the stars that guide me towards salvation. I stopped an old man along the way. Hoping to find some old forgotten words or ancient melodies. He turned to me as if to say. "Hurry, boy, it's waiting there for you". It's gonna take a lot to drag me away from you. There's nothing that a hundred men or more could ever do. I bless the rains down in Africa. Gonna take some time to do the things we never had


4OSBTYWVwsQhGLF9NHvIbR
[Valency: 0.5] [Danceability: 0.7] [Energy: 0.8] [Mood: intense] [Genre: Soul] [Song1: Rolling in the Deep] [Singer1: Adele] [Song2: Someone Like You] [Singer2: Adele] [Song3: Set Fire to the Rain] [Singer3: Adele]
There's a fire starting in my heart. Reaching a fever pitch, it's bringing me out the dark. Finally I can see you crystal clear. Go 'head and sell me out and I'll lay your shit bare. See how I leave with every piece of you. Don't underestimate the things that I will do. There's a fire starting in my heart. Reaching a fever pitch. And it's bringing me out the dark





