# system_utils.py
import psutil
import platform
import time
import os

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g: 1253656 => '1.20MB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def get_system_report():
    """
    Generates a professional-grade system report for the Sudo Menu.
    """
    uname = platform.uname()
    cpufreq = psutil.cpu_freq()
    svmem = psutil.virtual_memory()
    
    report = (
        "🏮 **KURAMA SYSTEM VITALS** 🏮\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"🖥️ **Node:** `{uname.node}`\n"
        f"🛡️ **OS:** `{uname.system} {uname.release}`\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "🧠 **PROCESSOR (CHAKRA FLOW)**\n"
        f"• **Physical cores:** {psutil.cpu_count(logical=False)}\n"
        f"• **Total cores:** {psutil.cpu_count(logical=True)}\n"
        f"• **Current Freq:** {cpufreq.current:.2f}Mhz\n"
        f"• **CPU Load:** {psutil.cpu_percent()}% \n"
        "━━━━━━━━━━━━━━━━━━\n"
        "💧 **MEMORY (STAMINA)**\n"
        f"• **Total:** {get_size(svmem.total)}\n"
        f"• **Available:** {get_size(svmem.available)}\n"
        f"• **Used:** {get_size(svmem.used)} ({svmem.percent}%)\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "⌛ **UPTIME:** " + time.strftime("%Hh %Mm %Ss", time.gmtime(time.time() - psutil.boot_time())) + "\n"
        "━━━━━━━━━━━━━━━━━━"
    )
    return report
