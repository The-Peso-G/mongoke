import skema
import requests
from typing import *
import sys
from funcy import merge, lmap, collecting, omit, remove, lcat
import yaml
from skema.to_graphql import to_graphql
import os.path
from populate import populate_string
from .templates.resolvers import (
    resolvers_dependencies,
    resolvers_init,
    resolvers_support,
    single_item_resolver,
    many_items_resolvers,
    single_relation_resolver,
    many_relations_resolver,
    generated_init,
)
from .templates.scalars import scalars_implementations
from .templates.graphql_query import (
    graphql_query,
    general_graphql,
    to_many_relation,
    to_many_relation_boilerplate,
    to_one_relation,
)
from .templates.main import main
from .templates.jwt_middleware import jwt_middleware
from .templates.logger import logger
from .templates.engine import engine
from .support import make_touch, pretty, get_skema
from .skema_support import get_scalar_fields, get_skema_aliases
from .naming import get_query_name, get_relation_filename, get_resolver_filenames
from .generators import generate_relation_boilerplate, generate_type_boilerplate

SCALAR_TYPES = ["String", "Float", "Int", "Boolean"]
SCALARS_ALREADY_IMPLEMENTED = [
    "ObjectId",
    "Json",
    "Date",
    "DateTime",
    "Time",
    *SCALAR_TYPES,
]


def add_guards_defaults(guard):
    guard["when"] = guard.get("when") or "before"
    guard["excluded"] = guard.get("excluded") or []
    return guard


def add_disambiguations_defaults(dis):
    return dis


@collecting
def make_disambiguations_objects(disambiguations):
    for type, expr in disambiguations.items():
        yield {"type_name": type, "expression": expr.strip()}


def generate_from_config(config, start=False):
    types = config.get("types", {})

    relations = config.get("relations", [])
    root_dir_path = config.get("root_dir_path", "generated")
    db_url = config.get("db_url", "")
    touch = make_touch(base=os.path.abspath(root_dir_path))
    skema_schema = get_skema(config)

    # TODO add other scalars from the skema
    scalars = [*SCALAR_TYPES, *get_skema_aliases(skema_schema)]
    main_graphql_schema = to_graphql(
        skema_schema, scalar_already_present=SCALARS_ALREADY_IMPLEMENTED
    )

    touch(f"__init__.py", "")
    touch(f"engine.py", engine)
    touch(
        f"__main__.py",
        populate_string(
            main,
            dict(
                root_dir_name=root_dir_path.split("/")[-1],
                db_url=db_url,
                resolver_names=get_resolver_filenames(config),
            ),
        ),
    )
    touch(f"generated/__init__.py", "")
    touch(f"generated/logger.py", logger)
    touch(f"generated/middleware/__init__.py", jwt_middleware)
    touch(f"generated/resolvers/__init__.py", resolvers_init)
    touch(
        f"generated/resolvers/support.py",
        populate_string(
            resolvers_support,
            dict(scalars=[x for x in scalars if x not in SCALARS_ALREADY_IMPLEMENTED]),
        ),
    )
    touch(
        f"generated/scalars.py",
        populate_string(
            scalars_implementations,
            dict(scalars=[x for x in scalars if x not in SCALARS_ALREADY_IMPLEMENTED]),
        ),
    )
    touch(
        f"generated/sdl/general.graphql",
        populate_string(general_graphql, dict(scalars=scalars)),
        index=True
    )
    touch(f"generated/sdl/main.graphql", main_graphql_schema, index=True)
    implemented_types = []
    for typename, type_config in types.items():
        type_config = type_config or {}
        if not type_config.get("exposed", True):
            continue
        disambiguations = type_config.get("disambiguations", {})
        disambiguations = make_disambiguations_objects(disambiguations)
        disambiguations = lmap(add_disambiguations_defaults, disambiguations)
        generate_type_boilerplate(
            touch=touch,
            skema_schema=skema_schema,
            collection=type_config.get("collection", ""),
            typename=typename,
            guards=lmap(add_guards_defaults, type_config.get("guards", [])),
            pipeline=type_config.get("pipeline", []),
            disambiguations=disambiguations,
        )
        implemented_types += [typename]

    for relation in relations:
        toType = relation["to"]
        generate_relation_boilerplate(
            touch=touch,
            skema_schema=skema_schema,
            fromType=relation["from"],
            where_filter=relation["query"],
            toType=toType,
            pipeline=types[toType].get("pipeline", []),
            collection=types[toType].get("collection", []),
            relationName=relation.get("field"),
            relation_type=relation.get("relation_type", "to_one"),
            implemented_types=implemented_types,
            resolver_filename=get_relation_filename(relation),
        )
        implemented_types += [toType]

