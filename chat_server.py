import asyncio
from aiohttp import web
import aiohttp
import aiohttp.web_ws

clients = set()

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    clients.add(ws)
    try:
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                for client in clients:
                    if client != ws:
                        await client.send_str(msg.data)
    finally:
        clients.remove(ws)

    return ws

async def health_check(request):
    return web.Response(text="OK")

app = web.Application()
app.router.add_get('/', health_check)
app.router.add_get('/ws', websocket_handler)

if __name__ == '__main__':
    web.run_app(app, port=10000)
