
<h1 align="center">mongoke</h1>
<p align="center">
  <img width="300" src="https://github.com/remorses/mongoke/blob/master/.github/logo.png?raw=true">
</p>

## Instantly get a graphql server to serve your MongoDb database

## Usage
Define yoor database schma with a simple configuration
```yaml
# example.yml

db_url: mongodb://mongo:27017/db

skema: |
    Article:
        content: Str
        autorId: ObjectId
        createdAt: DateTime
    User:
        _id: ObjectId
        name: Str
        surname: Str
        aricleIds: [ObjectId]
    ObjectId: Any
    DateTime: Any

types:
    User:
        collection: users
    Article:
        collection: articles

relations:
    -   from: User
        to: Article
        relation_type: to_many
        field: articles
        query:
            autorId: ${{ parent['_id'] }}
```

Then generate the server code and serve it with the mongoke docker image
```
version: '3'

services:
    server:
        image: mongoke/mongoke:latest
        command: /conf.yml
        volumes: 
            - ./example.yml:/conf.yml
    mongo:
        image: mongo
        logging: 
            driver: none
```

Then you can query the database from your graphql app as you like

```graphql

{
  author(where: {name: "Joseph"}) {
    name
    articles {
      nodes {
        content
      }
    }
  }
}
```

```graphql

{
  articles(first: 5, after: "22/09/1999", cursorField: createdAt) {
    nodes {
      content
    }
    pageInfo {
      endCursor
    }
  }
}
```

## Todo:
- publish the docker image (after tartiflette devs fix extend type issue)
- connection nodes must all have an _id field because it is default cursor field
- unit tests for the connection_resolver
- integration tests for all the resolver types
- integration tests for the relations
- cursor must be obfuscated in connection, (also after and before are string so it is a must)
- ~~add pipelines feature to all resolvers (adding a custom find and find_one made with aggregate)~~
- ~~add the $ to the where input fields inside resolvers (in must be $in, ...)~~
- ~~remove strip_nones after asserting v1 works~~

Low priority
- add verify the jwt with the secret if provided
- ~~add schema validation to the configuration~~
- add subscriptions
- add edges to make connection type be relay compliant 
- better performance of connection_resolver removing the $skip and $count
- add a dataloader for single connections
