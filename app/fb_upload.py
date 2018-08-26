KEY = None
INTERVAL = 5 #update iterval in seconds
FOOTER = "\nPozdrawiamy,\n Ekipa Radiowęzła\n\nPost automatyczny. Aplikacja \"PH\" P. Dietrich"
import facebook
from time import sleep
from db import get_day, facebook_post, update_facebook_post
from datetime import datetime

def gen_text():
	songs = get_day()
	message = "Dzisiaj (%s) w radiowęźle puściliśmy:\n\n" % (datetime.now().strftime("%d.%m.%Y r."))
	if len(songs)>0:
		for song in songs:
			message += " - %s | %s\n" % (song["song"], song["DJ"])
	else:
		return ""
	message += FOOTER
	return message

def gen_silence():
	return "Dzisiaj (%s) w radiowęźle słuchaliśmy ciszy:\n" % (datetime.now().strftime("%d.%m.%Y r.")) + FOOTER

def update_post():
	graph = facebook.GraphAPI(access_token=KEY)
	latest_update = facebook_post()
	latest_text = gen_text()
	if latest_update["text"] != latest_text:

		#print(latest_update['text'])
		#print(latest_text)
		if latest_text == "":
			latest_text = gen_silence()
		if latest_update["text"] == latest_text:
			return

		print("change found")
		if latest_update["FBID"] is None:
			#need to make new post!
			res = graph.put_object(parent_object='me', connection_name='feed',message=latest_text)
			if 'id' in res:
				latest_update["FBID"] = res['id']
				latest_update["error"] = False
			else:
				print("failed to make post %s" % (res))
				return #error
		else:
			res = graph.put_object(parent_object=latest_update["FBID"], connection_name='',message=latest_text)
			#need to update current post!
			if not ("success" in res and res["success"] == True):
				res = graph.put_object(parent_object='me', connection_name='feed',message=latest_text)
				if 'id' in res:
					latest_update["FBID"] = res['id']
					latest_update["error"] = False
				else:
					print("failed to make post %s" % (res))
					return #error


		#save changes to db
		latest_update['text']=latest_text
		#print(latest_update)
		update_facebook_post(latest_update)

if __name__ == "__main__":
	if KEY is None:
		exit()
	while True:
		update_post()
		sleep(5)
