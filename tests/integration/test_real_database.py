import asyncio
import mongodb_streams
import pytest
from bson import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.testclient import TestClient
from example_generated_code.make_app import make_app
from unittest.mock import _Call, call
from asynctest import mock
from prtty import pretty
from starlette.routing import Lifespan, Router

LETTERS = "abcdefghilmnopqrstuvz"
_ = mock.ANY



def test_get_user_real(query, users: Collection):
    assert not list(users.find({}))
    users.insert_one(dict(name="xxx"))
    q = """
        {
            User {
                _id
                name
                url
            }
        }

      """
    res = query(q)
    pretty(res)
    assert res["data"]["User"]


def test_id_is_searchable(query, users: Collection):
    assert not list(users.find({}))
    id = ObjectId()
    users.insert_one(dict(_id=id, name="xxx"))
    q = """
        query search($id: ObjectId!) {
            User(where: {_id: {eq: $id}}) {
                _id
                name
                url
            }
        }

      """
    res = query(q, dict(id=str(id)))
    pretty(res)
    assert res["data"]["User"]
    assert res["data"]["User"]["_id"] == str(id)


def test_first_and_after_asc(query, users: Collection):
    assert not list(users.find({}))
    LENGTH = 20
    users.insert_many([dict(_id=ObjectId(), name=str(i)) for i in range(LENGTH)])
    q = r"""
        query search($first: Int!, $after: AnyScalar) {
            UserNodes(first: $first, after: $after, cursorField: _id, direction: ASC) {
                nodes {
                    _id
                    name
                    url
                }
                pageInfo {
                    hasPreviousPage
                    hasNextPage
                    startCursor
                    endCursor
                }
            }
        }
      """
    res = query(q, dict(first=10))
    pretty(res)
    assert res["data"]["UserNodes"]["nodes"]
    assert len(res["data"]["UserNodes"]["nodes"]) == 10
    after = res["data"]["UserNodes"]["pageInfo"]["endCursor"]
    res = query(q, dict(first=10, after=after))
    pretty(res)
    assert res["data"]["UserNodes"]["nodes"]
    assert len(res["data"]["UserNodes"]["nodes"]) == 10


def test_first_and_after_desc(query, users: Collection):
    assert not list(users.find({}))
    LENGTH = 20
    users.insert_many([dict(_id=ObjectId(), name=str(i)) for i in range(LENGTH)])
    q = r"""
        query search($first: Int!, $after: AnyScalar) {
            UserNodes(first: $first, after: $after, cursorField: _id, direction: DESC) {
                nodes {
                    _id
                    name
                    url
                }
                pageInfo {
                    hasPreviousPage
                    hasNextPage
                    startCursor
                    endCursor
                }
            }
        }
      """
    res = query(q, dict(first=10))
    pretty(res)
    assert res["data"]["UserNodes"]["nodes"]
    assert len(res["data"]["UserNodes"]["nodes"]) == 10
    after = res["data"]["UserNodes"]["pageInfo"]["endCursor"]
    res = query(q, dict(first=10, after=after))
    pretty(res)
    assert res["data"]["UserNodes"]["nodes"]
    assert len(res["data"]["UserNodes"]["nodes"]) == 10


def test_before_and_last_asc(query, users: Collection):
    assert not list(users.find({}))
    LENGTH = 20
    users.insert_many([dict(_id=ObjectId(), name=str(i)) for i in range(LENGTH)])
    q = r"""
        query search($last: Int!, $before: AnyScalar) {
            UserNodes(last: $last, before: $before, cursorField: _id, direction: ASC) {
                nodes {
                    _id
                    name
                    url
                }
                pageInfo {
                    hasPreviousPage
                    hasNextPage
                    startCursor
                    endCursor
                }
            }
        }
      """
    res = query(q, dict(last=10))
    pretty(res)
    assert res["data"]["UserNodes"]["nodes"]
    assert len(res["data"]["UserNodes"]["nodes"]) == 10
    before = res["data"]["UserNodes"]["pageInfo"]["startCursor"]
    res = query(q, dict(last=10, before=before))
    pretty(res)
    assert res["data"]["UserNodes"]["nodes"]
    assert len(res["data"]["UserNodes"]["nodes"]) == 10


def test_before_and_last_desc(query, users: Collection):
    assert not list(users.find({}))
    LENGTH = 20
    users.insert_many([dict(_id=ObjectId(), name=str(i)) for i in range(LENGTH)])
    q = r"""
        query search($last: Int!, $before: AnyScalar) {
            UserNodes(last: $last, before: $before, cursorField: _id, direction: DESC) {
                nodes {
                    _id
                    name
                    url
                }
                pageInfo {
                    hasPreviousPage
                    hasNextPage
                    startCursor
                    endCursor
                }
            }
        }
      """
    res = query(q, dict(last=10))
    pretty(res)
    assert res["data"]["UserNodes"]["nodes"]
    assert len(res["data"]["UserNodes"]["nodes"]) == 10
    before = res["data"]["UserNodes"]["pageInfo"]["startCursor"]
    res = query(q, dict(last=10, before=before))
    pretty(res)
    assert res["data"]["UserNodes"]["nodes"]
    assert len(res["data"]["UserNodes"]["nodes"]) == 10


def test_before_and_last_different_cursor(query, users: Collection):
    assert not list(users.find({}))
    users.insert_many([dict(_id=ObjectId(), name=str(i)) for i in LETTERS])
    q = r"""
        query search($last: Int!, $before: AnyScalar) {
            UserNodes(last: $last, before: $before, cursorField: name, direction: ASC) {
                nodes {
                    _id
                    name
                    url
                }
                pageInfo {
                    hasPreviousPage
                    hasNextPage
                    startCursor
                    endCursor
                }
            }
        }
      """
    res = query(q, dict(last=10))
    pretty(res)
    assert res["data"]["UserNodes"]["nodes"]
    assert len(res["data"]["UserNodes"]["nodes"]) == 10
    before = res["data"]["UserNodes"]["pageInfo"]["startCursor"]
    res = query(q, dict(last=10, before=before))
    pretty(res)
    assert res["data"]["UserNodes"]["nodes"]
    assert len(res["data"]["UserNodes"]["nodes"]) == 10
