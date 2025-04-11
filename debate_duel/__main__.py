import subprocess
import sys
import os
import time
import signal
import atexit

processes = []


def kill_processes():
    """Kill all running processes."""
    for process in processes:
        try:
            if process.poll() is None:
                process.terminate()
        except Exception:
            pass


def main():
    """
    Start all services required for the Debate Duel system.
    This is for development purposes only.
    In production, each service should be deployed as a separate container.
    """
    # Register cleanup handler
    atexit.register(kill_processes)
    
    # Make sure the Python executable is the one from the venv
    python = sys.executable
    
    # Define services to start
    services = [
        {"name": "Arena", "module": "debate_duel.arena", "port": 8000},
        {"name": "Swarm A (Pro)", "module": "debate_duel.agents.swarm_a", "port": 8001},
        {"name": "Swarm B (Con)", "module": "debate_duel.agents.swarm_b", "port": 8002},
        {"name": "Judge", "module": "debate_duel.agents.judge", "port": 8003},
    ]
    
    for service in services:
        cmd = [python, "-m", service["module"]]
        env = os.environ.copy()
        env["PORT"] = str(service["port"])
        
        print(f"Starting {service['name']} on port {service['port']}...")
        process = subprocess.Popen(cmd, env=env)
        processes.append(process)
        
        # Wait a bit to let the service start
        time.sleep(1)
    
    print("\nAll services started. Press Ctrl+C to stop all services.")
    
    try:
        # Keep the main process running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping all services...")
        kill_processes()


if __name__ == "__main__":
    main() 