Welcome to Myne!
=====================

Myne is a free and open-source online platform, incubated within Parsons the New School for Design by two design professors, Jess Irish and Jane Pirone. The platform was developed to “connect and visualize relationships between the people, courses, research and projects within the university.” 
Myne was developed for students, faculty and administrators to get ‘the big picture view’ of the academic and research activity within the university.

The Myne software platform is currently developed within XYZlab, “a creative research and design team that focus[es] on the collaborative development of participatory design tools for spatialized urban research, social networking, community participation and non-linear storytelling.” 

##Name
“Myne” is an abbreviated name from the original name "DataMyne", and is a play on the popular URL syntax using the pronoun “my”. Two earlier papers presented in 2010 refer to the earlier platform name “DataMyne.”

##History
* Myne was launched in the spring of 2009 to all full and part-time Parsons faculty. As of February 2011, there were 1,339 registered users, including over 150 students prototypes.
* Myne 1.0 was first released documentation of its code internally within The New School on May 16, 2011.
* Myne 2.0 was released within the GitHub repository under the AGPL license in July, 2013.

##Features
Profiles that users may edit to include their names, contact information, areas of expertise, tags noting their interests, research/creative projects, documentation of works, portfolio links, teaching history, syllabi, streaming lectures, and much more. They may share this information as publicly as they choose. Indeed, user-friendly and flexible privacy controls have been specifically implemented with data-sharing critics in mind.

Integration with existing academic technologies and databases that provide course information (e.g., SunGard systems) and verification and streamlining of data imports.

Flexible data hub which combines user information with official database information to efficiently feed other content areas such as school websites and magazines, blogs, and mobile applications.

Robust search options that provide detailed results and filtered browsing and also allow for random content generation — another method of discovering connections between users.

Visualizations of connections between users, areas of expertise, interests, research/creative projects, programs, courses, syllabi, and curricular attributes.

Customizable permission system that allows for varying levels of editing access, to provide a distributed method for keeping information up to date, shared amongst administrators, faculty administrators and full-time faculty.

Mobile interface which allows for DataMyne to connect to event or exhibition related projects, as was prototyped in 2011 for the Parsons Festival.

##Maintenance
Myne is currently being supported and maintained by Parsons the New School for Design and The New School.

##Contributors
Myne would like to thank the following people for their help in creating and maintaining Myne.

* Frederico Andrade <faandrade@gmail.com>
* Jane Pirone - Data Mining <mining@b1950.parsons.edu>
* Levi Gross <grossl@newschool.edu>
* Lucas Vickers <lucasvickers@gmail.com>
* Or Zubalsky <juviley@gmail.com>
* Rory Solomon <rory@myne.newschool.edu>
* dbudell
* edwarm40
* lucasvickers

If you contributed to Myne and have been left out of the list, please submit a pull request.

#How to install Myne

## 1. Server Setup

`fab setup_and_deploy`

## 2. Django Setup

 `python manage.py syncdb --all`
 `python manage.py migrate --fake # We fake the migrations as the DB is setup properly within the last step`
