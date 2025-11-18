#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════
INFINITE SERVER26 - Health Check Service
═══════════════════════════════════════════════════════════════════

Simple health check HTTP service for container monitoring
Usage: python3 health-check.py [port]

Built by: NaTo1000
Version: 26.1
═══════════════════════════════════════════════════════════════════
"""

import sys
import json
import time
import socket
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000

class HealthCheckHandler(BaseHTTPRequestHandler):
    """Simple health check endpoint handler"""
    
    def log_message(self, format, *args):
        """Override to reduce logging noise"""
        pass
    
    def do_GET(self):
        """Handle GET requests"""
        
        if self.path == '/health' or self.path == '/':
            # Health check endpoint
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            health_data = {
                'status': 'healthy',
                'service': 'Infinite Server26 Fortress',
                'version': '26.1',
                'codename': 'FORTRESS',
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'hostname': socket.gethostname(),
                'uptime': time.time(),
                'components': {
                    'naydoev1': 'operational',
                    'jessicai': 'hunting',
                    'nai_gail': 'shielding',
                    'nia_vault': 'encrypting',
                    'rancher': 'orchestrating'
                },
                'security': {
                    'level': 'MAXIMUM',
                    'mercy_mode': 'DISABLED',
                    'auto_defense': 'ENABLED'
                }
            }
            
            self.wfile.write(json.dumps(health_data, indent=2).encode())
            
        elif self.path == '/ready':
            # Readiness probe
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            ready_data = {
                'ready': True,
                'message': 'Fortress is ready to defend'
            }
            
            self.wfile.write(json.dumps(ready_data, indent=2).encode())
            
        elif self.path == '/live':
            # Liveness probe
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            live_data = {
                'alive': True,
                'message': 'Fortress is alive and defending'
            }
            
            self.wfile.write(json.dumps(live_data, indent=2).encode())
            
        else:
            # 404 for unknown paths
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            error_data = {
                'error': 'Not Found',
                'message': 'Available endpoints: /health, /ready, /live'
            }
            
            self.wfile.write(json.dumps(error_data, indent=2).encode())

def run_server():
    """Start the health check server"""
    server = HTTPServer(('0.0.0.0', PORT), HealthCheckHandler)
    
    print("═" * 70)
    print("  INFINITE SERVER26 - HEALTH CHECK SERVICE")
    print("═" * 70)
    print(f"  Status: ONLINE")
    print(f"  Port: {PORT}")
    print(f"  Endpoints:")
    print(f"    - http://localhost:{PORT}/health  (Health check)")
    print(f"    - http://localhost:{PORT}/ready   (Readiness probe)")
    print(f"    - http://localhost:{PORT}/live    (Liveness probe)")
    print("═" * 70)
    print("  Press Ctrl+C to stop")
    print("═" * 70)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\nShutting down health check service...")
        server.shutdown()

if __name__ == '__main__':
    run_server()
