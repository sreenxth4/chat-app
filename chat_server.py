import asyncio
from aiohttp import web, WSMsgType

clients = set()

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    clients.add(ws)
    try:
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                # Broadcast message to all other clients
                for client in clients:
                    if client != ws:
                        await client.send_str(msg.data)
            elif msg.type == WSMsgType.ERROR:
                print(f'WebSocket connection closed with exception: {ws.exception()}')
    finally:
        clients.remove(ws)
    return ws

async def health_check(request):
    return web.Response(text="OK")

app = web.Application()
app.router.add_get("/", health_check)
app.router.add_get("/ws", websocket_handler)  # WebSocket endpoint

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=10000)
