<p align="center">
  <img width="300" src="https://github.com/remorses/mongoke/blob/master/.github/logo.jpg?raw=true">
</p>
<h1 align="center">mongoke</h1>
<h3 align="center">Instantly serve your MongoDb database via graphql</h3>

[**Docs**](https://mongoke.now.sh/docs/) • [**Examples**](https://github.com/remorses/mongoke/tree/master/examples)

## Features

-   **Powerful Queries**: Pagination, filtering, relation, relay-style connections built-in and generated in a bunch of seconds
-   **Works with existing databases**: Point it to an existing MongoDb database to instantly get a ready-to-use GraphQL API
-   **Authorization via Jwt**: Every collection can be protected based on jwt payload and document fields
-   **Horizontally Scalable**: The service is completely stateless and can be replicated on demand
-   **Apollo Federation**: The service can be easily glued with other graphql servers to handle writes and more complicated logic.
-   **Resilient Idempotent Configuration**: One YAML Configuration as the only source of truth, relations, authorization and types in one file

## Quickstart:

## Using Docker compose

The fastest way to try Mongoke is via docker-compose.

### 1. Write the configuration to describe the database schema and relations

The ObjectId scalar is already defined by default, it is converted to string when sent as json

```yml
# ./mongoke.yml
schema: |
    type User {
        _id: ObjectId
        username: String
        email: String
    }
    type BlogPost {
        _id: ObjectId
        author_id: ObjectId
        title: String
        content: String
    }

types:
    User:
        collection: users
    BlogPost:
        collection: posts

relations:
    - field: posts
      from: User
      to: BlogPost
      relation_type: to_many
      where:
          author_id: ${{ parent['_id'] }}
```

### 2. Run the `mongoke` image with the above configuration

To start the container mount copy paste the following content in a `docker-compose.yml` file, then execute `docker-compose up`.

```yml
# docker-compose.yml
version: '3'

services:
    mongoke:
        ports:
            - 4000:80
        image: mongoke/mongoke
        environment:
            DB_URL: mongodb://mongo/db
        volumes:
            - ./mongoke.yml:/conf.yml
    mongo:
        image: mongo
```

### 3. Query the generated service via graphql or go to [http://localhost:4000/graphiql](http://localhost:4000/graphiql) to open graphiql

```graphql
{
    User(where: { username: { eq: "Mike" } }) {
        _id
        username
        email
        posts {
            nodes {
                title
            }
        }
    }

    BlogPostNodes(first: 10, after: "Post 1", cursorField: title) {
        nodes {
            title
            content
        }
        pageInfo {
            endCursor
            hasNextPage
        }
    }
}
```

---

## Tutorials

Check out the /examples directory in this repo

Please help the project making new tutorials and submit a issue to list it here!

## Contributors

### Code Contributors

This project exists thanks to all the people who contribute. [[Contribute](CONTRIBUTING.md)].
<a href="https://github.com/remorses/mongoke/graphs/contributors"><img src="https://opencollective.com/mongoke/contributors.svg?width=890&button=false" /></a>

### Financial Contributors

Become a financial contributor and help us sustain our community. [[Contribute](https://opencollective.com/mongoke/contribute)]

#### Individuals

<a href="https://opencollective.com/mongoke"><img src="https://opencollective.com/mongoke/individuals.svg?width=890"></a>

#### Organizations

Support this project with your organization. Your logo will show up here with a link to your website. [[Contribute](https://opencollective.com/mongoke/contribute)]

<a href="https://opencollective.com/mongoke/organization/0/website"><img src="https://opencollective.com/mongoke/organization/0/avatar.svg"></a>
<a href="https://opencollective.com/mongoke/organization/1/website"><img src="https://opencollective.com/mongoke/organization/1/avatar.svg"></a>
<a href="https://opencollective.com/mongoke/organization/2/website"><img src="https://opencollective.com/mongoke/organization/2/avatar.svg"></a>
<a href="https://opencollective.com/mongoke/organization/3/website"><img src="https://opencollective.com/mongoke/organization/3/avatar.svg"></a>
<a href="https://opencollective.com/mongoke/organization/4/website"><img src="https://opencollective.com/mongoke/organization/4/avatar.svg"></a>
<a href="https://opencollective.com/mongoke/organization/5/website"><img src="https://opencollective.com/mongoke/organization/5/avatar.svg"></a>
<a href="https://opencollective.com/mongoke/organization/6/website"><img src="https://opencollective.com/mongoke/organization/6/avatar.svg"></a>
<a href="https://opencollective.com/mongoke/organization/7/website"><img src="https://opencollective.com/mongoke/organization/7/avatar.svg"></a>
<a href="https://opencollective.com/mongoke/organization/8/website"><img src="https://opencollective.com/mongoke/organization/8/avatar.svg"></a>
<a href="https://opencollective.com/mongoke/organization/9/website"><img src="https://opencollective.com/mongoke/organization/9/avatar.svg"></a>
