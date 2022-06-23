# GraphQL_basics_using_ariadne
GraphQL CRUD API in Python using ariadne library(schema-first approach)

### GraphQL Server operations 

- **Create** - create new book in the book store using Mutation type

- **Read** - query the book using the Book ID or query all the books

- **Update** - update the book using the Mutation type with the Book ID

- **Delete** - delete the book from the book store using the Mutation type with the Book ID

#### Note

- Server uses in-memory store to store the Books information not any kind of database. (To make it simpler and focus on the GraphQL API Server implementation part)


### GraphQL Server's schemas,

**Query type**.

![Image](https://github.com/LogeshVel/GraphQL_basics_using_ariadne/blob/main/snaps/types/query_types.png)

**Mutation type**

![Image](https://github.com/LogeshVel/GraphQL_basics_using_ariadne/blob/main/snaps/types/mutation.png)

## Server

Server is created in Python and to start the server need to install two Packages

- ariadne

```
pip install ariadne
```

- uvicorn

```
pip install uvicorn
```

Now, start the Server using the following command.

```
uvicorn main:app
```

- here **main** is the filename


Open the _http://127.0.0.1:8000_ (default one)

Now you can query and mutate the Book Information.

Also you can test this in the Postman.
