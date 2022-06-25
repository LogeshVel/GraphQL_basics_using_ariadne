from ariadne import QueryType, gql, make_executable_schema, MutationType, load_schema_from_path
from ariadne.asgi import GraphQL
from data import BOOK_STORE
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_book_from_book_store_by_id(book_id):
    logger.info(f"Getting the Book of ID {book_id} from the Book Store")
    for book in BOOK_STORE:
        if str(book["book_id"]) == str(book_id):
            logger.info(book)
            return book


def is_book_exists_in_book_store(book_id):
    logger.info(f"Checking whether the Book of ID {book_id} exists")
    for book in BOOK_STORE:
        if str(book["book_id"]) == str(book_id):
            logger.info(f"Book with the ID {book_id} exists")
            return True
    logger.info(f"Book with the ID {book_id} doesn't exist")
    return False


def generate_unique_id():
    if len(BOOK_STORE) == 0:
        return 1
    last_book = BOOK_STORE[len(BOOK_STORE) - 1]
    last_book_id = last_book.get("book_id")
    return last_book_id + 1


def delete_book_from_book_store(book_id):
    """
    Call this function after calling is_book_exists_in_book_store() function
    """
    logger.info(f"Deleting the Book of ID {book_id} from the Book store")
    for i, book in enumerate(BOOK_STORE):
        if str(book["book_id"]) == str(book_id):
            BOOK_STORE.pop(i)
            logger.info(f"Deleted the book of ID {book_id}")
            return True
    logger.info(f"Failed to delete the book of ID {book_id}")
    return False


def get_book_list_for_genre(book_genre):
    logger.info(f"Getting the books of the given genre - {book_genre}")
    book_list = []
    for book in BOOK_STORE:
        if book.get("genre") == book_genre:
            book_list.append(book)

    return book_list


query = QueryType()
mutation = MutationType()


@query.field("book")
def resolve_book(_, info, book_id):
    logger.info(f"Query book with the Book ID {book_id}")
    if is_book_exists_in_book_store(book_id):
        return {"isexists": True, "book": get_book_from_book_store_by_id(book_id)}
    return {"isexists": False}


@query.field("books")
def resolve_books(_, info):
    logger.info(f"Query books")
    return BOOK_STORE


@query.field("getbooks")
def resolve_getbooks(_, info, getgenre):
    logger.info(f"Query getbooks")
    return get_book_list_for_genre(getgenre)


@mutation.field("add_book")
def resolve_add_book(_, info, input):
    logger.info(f"Mutation add_book with the input - {input}")
    try:
        book_id = generate_unique_id()
        input.update({"book_id": book_id})
        BOOK_STORE.append(input)
        r = {"iserror": False, "description": "success", "book_id": book_id}
        logger.info(f"Successfully added and the id is {book_id}")
    except Exception as e:
        logger.error(e)
        logger.error("Failed to add the book")
        r = {"iserror": True, "description": str(e), "book_id": None}
    return r


@mutation.field("update_book")
def resolve_update_book(_, info, input):
    """
    input : {
            book_id: ID!
            title: String
            authors: [{
                name: String
                mail: String
            }]
    """
    book_id = input["book_id"]
    logger.info(f"Mutation update_book with the Book ID {book_id}")
    try:
        if is_book_exists_in_book_store(book_id):
            book_to_update = get_book_from_book_store_by_id(book_id)
            if input.get("title"):
                book_to_update["title"] = input["title"]
            if input.get("authors"):
                book_to_update["authors"] = input["authors"]
            r = {"iserror": False, "description": f"Successfully updated the book id ({book_id})"}
            logger.info(f"Successfully updated the book with the ID {book_id}")
        else:
            r = {"iserror": True, "description": f"Given book id ({book_id}) doesn't exists"}
            logger.info(f"Failed to updated the book with the ID {book_id}. Since the book id doesn't exist")

    except Exception as e:
        logger.error(e)
        logger.error(f"Failed to updated the book with the ID {book_id}")
        r = {"iserror": True, "description": str(e)}
    return r


@mutation.field("delete_book")
def resolve_delete_book(_, info, book_id):
    logger.info(f"Mutation delete_book with the Book ID {book_id}")
    try:
        if is_book_exists_in_book_store(book_id):
            if delete_book_from_book_store(book_id):
                r = {"iserror": False, "description": f"Successfully deleted the book id ({book_id})"}
            else:
                r = {"iserror": True, "description": f"Some internal error while deleting the book of ID ({book_id})"}
        else:
            logger.error(f"Given Book ID doesn't exist")
            r = {"iserror": True, "description": f"Given book id ({book_id}) doesn't exists"}

    except Exception as e:
        logger.error(e)
        logger.error(f"Error while deleting the Book of ID {book_id}")
        r = {"iserror": True, "description": str(e)}
    return r


# We can load the schema from either the file or we can directly define here
# Below is the example for defining the schema here and using it

# type_defs = gql("""
#     type Query {
#         book(book_id : ID!): GetBookResult
#         books: [Book]
#     }
#     type Mutation {
#         add_book(input: BookInput!): PostStatus
#         update_book(input: UpdateInput): PutStatus
#         delete_book(book_id: ID!): DeleteStatus
#     }
#     input UpdateInput{
#         book_id: ID!
#         title: String
#         authors: [UpdateAuthorInput]
#     }
#     input UpdateAuthorInput{
#         name: String
#         mail: String
#     }
#     input BookInput{
#         title: String!
#         authors: [AuthorInput]!
#     }
#     input AuthorInput{
#         name: String!
#         mail: String
#     }
#     type PutStatus{
#         iserror: Boolean!
#         description: String
#     }
#     type DeleteStatus{
#         iserror: Boolean!
#         description: String
#     }
#     type PostStatus{
#         iserror: Boolean!
#         description: String
#         book_id: ID
#     }
#     type Author{
#         name: String!
#         mail: String
#     }
#     type Book{
#         title: String!
#         book_id: ID
#         authors: [Author]!
#     }
#     type GetBookResult{
#         isexists: Boolean!
#         book: Book
#     }
# """)
# schema = make_executable_schema(type_defs, query, mutation)
# app = GraphQL(schema, debug=True)


# Below is the example of loading the schema from the external file
book_type_defs = load_schema_from_path("book_schema.graphql")
schema = make_executable_schema(book_type_defs, query, mutation)
app = GraphQL(schema, debug=True)
