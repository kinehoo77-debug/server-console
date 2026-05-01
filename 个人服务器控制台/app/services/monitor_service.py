from __future__ import annotations

import os
import platform
import socket
import time
from datetime import datetime

import psutil


class MonitorService:
    boot_time = psutil.boot_time()

    @staticmethod
    def get_system_info() -> dict:
        hostname = socket.gethostname()
        ip_addr = MonitorService._best_ip()
        uptime_seconds = int(time.time() - MonitorService.boot_time)
        return {
            "hostname": hostname,
            "ip": ip_addr,
            "os": f"{platform.system()} {platform.release()}",
            "version": platform.version(),
            "uptime": MonitorService._format_duration(uptime_seconds),
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "load": MonitorService._load_avg(),
        }

    @staticmethod
    def get_metrics() -> dict:
        vm = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        net = psutil.net_io_counters()
        return {
            "timestamp": int(time.time() * 1000),
            "cpu_percent": round(psutil.cpu_percent(interval=None), 2),
            "memory_percent": round(vm.percent, 2),
            "memory_used": vm.used,
            "memory_total": vm.total,
            "disk_percent": round(disk.percent, 2),
            "disk_used": disk.used,
            "disk_total": disk.total,
            "net_sent": net.bytes_sent,
            "net_recv": net.bytes_recv,
        }

    @staticmethod
    def _best_ip() -> str:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.connect(("8.8.8.8", 80))
            ip = sock.getsockname()[0]
            sock.close()
            return ip
        except OSError:
            return "127.0.0.1"

    @staticmethod
    def _format_duration(seconds: int) -> str:
        days, rem = divmod(seconds, 86400)
        hours, rem = divmod(rem, 3600)
        mins, secs = divmod(rem, 60)
        if days > 0:
            return f"{days}d {hours:02}:{mins:02}:{secs:02}"
        return f"{hours:02}:{mins:02}:{secs:02}"

    @staticmethod
    def _load_avg() -> str:
        if hasattr(os, "getloadavg"):
            a, b, c = os.getloadavg()
            return f"{a:.2f}, {b:.2f}, {c:.2f}"
        return "-"
