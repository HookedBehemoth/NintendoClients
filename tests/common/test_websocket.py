
from nintendo.common import websocket, http
import pytest


HOST = "127.0.0.1"


@pytest.mark.anyio
async def test_websocket():
	async def handler(client):
		assert await client.recv() == b"binary"
		assert await client.recv_text() == "text"
		
		await client.send(b"test1")
		await client.send_text("test2")
	
	async with websocket.serve(handler, "TestProtocol", HOST, 12345):
		async with websocket.connect("TestProtocol", HOST, 12345) as client:
			assert client.remote_address() == (HOST, 12345)
			
			await client.send(b"binary")
			await client.send_text("text")

			assert await client.recv_text() == "test2"
			assert await client.recv() == b"test1"


@pytest.mark.anyio
async def test_error():
	async def handler(req):
		response = http.HTTPResponse(404)
		response.body = b"not found"
		return response
	
	async with http.serve(handler, HOST, 12345):
		with pytest.raises(websocket.WSError):
			async with websocket.connect("TestProtocol", HOST, 12345) as client:
				pass
