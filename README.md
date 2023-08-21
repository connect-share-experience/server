
# Connect server

This repo is the backend counterpart to the Connect [frontend repo](https://github.com/connect-share-experience/FrontEnd).
It provides API endpoints used to handle all database and algorithms operations needed by the app.




## Stack
- **API** : [FastAPI](https://fastapi.tiangolo.com/)
- **ORM** : [SQLModel](https://sqlmodel.tiangolo.com/)



## See Also

- [pydantic](https://docs.pydantic.dev/latest/)
- [sqlalchemy](https://www.sqlalchemy.org/)
## Run Locally

Clone the project and go to project directory
```bash
  git clone https://github.com/connect-share-experience/server
  cd server
```

Install dependencies
```bash
  python -m pip install -r requirements.txt
```

Create a `.env` file to store app variables.
Use instructions in `app/.env.example` to do so.

Before starting the server, you can use the instructions in makefile to verify that it will run smoothly.


Start the server
```bash
  python -m app.main
```

To see API documentation, go to `/docs` once started on your chosen URL.

## Authors

- [@ejoubrel](https://github.com/ejoubrel)

<img src="https://img.tedomum.net/data/logo%281%29-4d8b91.png" alt="Logo" width=300>
