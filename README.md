# Travel to share
### - A platform for travelers and local organizations

#### History

I had this ideas for years but never had the tools nor the capacity to make it happen. Somehow, my interest for Python 
led me to a bootcamp in web app development which re-ignite the flame. Finally, I am going to bring it to life.

#### About the idea.
Since September, 2014, I had been exploring - understanding myself through 
observing, learning, experimenting and above all, living. Often, I felt the purpose of my trips was merely to 
deliver a message or receiving one. Probably all of us are just messengers in our own ways. 

The majority of people, either youtuber or developers, freelancers or employees of big companies, wants something in common:
travel more! Watching youtube videos is fun but being there is much better. Online courses are great,
convenient and often cost less or nothing. But on-site study is still the best way to learn, in my opinion, 
more effective and more fun. Sharing in person at this digital era has a special charm.

Many interesting websites are out there, already serving travelers from kayak to airbnb, from tripadvisor to lonelyplanet, 
from workaway to nomadlist.There are also many platforms for internationals volunteers but often they are not free. 
Nonetheless, I am not aware of any platform dedicated to serve this special need to share and communicate among
travelers and locals, free of charge. 

Therefore, I want to provide a FREE webapp that allow travelers to share a few words with the locals, 
in the form of a talk, a lecture, a speech, a workshop. Local organizations like
NGOs, schools, communities, or co-ops could help to make this happen. 

A key point is that, I want this space to be completely free to everyone. A common space for
people to give and receive whatever they prefer. A place to connect and share.



#### Overview of the Webapp

Basically, this web app is a free space for travelers to indicate their availabilities when they travel and 
what they would like to share, e.g. a talk or a workshop; and local organizations around the world 
to indicate their interests and needs, plus their capacity to host a sharing event. 

For example, John is a Java developer working in Apple who is passionate about teaching programing to children. He is traveling to 
India with his family for 2 months. Jone registers in this website and updates his profile. When he has a travel plan 
he shares his travel dates and destinations. For instance, a local NGO in Pundicherry, Tamil Nadu 
could host 50 people in their meeting room and the local community they support would love to bring in a tech person for a talk. 
Through this web app they could easily find and contact each other. 
Some children in Southern India might have a new hobby or even a new direction in life after this free talk.

On the one hand, travels could use this platform to spread his/her ideas and share a few words with the local people. 
On the other hand, the participants of the event have the rare chance of meeting the speaker face to face.
Especially for remote locations and under-served communities, a talk or a workshop might plant a life-changing seed. 
It is a way of bring together the travelers and the locals; the experts and the students.


#### Structure of the web app

##### 1. Home page
Simple landing page with description of the project and how to use it, who should use it. 

NavBar: 
1. *Register* and *Login*, (or *Logout* and *Profile Update* for logged-in users)
2. Find *Traveler* info and *Organization* info.

Content:
1. Overview of the webapp
2. Upcoming *Trips*

##### 2. Register Page
Register Form
1. username
2. email
3. password

Or Social Authentication (V2)
1. Google
2. Facebook
3. LinkedIn
4. Twitter
5. Github
6. Own Website

##### 3. Update Profile (@login_required)
**Page 0**

Two options: Travelers Or Organizations

###### Travelers
**Page 1** 
with progress bar

Basic Info:
- first name (default: username)
- last name
- gender
- where are you from (choose from country list)
- languages (professional/causal)
- phone number (optional for whatsapp, wechat, line)

**Page 2** 
with progress bar

More about me:
- profile photo (default pic)
- bio (default: Hello, world! I am {username}.)
- area of expertise (multiple choice with tag) 
- my links:
  - Google
  - Facebook
  - LinkedIn
  - Twitter
  - Instagram
  - Github
  - Own Website
  - Other channels


**Page 3** 
with progress bar

What do you offer (more than one topic - allowed):

- Offer type (choose from talk, workshop, lecture...)
- Duration 
  - One time (<=2h, 2-4h, 4-8h, >1 day)
  - Multiple (daily, weekly, monthly, yearly)
  - Flexi 
- Topic (multiple choices tag)
- Title
- Description
- Requirements (projector, internet, equipments etc)


###### Organizations
**Page 1** 
with progress bar

Basic Info:
- org name (default: username)
- org type (list)
- languages (for communication)
- phone number (whatsapp, wechat, line, )
- address
- description of the org (default: Hello, world!)

**Page 2** 
with progress bar

More about me:
- profile photo (default pic)
- area of interests (multiple choices with tag) 
- more about what we want (text area)
- my links:
  - Google
  - Facebook
  - LinkedIn
  - Twitter
  - Instagram
  - Own Website
  - Other channels
  
**Page 3** 
with progress bar

What we can offer: 
- physical space
- equipments
- others (text area)

##### 4. Update Availability (Calendar page)

###### Travelers Event Page
- New event
    - location (country->city lists jquery)
    - description
    - start date
    - end date
- Update event
- Delete evnent

travel time, destination 
(traveling info helper, e.g. visa requirements)

###### Organizations Availability Page
- Create
    - address (default org address)
    - extra info (beyond the profile)
    - start date
    - end date
- Update 
- Delete



##### 5. List of Travelers 
Search based on the following:
- profile: language, gender, country of origin, area of expertise 
- trip: country, date        

List of results per traveler

##### 6. List of Organizations
Search bar: 
- profile: org type, area of interests, language, country
- availability: date

List of results per org

##### 7. Detail page - per Traveler (@login_required)
detailed traveler profile
travel calendar

##### 8. Detail page - per Organization (@login_required)
detailed organization profile
availability calendar


#### Folder structure of the project
github repository: finalproject

            -| env (virtual environment)
            -| proj_travelshare
                -| app_user
                    -| forms.py
                        -| FormRegister
                        -| FormLogin
                        -| FormLogout
                        -| FormPersonBasic
                        -| FormPersonMore
                        -| FormPersonOffer 
                        -| FormPersonEvent                         
                        -| FormOrgBasic
                        -| FormOrgMore
                        -| FormOrgOffer
                        -| FormOrgEvent
                    -| models.py
                        -| User
                            -| Username
                            -| Email
                            -| Password
                        -| Profile_Person (extension of User)
                            -| Gender (Choice)
                            -| Nationality (Char)
                            -| Language (ManyToMany: Language)
                            -| Phone ()
                            -| photo (image)
                            -| bio (Text)
                            -| expertise (ManyToMany: Expertise)
                            -| links (ManyToMany: Link)
                        
                        -| Profile_Org (extension of User)
                            -| Org Name (Char)
                            -| Org Type (Dropdown)
                            -| Org Description (Text)
                            -| Phone ()
                            -| Language (ManyToMany: Language)
                            -| Address (Google API)
                            -| photo (image)
                            -| interests (ManyToMany: Expertise)
                            -| interests_details (Text)
                            -| links (ManyToMany: Link)                            
 
                        -| Language
                            -| UserID (ManyToMany)
                            -| Name
                        -| OrgType
                            -| UserID (ManyToMany)
                            -| Name
                        -| Address
                            -| Street
                            -| City
                            -| Country
                            -| PostCode
                        -| Expertise
                            -| UserID (ManyToMany)
                            -| Name
                            -| Level
                        -| Topics - tag
                            -| UserID (ManyToMany)
                            -| Name                      
                        -| EventType
                            -| UserID (ManyToMany)
                            -| Name
                        -| Links
                            -| UserID (ManyToMany)
                            -| Name                                 
                                                                               
                    -| urls.py
                        -| register
                        -| login
                        -| logout
                        -| password_change
                        -| password_change/done
                        -| password_reset
                        -| password_reset/done
                        -| reset/<uidb64>/<token>
                        -| reset/done
                        -| profile_update_person
                        -| profile_view_person
                        -| profile_update_org
                        -| profile_view_org
                        
                    -| views.py
                        -| UserRegistration
                        -| UserLogin
                        -| UserLogout
                        -| ProfileUpdate
                        -| ProfileView
                    
                -| app_main
                    -| forms.py
                        -| FormTrip(ModelForm)
                        -| FormPersonOffer (Form)
                        -| FormOrgOffer (ModelForm)
                    -| models.py
                        -| Person_Offer (User One to Many)
                            -| event type (ManyToMany: EventType)
                            -| topic (ManyToMany: Topics)
                            -| title (Char)
                            -| duration (Choice)
                            -| details (Text)   
                            -| requirements (Text)
                        -| Org_Offer (User One to Many)
                            -| title (char)
                            -| details (text) 
                        -| Person_Trip (User One to Many)
                            - Location (Char)
                            - Details (Text)
                            - Start_Time (DateTimePicker)
                            - End_Time (DateTimePicker)
                    -| urls.py
                    
                    -| views.py
                    
                -| app_info
                
                  
                    
                -| proj_travelshare
                    -| settings.py
                    -| urls.py

                -| media
                    -|profile_person
                    -|profile_org
                -| static
                    -| css
                    -| js
                    -| pic
                -| templates
                    -| app_user
                    -| app_main
                    -| app_info
            -| .gitignore
            -| mimi.py (secret file)
            -| README.md

           