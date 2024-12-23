import time
import json
import requests
import os
from datetime import datetime

class LogAnalyzer:
    def __init__(self, ollama_url="http://localhost:11434/api/generate"):
        self.ollama_url = ollama_url
        print(f"LogAnalyzer initialized with URL: {self.ollama_url}")

    def analyze_log(self, log_entry):
        prompt = f"""
        Analyze this log entry and provide severity assessment:
        ID: {log_entry['id']}
        Level: {log_entry['level']}
        Message: {log_entry['message']}
        Service: {log_entry['service']}
        
        Respond in JSON format with: severity (critical/high/medium/low), reason, and recommended_action
        """
        
        try:
            response = requests.post(
                self.ollama_url,
                json={
                    "model": "llama3",
                    "prompt": prompt,
                    "stream": False
                }
            )
            return response.json()
        except Exception as e:
            print(f"Error in analyze_log: {e}")
            return {"error": str(e)}

def monitor_logs():
    analyzer = LogAnalyzer()
    last_position = 0
    log_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs', 'system.log')
    
    print(f"Starting log monitoring on: {log_file}")
    
    while True:
        try:
            with open(log_file, 'r') as file:
                lines = file.readlines()
                
                if len(lines) > last_position:
                    print(f"\nFound {len(lines) - last_position} new log entries")
                    
                    # Process new lines
                    for i in range(last_position, len(lines)):
                        try:
                            log_entry = json.loads(lines[i].strip())
                            print(f"\n{datetime.now()} - Processing ID {log_entry['id']}: {log_entry['levelname']} - {log_entry['message']}")
                            
                            analysis_input = {
                                'id': log_entry['id'],
                                'level': log_entry['levelname'],
                                'message': log_entry['message'],
                                'service': log_entry['service']
                            }
                            
                            result = analyzer.analyze_log(analysis_input)
                            print(f"Analysis: {result}")
                            
                        except json.JSONDecodeError as e:
                            print(f"Error parsing log entry: {e}")
                        except Exception as e:
                            print(f"Error processing entry: {e}")
                    
                    last_position = len(lines)
            
            time.sleep(1)  # Check every second
            
        except Exception as e:
            print(f"Error reading log file: {e}")
            time.sleep(1)

if __name__ == "__main__":
    print("Starting log monitoring system...")
    monitor_logs()