
from tartiflette import Resolver
from .support import strip_nones, connection_resolver, zip_pluck, select_keys, get_pagination
from operator import setitem

pipeline = []

@Resolver('Query.bots')
async def resolve_query_bots(parent, args, ctx, info):
    where = strip_nones(args.get('where', {}))
    orderBy = args.get('orderBy', {'_id': 'ASC'}) # add default
    headers = ctx['request']['headers']
    jwt = ctx['req'].jwt_payload # TODO i need to decode jwt_payload
    fields = []
    if not (jwt['_id'] == where['_id']):
        raise Exception("guard `jwt['_id'] == where['_id']` not satisfied")
    else:
        fields += []
    
    pagination = get_pagination(args)
    data = await connection_resolver(
        collection=ctx['db']['bots'], 
        where=where,
        orderBy=orderBy,
        pagination=pagination,
        pipeline=pipeline,
    )
    
        
    
        
    
    return data

