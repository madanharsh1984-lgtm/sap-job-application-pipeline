#!/usr/bin/env python3
# =============================================================================
# run_admin.py — Launch the Admin Portal Server
# =============================================================================
# Usage:
#   python run_admin.py
#   ADMIN_JWT_SECRET=your-secret python run_admin.py
# =============================================================================

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from admin_portal.app import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("ADMIN_PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"
    print(f"\n{'='*60}")
    print(f"  SAP Job Application Pipeline — Admin Portal")
    print(f"  URL: http://localhost:{port}")
    print(f"  Debug: {debug}")
    print(f"{'='*60}\n")
    app.run(host="0.0.0.0", port=port, debug=debug)
