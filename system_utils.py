# system_utils.py
import platform
import os
import subprocess

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

def get_system_report():
    """Generates a report that won't crash on Termux."""
    uname = platform.uname()
    
    # Basic Info (Works everywhere)
    report = (
        "🌌 <b>COSMIC VITALS</b> 🏮\n"
        "━━━━━━━━━━━━━━\n"
        f"🖥️ <b>OS:</b> {uname.system}\n"
        f"🆔 <b>Node:</b> {uname.node}\n"
        f"🏗️ <b>Arch:</b> {uname.machine}\n"
    )

    if HAS_PSUTIL:
        try:
            cpu_usage = psutil.cpu_percent()
            mem = psutil.virtual_memory()
            report += (
                f"🧠 <b>CPU:</b> {cpu_usage}%\n"
                f"💾 <b>RAM:</b> {mem.percent}%\n"
            )
        except Exception:
            report += "🧠 <b>CPU/RAM:</b> Access Restricted\n"
    else:
        # Termux Fallback: Use 'free' command if available
        try:
            report += "🧠 <b>CPU/RAM:</b> psutil missing (Termux restricted)\n"
        except Exception:
            pass

    report += "━━━━━━━━━━━━━━"
    return report
