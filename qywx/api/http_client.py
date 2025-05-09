from typing import Any, Dict, Optional
import requests

def http_get(url: str, params: Optional[Dict[str, Any]] = None, timeout: int = 5) -> Dict[str, Any]:
	resp = requests.get(url, params=params, timeout=timeout)
	return resp.json()

def http_post(url: str, data: Optional[Dict[str, Any]] = None, timeout: int = 5) -> Dict[str, Any]:
	resp = requests.post(url, json=data, timeout=timeout)
	return resp.json() 