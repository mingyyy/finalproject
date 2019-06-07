
## Structure of the web app

#### 1. Home page
Simple landing page with description of the project and how to use it, who should use it. 

NavBar: 
1. *Register as Traveler or Organization* 
2. *Login* (or *Logout* and *Profile Update* for logged-in users)
3. Links to  *Traveler* and *Organization* info
4. Links to *Trip* and *Availability*

Content:
1. Overview of the webapp
2. Upcoming *Trips*

#### 2. Register Page
Register Form
0. account type
1. username
2. email
3. password

Or Social Authentication (v2)
1. Google
2. Facebook ( not working yet)
3. LinkedIn
4. Twitter (working)
5. Github (not working yet)

#### 3. Update Profile (@login_required @type_required)

##### Travelers
**Page 1** (with progress bar)

Basic Info:
- first name* (default: username)
- last name*
- gender* (f/m/o)
- birthdate* (datepicker)
- nationality* (country list)
- phone number 
- languages* (multiple choices)
- profile photo

**Page 2** (with progress bar)

Professional Info:
- bio (Tell us more about your)
- area of expertise (multiple choice with tag) 
- experiences

**Page 3** (with progress bar)

Add social links:
- Social links (e.g. facebook, linkedin, etc)
- Personal Website
- Other channels


**Page 4** (with progress bar)

Traveler offer (more than one topic - allowed):

- Subject* (list)
- Type* (Event Type List)
- Frequency*
  - One time 
  - Multiple (x times)
  - Flexi 
- Duration* per section(<=2h, 2-4h, 4-8h, >8h)
- Title*
- Description*
- Requirement* (projector, internet, equipments etc)


##### Local Hosts
**Page 1** (with progress bar)

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
- type of offer
- details
    - physical space
    - equipments
    - others (text area)

#### 4. Update Trips/Availability (@login_required @type_required)

##### Travelers Event Page
- New event
    - location (country->city lists jquery)
    - description
    - start date
    - end date
- Update event
- Delete event

travel time, destination 
(traveling info helper, e.g. visa requirements. local ccy, weather etc)

##### Local Host Availability Page
- Create
    - address (default org address)
    - extra info (beyond the profile)
    - start date
    - end date
- Update 
- Delete


#### 5. List of Travelers 
Search based on the following:
- profile: language, gender, country of origin, area of expertise 
- trip: country, date        

Summary: List of results per traveler

#### 6. List of Local Hosts
Search bar: 
- profile: org type, area of interests, language, country
- availability: date

Summary: List of results per org

##### 7. Detail page - per Traveler (@login_required)
detailed traveler profile
travel calendar

##### 8. Detail page - per Local host (@login_required)
detailed organization profile
availability calendar


## Folder structure of the project
github repository: finalproject

            -| env (virtual environment)
            -| proj_travelshare
                -| app_user
                    -| forms.py
                        -| FormRegister
                            -| Type
                            -| Username
                            -| Email
                            -| Password
                        -| FormLogin
                            -| Username
                            -| Password
                        -| FormLogout
                        -| FormPersonBasic
                        -| FormPersonMore
                        -| FormPersonOffer                       
                        -| FormOrgBasic
                        -| FormOrgMore
                        -| FormOrgOffer

                    -| models.py
                        -| User
                            -| type
                            -| username
                            -| email
                            -| password
                            -| first_name
                            -| last_name
                        -| ProfileTraveler (extension of User)
                            -| gender (Choice)
                            -| nationality (Choice)
                            -| phone (PhoneNumberField)
                            -| photo (image)
                            -| bio (Text)
                            -| expertise (ManyToMany: Expertise)
                            -| links (ManyToMany: Link)
                            -| language (ManyToMany: Language)
                        -| ProfileHost (extension of User)
                            -| host Name (Char)
                            -| host Type (Dropdown)
                            -| host Description (Text)
                            -| phone ()
                            -| language (ManyToMany: Language)
                            -| address (Google API)
                            -| photo (image)
                            -| interests (ManyToMany: Expertise)
                            -| interests_details (Text)
                            -| links (ManyToMany: Link)
                                                        
                        -| Traveler_Offer (User One to Many)
                            -| event type (ManyToMany: EventType)
                            -| topic (ManyToMany: Topics)
                            -| title (Char)
                            -| duration (Choice)
                            -| details (Text)   
                            -| requirements (Text)
                            
                        -| Host_Offer (User One to Many)
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
                        -| register
                        -| UserLogin
                        -| UserLogout
                        -| profiletraveler
                        -| profilehost
                    
                -| app_main
                    -| forms.py
                        -| FormTrip(ModelForm)
                        -| FormTravelerTrip (Form)
                        -| FormHostAvailability (ModelForm)
                    -| models.py

                        -| Traveler_Trip (User One to Many)
                            - Location (Char)
                            - Details (Text)
                            - Start_Time (DateTimePicker)
                            - End_Time (DateTimePicker)
                        -| Host_Availability (User one to Many)
                            - Address (Google Map)
                            - Extra_info (Text)
                            - Start_Time (DateTimePicker)
                            - End_Time (DateTimePicker)
                    -| urls.py
                        -| traveler_trip_update
                        -| traveler_trip_create
                        -| host_availability_update
                        -| host_availability_create
                        -| searchperson
                        -| searchorg
                        -| triplist
                    -| views.py
                        -| ViewCreateTrip
                        -| ViewUpdateTrip
                        -| ViewCreateSpace
                        -| ViewUpdateSpace
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
                    -|profile_traveler
                    -|profile_host
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

