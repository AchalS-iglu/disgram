from instagrapi import Client

incl = Client()
incl.login(username="obvigloop", password="blehbleh69")



stories = (incl.user_stories(user_id = 27996795166, amount=5))

for story in stories:
    incl.story_download(story_pk=story.pk)
