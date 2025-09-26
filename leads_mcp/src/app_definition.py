from fastapi import FastAPI
from routes import leads_mcp
import contextlib


leads_app = leads_mcp.streamable_http_app()

@contextlib.asynccontextmanager
async def combine_mcp_lifespans(app):
    async with contextlib.AsyncExitStack() as stack:

        await stack.enter_async_context(leads_app.lifespan(app))
        yield


app = FastAPI(
    lifespan=combine_mcp_lifespans #  one lifespan to rule them all
)

app.mount("/v1/leads/", leads_app)