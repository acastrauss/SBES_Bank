# SBES_Bank
Bank security system with breach testing, for faculty class named: 'Sigurnost i bezbednost elektroenergetskih sistema' (Safety and security of power systems) at Faculty of Technical Sciences, Novi Sad, Serbia.

The project consists of 3 main parts:

1. Banking system:
  Web application where clients can login/sign up and use banking services. 
  Clients have authentificated and authorized access to all services, based on their roles (login with certificate and email/password login).   

2. Data leak prevenetion:
 Preventing leakage of sensitive data (Card number, CIV number, etc.) with control of copy-paste, screenshot, and similar events inside of an application (analogy to modern mobile  banking application features).

3. Breach testing:
  Trying to access/destroy/corrupt system data, with attacks like: SQL injection, modified bank/self-generated certificate access, ransomware attacks, etc.
  
 
Implementation details:
  Main web application backend is in Python (Django REST framework) and frontend is in React/Angular.
  Data leakage prevention in frontend framework.
  Breach testing is done with Python.
