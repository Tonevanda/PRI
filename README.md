# One Piece Search Engine

Developed for PRI (Information Processing and Retrieval) @ FEUP - MEIC

Uses Solr' capabilities to create the search engine. Uses both keyword matching and embeddings.

Report can be found [here](/report/One_Piece_Search_Engine.pdf) for in-depth analysis.

## Solr

In order to access Solr capabilities you need to have Solr 9.0 and Docker installed on your system

Then you need to run `pip install -r requirements.txt` in your terminal inside [backend/project](/backend/project) to install dependencies

Since embeddings are a huge file that we couldn't upload to GitHub, you need to create them yourself by running [get_embeddings.py](/backend/project/src/scripts/get_embeddings.py) and placing the file ``data_embeddings.json`` inside [data](/backend/project/data/)

Now to start Solr run [startup.sh](backend/project/src/startup.sh) inside a bash terminal

## Frontend

The frontend is built using React.

To run it, you need Node.js installed in your system.

After that, run `npm install` to install the node package manager in your system.

To run the React App, go into the `frontend` folder and run `npm start`.

## Backend

The backend was setup using Django.

You need Django installed in your system.

To do that, run `pip install django` in your terminal.

To start the server, go into the `backend` folder and run `python3 manage.py runserver` or `python manage.py runserver`.

## Developed by

- João Lourenço
- João Cardoso
- Tiago Cruz
- Tomás Xavier
