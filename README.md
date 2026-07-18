I have created a website to display a league standings. You could call it the overall standings of the teams.
As an example, I have retrieved the standings from SportsData.io via API to display the current standings in Major League Baseball.
Alternatively, you can create your own teams and leagues to display results from a local league.
The local league is on the file system. The website allows you to create sports teams and
divide them into leagues, and display the overall standings.
The website could address administrators for results dissemination, perhaps for a
tournament committee in a sports federation. Which could simply display the overall
standings in a tournament. It could be used for other sports - but here, it is intended for
Baseball.
Technically: I have used Python and Flask frameworks, and I store data in SQLite.
I have worked with a 3-layer architecture - where I separate presentation, business logic and
data access. By using this approach, the responsibility for different parts becomes
separated and more manageable for developers. This simplification makes it easier to change and
maintain the code - and it provides better opportunities for reuse of components
or logic.
My presentation layer uses JINJA2 which also contains html & css, we create templates,
which can contain Python variables.
To help create the business logic, it is divided into different services with
different responsibilities. But everything is collected in a service layer.
My data access layer is placed together in a folder called "storage". This layer stands for
creating, reading, updating and deleting data in the database. This is referred to as
CRUD: Create, Read, Update and Delete, which are the fundamental data operations.
You can:
• Create/change teams
o Assign wins and losses
• View the teams in an overview – view the results in an overview
• View the overall standings
• View the MLB standings
o Filter by league and division
