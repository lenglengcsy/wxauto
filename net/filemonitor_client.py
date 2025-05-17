#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import argparse
import sys
import time
from typing import Dict, Any, Optional, Union, List

class FileMonitorClient:
	"""FileMonitor HTTP客户端，用于向注入端发送命令"""
	
	def __init__(self, host: str = "localhost", port: int = 8080, timeout: int = 10) -> None:
		"""
		初始化客户端
		
		Args:
			host: 服务器主机名或IP
			port: 服务器端口
			timeout: 请求超时时间(秒)
		"""
		self.base_url = f"http://{host}:{port}"
		self.timeout = timeout
		self.stats: Dict[str, List[float]] = {"command": [], "status": []}
	
	def send_command(self, command: str, verbose: bool = True) -> Dict[str, Any]:
		"""
		发送命令到注入端
		
		Args:
			command: 要执行的命令
			verbose: 是否输出详细信息
			
		Returns:
			响应的JSON数据
		
		Raises:
			requests.RequestException: 请求失败时抛出
		"""
		url = f"{self.base_url}/api/command"
		payload = {"command": command}
		
		headers = {
			"Content-Type": "application/json",
			"Accept": "application/json",
			"User-Agent": "FileMonitorClient/1.0"
		}
		
		if verbose:
			print(f"正在发送命令 '{command}' 到 {url}...")
		
		start_time = time.time()
		
		# 使用一次性会话发送请求
		with requests.Session() as session:
			response = session.post(
				url, 
				json=payload, 
				headers=headers, 
				timeout=self.timeout
			)
		
		elapsed = time.time() - start_time
		self.stats["command"].append(elapsed)
		
		if verbose:
			print(f"请求耗时: {elapsed:.3f}秒")
		
		response.raise_for_status()
		result = response.json()
		
		if verbose and "elapsedMs" in result:
			print(f"服务端处理耗时: {result['elapsedMs']}毫秒")
			
		return result
	
	def get_status(self, verbose: bool = True) -> Dict[str, Any]:
		"""
		获取服务器状态
		
		Args:
			verbose: 是否输出详细信息
			
		Returns:
			状态信息的JSON数据
		
		Raises:
			requests.RequestException: 请求失败时抛出
		"""
		url = f"{self.base_url}/api/status"
		
		headers = {
			"Accept": "application/json",
			"User-Agent": "FileMonitorClient/1.0"
		}
		
		if verbose:
			print(f"获取服务器状态...")
		
		start_time = time.time()
		
		# 使用一次性会话发送请求
		with requests.Session() as session:
			response = session.get(
				url, 
				headers=headers, 
				timeout=self.timeout
			)
		
		elapsed = time.time() - start_time
		self.stats["status"].append(elapsed)
		
		if verbose:
			print(f"状态请求耗时: {elapsed:.3f}秒")
		
		response.raise_for_status()
		return response.json()
	
	def print_stats(self) -> None:
		"""输出性能统计信息"""
		if not self.stats["command"] and not self.stats["status"]:
			print("没有统计数据")
			return
			
		print("\n性能统计:")
		if self.stats["command"]:
			cmd_times = self.stats["command"]
			print(f"  命令请求: {len(cmd_times)}次")
			print(f"  平均耗时: {sum(cmd_times)/len(cmd_times):.3f}秒")
			print(f"  最小耗时: {min(cmd_times):.3f}秒")
			print(f"  最大耗时: {max(cmd_times):.3f}秒")
			
		if self.stats["status"]:
			status_times = self.stats["status"]
			print(f"  状态请求: {len(status_times)}次")
			print(f"  平均耗时: {sum(status_times)/len(status_times):.3f}秒")
			
		print("")

def main() -> None:
	"""主函数"""
	parser = argparse.ArgumentParser(description="FileMonitor HTTP客户端")
	parser.add_argument("--host", default="localhost", help="服务器主机名或IP (默认: localhost)")
	parser.add_argument("--port", type=int, default=8080, help="服务器端口 (默认: 8080)")
	parser.add_argument("--timeout", type=int, default=10, help="请求超时时间(秒) (默认: 10)")
	parser.add_argument("--quiet", "-q", action="store_true", help="静默模式，减少输出")
	parser.add_argument("--benchmark", "-b", action="store_true", help="基准测试模式")
	parser.add_argument("--status", action="store_true", help="获取服务器状态")
	parser.add_argument("command", nargs="?", help="要执行的命令")
	
	args = parser.parse_args()
	
	# 创建客户端实例
	client = FileMonitorClient(args.host, args.port, args.timeout)
	verbose = not args.quiet
	
	try:
		if args.benchmark:
			print("开始基准测试模式...")
			test_commands = ["dir", "echo hello", "help", "echo test"]
			iterations = 5
			
			print(f"将对每个命令执行{iterations}次测试")
			for cmd in test_commands:
				print(f"\n测试命令: {cmd}")
				for i in range(iterations):
					try:
						start = time.time()
						result = client.send_command(cmd, verbose=False)
						elapsed = time.time() - start
						success = result.get("success", False)
						status = "成功" if success else "失败"
						server_time = result.get("elapsedMs", 0)
						print(f"  [{i+1}/{iterations}] {status} - 总耗时: {elapsed:.3f}秒, 服务端处理: {server_time}毫秒")
						time.sleep(0.5)  # 防止请求过于频繁
					except Exception as e:
						print(f"  [{i+1}/{iterations}] 错误: {e}")
						
			client.print_stats()
			return
			
		elif args.status:
			# 获取状态
			status = client.get_status(verbose)
			if verbose:
				print("\n服务器状态:")
				print(json.dumps(status, indent=2, ensure_ascii=False))
		elif args.command:
			# 发送命令
			result = client.send_command(args.command, verbose)
			
			if verbose:
				print("\n命令执行结果:")
				if result.get("success"):
					print(f"成功: {result.get('result', '')}")
				else:
					print(f"失败: {result.get('result', '')}")
		else:
			# 交互模式
			print(f"连接到 {args.host}:{args.port} 的FileMonitor服务器")
			print("输入 'exit' 或 Ctrl+C 退出，'status' 获取状态，'stats' 查看性能统计")
			
			while True:
				try:
					command = input("\n请输入命令: ")
					if command.lower() == "exit":
						break
					elif command.lower() == "status":
						status = client.get_status(verbose)
						print(json.dumps(status, indent=2, ensure_ascii=False))
					elif command.lower() == "stats":
						client.print_stats()
					elif command.strip():
						result = client.send_command(command, verbose)
						if result.get("success"):
							print(f"成功: {result.get('result', '')}")
						else:
							print(f"失败: {result.get('result', '')}")
				except KeyboardInterrupt:
					print("\n退出程序")
					break
				except requests.Timeout:
					print(f"错误: 请求超时 (超过{client.timeout}秒)")
				except requests.ConnectionError:
					print("错误: 连接失败，服务器可能未运行")
				except Exception as e:
					print(f"错误: {e}")
	except requests.Timeout:
		print(f"错误: 请求超时 (超过{client.timeout}秒)", file=sys.stderr)
		sys.exit(1)
	except requests.ConnectionError:
		print("错误: 连接失败，服务器可能未运行", file=sys.stderr)
		sys.exit(1)
	except requests.RequestException as e:
		print(f"请求错误: {e}", file=sys.stderr)
		sys.exit(1)
	except json.JSONDecodeError:
		print("错误: 无法解析服务器返回的JSON数据", file=sys.stderr)
		sys.exit(1)
	except Exception as e:
		print(f"未知错误: {e}", file=sys.stderr)
		sys.exit(1)
	finally:
		if verbose and (args.command or args.status):
			client.print_stats()

if __name__ == "__main__":
	main() 