import asyncio
import websockets
from aiohttp import web

clients = set()

async def websocket_handler(websocket, path):
    clients.add(websocket)
    try:
        async for message in websocket:
            await asyncio.wait([client.send(message) for client in clients if client != websocket])
    finally:
        clients.remove(websocket)

async def health_check(request):
    return web.Response(text="OK")  # Handles GET/HEAD requests for Render health checks

async def start_servers():
    # HTTP server for Render health checks
    app = web.Application()
    app.router.add_get('/', health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 10000)  # HTTP on port 10000
    await site.start()

    # WebSocket server
    websocket_server = await websockets.serve(websocket_handler, '0.0.0.0', 10001)  # WebSocket on port 10001

    print("HTTP + WebSocket servers running...")
    await asyncio.Future()  # keep running

if __name__ == '__main__':
    asyncio.run(start_servers())
