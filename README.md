What :
    *A Web Application built to create, manage and participate in sporting events.
    *App admin can give certain users host status, those users can create and manage events.
    *Other users can register to events from a list of upcoming events on the home page.
    *Users can see upcoming events they have registered to and past events they have participated in, from      their dashboard.
    *Users can unregister from free events they have registered to. 
    *Users can create, join teams and register as teams to team events.
    *Hosts can Create / View / Update & Delete Events from their dashboard. List of users who are registered to a specific event are viewable and downloadable as csv from the dashboard of that given event's host.
    *Events Can Individual Events, Team Events, Paid Events, Free Events. Online payment has not be integrated yet but an input for transaction id is used for paid events so that users can click on a link to be redirected to a third part payment gateway and then after successful payment, input the transaction Id on this app so that an admin can reference and validate the payment.
    

Why :
    I work for a sporting goods retailer and we try to engage different sporting communities by either hosting events ourselves or by collaborating with others who are involved in communities of their respective sports. We usually use Google Forms as registration forms and share those forms via Facebook. I built this web app to solve the following problems :
        a. Have an organized portal where users can see a list of all sporting events coming up in one place so that sports enthusiasts who are not active on social media do not miss out.
        b. Have a fixed format which hosts can follow to create events by and the kind of data they can collect.
        c. Make it easier for users to sign up for different events from different hosts by signing up once and just clicking on register without having to fill up a form with the same information for all the different events they want to participate in.
        d. Keep track of what events users have signed up for.
    I built this allocating an hour each morning before work as a prototype to pitch to my manager. If validated, I can build a production version utilizing paid work hours :D :D :D 

Distinctiveness and Complexity:
    
    This project is distinct form other projects that I have done in this course for the following reasons:

        This project is functionally different and serves a completely different purpose than any of the projects done during the course. I have gone through Django documentation and used features offered by Django that were not taught during the course. I have used libraries that I have not used during the course. I figured out how I wanted the project to behave and what purpose I wanted it to serve and then read documentations and did my research to find the best tools, functions and libraries that helps me achieve those targets.

    This project is more complex than other projects that I have done in this course for the following reasons:
        
        Multiple user permission levels.
        Views based on Users relationship with the object in view.
        Uses Javascript generated form that changes based on input.
        Greater complexity of relationships between different models.
        CSV download of data.
        Data Validation.
        Email confirmations.

Folders:

    download:
        View and download to csv, list of user details, of users registered to event hosted by logged in user.
        Restricted for users who are managers.

    eventmanage:
        
        CRUD for Events.

        Models : 
            Manager  - Object like an organization that can host Events, managed by an user. 
            EventType, PaymentMethod - as relationals for Event
            Event
            TransactionId - to keep track of payment offline payments
            Community - Not yet implemented.
        
        View : 
            Managers can create events using a form that guides through the process using javascript to renders in/out input fields and options based on users input.

            Events can be Edited or Deleted by managers
            Authenticated users who have created a profile can register/unregister to free events, Register to paid events.

            Teams can be registered/unregistered to team events. Each user in team is added to participants list in Event.

    events:
        Core App

    media:
        User uploaded media storage
    
    profiles:

        Model : 
            Profile -  Detailed profile model with relationship to the User model as Foreignkey. 
            Area - Location of user - for relationship with profile
            Sport - User Sport interest - for relationship with profile

        View : 
            User Dashboard -  
                Displays user profile if one exists, or a profile creation form. 
                Profile can be viewed and edited.
                Has option for changing email address.
                User can see list of upcoming events user has registered to.
                User can see list of past events user has participated in.
                User can see list of teams uer is part of / user manages.
                User has the option to create or join a team.

            
                
        

    Teams: 
        Model and functionality for managing teams. Can create teams with one manager and multiple         members. Teams can assign passwords that users have to use to join the team. Teams have foreign relation to specific sport.
    

How to Run:
    *Create virtual environment
    *cd in to root folder
    *run pip install -r requirements.txt
    *run python manage.py migrate
    *run python manage.py runserver

