import requests
import time

class Monitor:
    """
    Singularity AGI Monitor Module (Phase 4)
    Tracks the health, uptime, and performance of deployed apps.
    """
    
    def __init__(self):
        self.monitored_apps = {}

    def add_app(self, name: str, url: str):
        """
        Adds a new app to the monitoring list.
        """
        print(f"[*] Started monitoring: {name} ({url})")
        self.monitored_apps[name] = {
            "url": url,
            "status": "Initializing",
            "last_check": None,
            "uptime": 100.0,
            "latency": 0
        }

    def check_health(self, name: str) -> dict:
        """
        Checks the HTTP status and latency of a specific app.
        """
        app = self.monitored_apps.get(name)
        if not app:
            return {"error": "App not found."}

        try:
            start_time = time.time()
            response = requests.get(app["url"], timeout=10)
            latency = int((time.time() - start_time) * 1000)
            
            status = "Healthy" if response.status_code == 200 else f"Error ({response.status_code})"
            
            # Update app status
            app["status"] = status
            app["latency"] = latency
            app["last_check"] = time.strftime("%Y-%m-%d %H:%M:%S")
            
            return {
                "name": name,
                "url": app["url"],
                "status": status,
                "latency": f"{latency}ms",
                "last_check": app["last_check"]
            }
        except Exception as e:
            app["status"] = "Down"
            return {"name": name, "status": "Down", "error": str(e)}

    def get_dashboard_summary(self) -> list:
        """
        Returns a summary for the Next.js dashboard.
        """
        summary = []
        for name in self.monitored_apps:
            summary.append(self.check_health(name))
        return summary
