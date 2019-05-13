import app_user.constants as cons
from app_user.models import Language, Topic

lan=[]
for x in cons.LANGUAGE_LIST:
    lan.append(Language(language=x))
print(lan)

topic=[]
for x in cons.SUBJECT_LIST:
    topic.append(Topic(topic=x))
print(topic)