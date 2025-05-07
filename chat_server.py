import asyncio
import websockets
from aiohttp import web

clients = set()

# WebSocket connection handler
async def websocket_handler(websocket, path):
    clients.add(websocket)
    try:
        async for message in websocket:
            await asyncio.wait([client.send(message) for client in clients if client != websocket])
    finally:
        clients.remove(websocket)

# HTTP health check (Render requires this to be alive)
async def health_check(request):
    return web.Response(text="OK")

# Start both HTTP and WebSocket servers
async def main():
    # HTTP Server on port 10000
    app = web.Application()
    app.router.add_get('/', health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 10000)
    await site.start()

    # WebSocket Server on port 10001
    await websockets.serve(websocket_handler, '0.0.0.0', 10001)

    print("✅ Servers running: HTTP (10000), WebSocket (10001)")
    await asyncio.Future()  # Run forever

if __name__ == '__main__':
    asyncio.run(main())
