## Assessment 3
### Assessment 3 Brief: **Briefing** 
Assessment: Case Study Project
Length: 1,500 words + 4-6 minutes presentation with a poster
Due Date: 03/12/2025

#### Summary: 
Cyber Security relies on well designed and implemented systems and applications. It is a crucial task to create a design document that addresses not only the desired technical features but all security related constraints and design systems. If such a design document lacks clarity and completeness, the resulting implementation is very likely flawed and creates a security risk.

#### Instructions: 
You are tasked to create a security design guide for a web based data retrieval application. This design guide must include all required security measures, their references to applicable standards (i.e. OWASP, ISO 27001) and the specification of technical methods, such as encryption algorithms or encrypted data transport.  
It is not necessary to include technical details on how the system should be coded or how the GUI design should look like. The guide must concentrate on the security aspects of the application. 

The application is divided into three parts; Request, Retrieve and Review

**Part 1: Request**

**Scenario:**
Consider a web interface where a user can log into and then request data from a
database. The web interface incorporates a login page accessible by a login-
button. After a successful login the web interface for the data retrieval is
accessible and the interface displays a search field(s) that directly create a SQL query to the database with the information stored (your instructor may
demonstrate such an example, as required). The returned information is then
displayed as a result to the user.

The data fields on the web interface may include:
- Name
- Address (separate field for unit, street, postal code, state, suburb)
- Phone number

Wildcard searches are often permitted for ‘Name’ and ‘Phone number’ for user
convenience.

**Task**
You must create a security design specification (not a GUI layout or coding) that
specifies how the individual fields of the web interface shall be sized and
evaluated. It is also required to specify the method of transporting the data from he web interface to the backend (web and database systems) and how the user
authentication shall be performed. It must be specified where the login
credentials are stored, how they are stored and what happens if a user tries to
login with the wrong credentials. References to relevant standards or reasoning
why a specific standard is not being followed is required

**Part 2: Retrieve**

**Scenario:**
Consider an SQL-based database as a case example (note you are not expected
to produce SQL codes and a sample database may be demonstrated by your
instructor, if required). This database contains all retrievable data and shall only
be accessible when a user is successfully logged in. The data stored in the
database consists of:
- Name (last name is sufficient)
- Address (separate entries for unit, street, postal code, state, suburb)
- Phone number
- Medical status with one of the following possible entries:
    - Sick
    - Healthy
    - Cancer
    - Deceased
    - Flu
    - Covid
- Credit card data (credit card number and expiry stored as separate fields)

For simplicity, all fields can be formatted as strings.

**Task:**
In the design document it is mandatory that the appropriate field length is
chosen with a detailed explanation of why this length is chosen. It is also
mandatory that database security related issues are addressed such as SQL-
escaping. Special knowledge of SQL-Databases is not required, you must
describe your design choices in plain English. References to relevant standards
or reasoning why a specific standard is not being followed is required.

**Part 3: Review**

**Scenario:**
A user rights model should exist that permits which user (group) is allowed to
see what kind of data. Generally three groups of users must exist:
1. Normal user that only shall see name and address and phone number from the database
2. Accounting users that can see name, address, phone number and credit card data from the database and
3. Privileged users that can see all data

**Task:**
The design paper has to address how to identify those users and how to create the individual access rights into the database. Again, it is not requested that you know the actual database programming. Description of the required user roles and general system design is adequate.

Generally, this design paper shall be created with the security concept in mind
and not with the technical details. The paper must include the following topics:
- Handling of data input with an explanation for why this form or method is
being used
- Prevention of malicious data input
- Prevention of login trials with incorrect credentials by a robot
- The secure storing and retrieving of account credentials
- The rights model and prevention of gaining unwanted rights
- General security designs
- General risk assessment of applications of that type

If encryption algorithms or any other method for ensuring security is required, a detailed specification of that is mandatory. Detailed specification includes possible algorithms and minimum keylength.
If a requirement from one part is needed in another part this must be reflected in the description of the other part, i.e. if the web page requires a secured field in the database this must be described in the database part.
The student shall present their solution(s) with a one-page poster and a 4-6
minutes presentation about the solution.

As preparation, please review all material provided and discussed during the
modules 1 – 8. Additional individual research in the library and on the internet is recommended.

> Hint: It is a good idea to research the topic of “SQL code injection”.
> Hint: If access to the database is defined to require database credentials (username and password), the handling of these credentials in the database itself is not a required part of the assignment.

#### Applicable standards
The report must include references to applicable standards or industry good practises where appropriate. It is mandatory that the chosen design is compared to the relevant standards and, where it is divergent, to be explained why the standard is not followed.

#### Referencing
Referencing is essential for this assessment. A minimum of one reference for
each topic is required for this, including at least 8 academic sources.

(An academic source is one that has been peer-reviewed).

Your references will be evaluated for their relevance to the case study.
Remember you must ensure that your arguments and justifications are based on
sound reasoning and clear relevance.

Ensure that you reference according to the appropriate APA style, for
citing and referencing information, as well as all appropriate research
sources.

Please see more information on referencing here:
http://library.laureate.net.au/research_skills/referencing
