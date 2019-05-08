
## Structure of the web app

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

Or Social Authentication (v2)
1. Google
2. Facebook ( not working yet)
3. LinkedIn
4. Twitter (working)
5. Github (not working yet)

##### 3. Update Profile (@login_required)
**Page 0**

First time login

Two options: Travelers Or Organizations

###### Travelers
**Page 1** 
with progress bar

Basic Info:
- first name *(default: username)
- last name *
- gender* (f/m/o)
- nationality (choose from country list)
- languages * (lang list, level: professional/causal)
- phone number (optional for whatsapp, wechat, line)

**Page 2** 
with progress bar

More about me:
- profile photo (default pic)
- bio (default: Hello, world! I am {first_name}. Tell us more about your)
- area of expertise (multiple choice with tag) 
- details (professional experiences)

**Page 3**
Add links: (Model: links)
  - Google
  - Facebook
  - LinkedIn
  - Twitter
  - Instagram
  - Github
  - Own Website
  - Other channels


**Page 4** 
with progress bar

What do you offer (more than one topic - allowed):

- Offer type * (choose from Event_List:talk/workshop/lecture...)
- Duration *
  - One time (<=2h, 2-4h, 4-8h, >1 day)
  - Multiple (x times)
  - Flexi 
- Topic *(multiple choices tag)
- Title *
- Description
- Requirements (projector, internet, equipments etc)


###### Organizations
**Page 1** 
with progress bar

Basic Info:
- org name *(default: username)
- org type *(list)
- languages * (language in talks)
- phone number (whatsapp, wechat, line, )
- address *
- description of the org (default: Hello, world!)

**Page 2** 
with progress bar

More about the org:
- profile photo (default pic)
- area of interests (multiple choices with tag) 
- more about what we want (text area)

**Page 3** 
Add my links:
  - Google
  - Facebook
  - LinkedIn
  - Twitter
  - Instagram
  - Own Website
  - Other channels
  
**Page 4** 
with progress bar

What we can offer: 
- title
- details
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
- Delete event

travel time, destination 
(traveling info helper, e.g. visa requirements. local ccy, weather etc)

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

Summary: List of results per traveler

##### 6. List of Organizations
Search bar: 
- profile: org type, area of interests, language, country
- availability: date

Summary: List of results per org

##### 7. Detail page - per Traveler (@login_required)
detailed traveler profile
travel calendar

##### 8. Detail page - per Organization (@login_required)
detailed organization profile
availability calendar


## Folder structure of the project
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
                        -| FormOrgBasic
                        -| FormOrgMore
                        -| FormOrgOffer

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
                        -| ViewProfileUpdatePerson
                        -| ViewProfileUpdateOrg
                    
                -| app_main
                    -| forms.py
                        -| FormTrip(ModelForm)
                        -| FormPersonTrip (Form)
                        -| FormOrgAvailability (ModelForm)
                    -| models.py

                        -| Person_Trip (User One to Many)
                            - Location (Char)
                            - Details (Text)
                            - Start_Time (DateTimePicker)
                            - End_Time (DateTimePicker)
                        -| Org_Availability (User one to Many)
                            - Address (Google Map)
                            - Extra_info (Text)
                            - Start_Time (DateTimePicker)
                            - End_Time (DateTimePicker)
                    -| urls.py
                        -| person_trip_update
                        -| person_trip_create
                        -| org_availability_update
                        -| org_availability_create
                        -| searchperson
                        -| searchorg
                        -| triplist
                    -| views.py
                        -| ViewCreateTrip
                        -| ViewUpdateTrip
                        -| ViewCreateAvailability
                        -| ViewUpdateAvilability
                        -| ViewSearchPerson
                        -| ViewSearchOrg
                        -| ViewTripList
                    
                -| app_info
                    - forms.py
                        - FormVisa (Form)
                            - nationality (Country_List)
                            - destination (Country_List)
                            
                    - views.py
                        - view_visa
                            - retrieve visa info using Sherpa API
                            - retrieve weather info using destination 
                            - retrieve country info using destination
                            - retrieve currency info using nationality/destination ccy (v2)
                
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

