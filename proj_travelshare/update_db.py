import app_user.constants as cons
from app_user.models import Language, Topic

# Testing
lan=[]
for x in cons.LANGUAGE_LIST:
    lan.append(Language(language=x))
print(lan)

topic=[]
for x in cons.SUBJECT_LIST:
    topic.append(Topic(topic=x))
print(topic)

# insert into DB

# for x in cons.LANGUAGE_LIST:
# #     p = Language(language=x)
# #     p.save()

# for x in cons.SUBJECT_LIST:
#     p = Topic(topic=x)
#     p.save()
