
from nintendo.common import http, tls

import logging
logger = logging.getLogger(__name__)


USER_AGENT = {
	 900: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 9.3.0.0; Add-on 9.3.0.0)",
	 901: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 9.3.0.0; Add-on 9.3.0.0)",
	 910: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 9.3.0.0; Add-on 9.3.0.0)",
	 920: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 9.3.0.0; Add-on 9.3.0.0)",
	1000: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 10.4.0.0; Add-on 10.4.0.0)",
	1001: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 10.4.0.0; Add-on 10.4.0.0)",
	1002: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 10.4.0.0; Add-on 10.4.0.0)",
	1003: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 10.4.0.0; Add-on 10.4.0.0)",
	1004: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 10.4.0.0; Add-on 10.4.0.0)",
	1010: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 10.4.0.0; Add-on 10.4.0.0)",
	1011: "libcurl (nnAccount; 789f928b-138e-4b2f-afeb-1acae821d897; SDK 10.4.0.0; Add-on 10.4.0.0)"
}

LATEST_VERSION = 1011


class BAASError(Exception):
	def __init__(self, error):
		self.status = error["status"]
		self.name = error["errorCode"]
		self.title = error["title"]
		self.detail = error["detail"]
		self.instance = error["instance"]
		self.type = error["type"]


class BAASClient:
	def __init__(self):
		self.url = "e0d67c509fb203858ebcb2fe3f88c2aa.baas.nintendo.com"
		self.user_agent = USER_AGENT[LATEST_VERSION]
		self.power_state = "FA"
		
		self.context = tls.TLSContext()
		self.context.load_default_authorities()
	
	def set_url(self, url): self.url = url
	def set_user_agent(self, user_agent): self.user_agent = user_agent
	def set_power_state(self, state): self.power_state = state
	def set_context(self, context): self.context = context
	
	def set_system_version(self, version):
		if version not in USER_AGENT:
			raise ValueError("Unknown system version")
		self.user_agent = USER_AGENT[version]
		
	async def request(self, req, token, use_power_state):
		req.headers["Host"] = self.url
		req.headers["User-Agent"] = self.user_agent
		req.headers["Accept"] = "*/*"
		if token:
			req.headers["Authorization"] = "Bearer " + token
		if use_power_state:
			req.headers["X-Nintendo-PowerState"] = self.power_state
		req.headers["Content-Length"] = 0
		req.headers["Content-Type"] = "application/x-www-form-urlencoded"
		
		response = await http.request(req, self.context)
		if response.error():
			logger.warning("BAAS request returned error: %s" %response.json)
			raise BAASError(response.json)
		return response
		
	async def authenticate(self, device_token):
		req = http.HTTPRequest.post("/1.0.0/application/token")
		req.form["grantType"] = "public_client"
		req.form["assertion"] = device_token
		
		response = await self.request(req, None, True)
		return response.json
	
	async def login(self, id, password, auth, app_token=None):
		req = http.HTTPRequest.post("/1.0.0/login")
		req.form["id"] = "%016x" %id
		req.form["password"] = password
		if app_token:
			req.form["appAuthNToken"] = app_token
			
		response = await self.request(req, auth, True)
		return response.json
