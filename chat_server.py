import asyncio
import websockets

clients = []

# Handle incoming WebSocket connections
async def handle(websocket):
    try:
        username = await websocket.recv()
        # Ignore HTTP connections that are not real WebSocket requests
        if username.startswith("GET") or username.startswith("HEAD") or "HTTP" in username:
            print("Ignored HTTP client:", username)
            await websocket.close()
            return

        clients.append(websocket)
        print(f"{username} connected.")
        await broadcast(f"{username} joined the chat!")

        while True:
            message = await websocket.recv()
            if message:
                await broadcast(message)

    except Exception as e:
        print("Error in handle():", e)
    finally:
        if websocket in clients:
            clients.remove(websocket)
        await websocket.close()
        await broadcast(f"{username} has left the chat.")

# Broadcast message to all connected clients
async def broadcast(message):
    for client in clients:
        try:
            await client.send(message)
        except Exception as e:
            print(f"Error broadcasting message: {e}")

# Start the WebSocket server
async def main():
    async with websockets.serve(handle, "0.0.0.0", 55555):
        print("WebSocket server running on port 55555...")
        await asyncio.Future()  # run forever

# Run the WebSocket server
asyncio.run(main())
