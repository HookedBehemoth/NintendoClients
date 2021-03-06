
# Module: <code>nintendo.nex.prudp</code>

Provides a client and server for PRUDP. Originally, PRUDP implemented reliable and secure transmission on top of UDP, but the Nintendo Switch introduced a 'Lite' mode in which PRUDP is implemented on top of TCP or WebSockets instead.

The current implementation only supports a single PRUDP connection per socket.

<code>**class** PRUDPClient</code><br>
<span class="docs">A PRUDP client.</span>

<code>**async with connect**(settings: [Settings](../settings#settings), host: str, port: int, vport: int = 1, context: [TLSContext](../../common/tls#tlscontext) = None, credentials: [Credentials](../kerberos#credentials) = None) -> [PRUDPClient](#prudpclient)</code><br>
<span class="docs">Creates a PRUDP client and connects it to the given address. If `context` is provided, and the underlying transport supports this, the connections is secured with TLS. If credentials are provided they are sent to the server in the connection request. Blocks until the connection is ready and handshake has been performed.</code>

<code>**async with serve**(handler: Callable, settings: [Settings](../settings#settings), host: str = "", port: int = 0, vport: int = 1, context: [TLSContext](../../common/tls#tlscontext) = None, key: bytes = None) -> None</code><br>
<span class="docs">Creates a PRUDP server and binds it to the given address. If `host` is empty, the local address of the default interface is used. If `port` is 0, it is chosen by the operating system. `handler` must be an `async` function that accepts a [`PRUDPClient`](#prudpclient). The client is closed automatically when `handler` returns. If `context` is provided, and the underlying transport supports this, the server is secured with TLS. If `key` is provided it is used to decrypt the Kerberos tickets in connection requests. If `key` is `None`, the payload of connection requests is ignored an all client connections are accepted.</span>

## PRUDPClient
<code>**async def send**(data: bytes, substream: int = 0) -> None</code><br>
<span class="docs">Sends a reliable data packet to the server through the given substream. Blocks if the send buffer is full. Packets are retransmitted automatically if no acknowledgement is received.</span>

<code>**async def send_unreliable**(data: bytes) -> None</code><br>
<span class="docs">Sends an unreliable data packet to the server. Blocks if the send buffer is full.</span><br>

<code>**async def recv**(substream: int = 0) -> bytes</code><br>
<span class="docs">Receives a single reliable data packet from the server from the given substream. Blocks if no reliable data is available.</span>

<code>**async def recv_unreliable**() -> bytes</code><br>
<span class="docs">Receives an unreliable data packet from the server. Blocks if no unreliable data is available. Raises [`InvalidStateError`](../../common/exceptions) if the socket is closed or not connected.</span>

<code>**async def close**() -> None</code><br>
<span class="docs">Closes the connection gracefully. Blocks until the disconnection handshake is complete. If the client is wrapped in an `async with` statement it is closed automatically.</span>

<code>**async def abort**() -> None</code><br>
<span class="docs">Aborts the connection by closing the underlying transport.</span>

<code>**def pid**() -> int</code><br>
<span class="docs">Returns the user id of the connected client. Returns `None` if the client is connected without credentials.</span>

<code>**def minor_version**() -> int</code><br>
<span class="docs">Returns the PRUDP minor version that was negotiated during the handshake.</span>

<code>**def local_address**() -> tuple[str, int]</code><br>
<span class="docs">Returns the local address of the client.</span>

<code>**def remote_address**() -> tuple[str, int]</code><br>
<span class="docs">Returns the address that the client is connected to.</span>
