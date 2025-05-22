"""
Run script for the Market Research Crew Web Interface
"""
import os
import sys
import webbrowser
from app import app, socketio

def main():
    """
    Main entry point to run the web interface.
    """
    print("=" * 70)
    print("Market Research Crew - Web Interface")
    print("=" * 70)
    print("Starting server on http://localhost:5000")
    print("Opening browser...")
    
    # Try to open the browser after a slight delay
    try:
        import threading
        import time
        threading.Timer(1.5, lambda: webbrowser.open('http://localhost:5000')).start()
    except Exception as e:
        print(f"Could not open browser automatically: {e}")
        print("Please manually navigate to http://localhost:5000 in your browser")
    
    # Create necessary directories if they don't exist
    for directory in ['templates', 'static', 'reports']:
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    # Run the Flask server
    try:
        socketio.run(app, debug=False, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\nShutting down server...")
        return 0
    except Exception as e:
        print(f"\nError running web server: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 