
from tartiflette import Resolver
from .support import strip_nones, connection_resolver, zip_pluck, select_keys, get_pagination, get_cursor_coercer
from operator import setitem
from funcy import omit

def filter_nodes_by_guard(nodes, fields):
    for x in nodes:
        try:
            
            yield omit(x or dict(), fields)
        except Exception:
            pass


map_fields_to_types = {
        "_id": "ObjectId",
        "user_id": "ObjectId",
        "username": "String"
    }

pipeline: list = [
    {
        "$set": {
            "user_id": "fucku"
        }
    }
]

@Resolver('Query.bots')
async def resolve_query_bots(parent, args, ctx, info):
    where = strip_nones(args.get('where', {}))
    cursorField = args.get('cursorField', '_id')
    headers = ctx['req'].headers
    jwt = ctx['req'].jwt_payload
    fields = []
    
    pagination = get_pagination(args,)
    data = await connection_resolver(
        collection=ctx['db']['bots'], 
        where=where,
        cursorField=cursorField,
        pagination=pagination,
        scalar_name=map_fields_to_types[cursorField],
        pipeline=pipeline,
    )
    data['nodes'] = list(filter_nodes_by_guard(data['nodes'], fields))
    
    return data

