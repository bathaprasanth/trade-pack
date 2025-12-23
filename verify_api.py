import requests
import time
import sys

BASE_URL = "http://127.0.0.1:8002"
API_KEY = "gemini-trade-api"

def test_root():
    """Test the root endpoint."""
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("[OK] Root endpoint accessible.")
        else:
            print(f"[FAIL] Root endpoint failed with {response.status_code}")
    except Exception as e:
        print(f"[FAIL] Root endpoint connection failed: {e}")
        sys.exit(1)

def test_auth():
    """Test authentication mechanisms."""
    print("\nTesting Authentication...")
    # Test without key
    response = requests.get(f"{BASE_URL}/analyze/tech")
    if response.status_code == 403:
        print("[OK] Auth enforcement (Missing Key): Passed (403)")
    else:
        print(f"[FAIL] Auth enforcement (Missing Key): Failed ({response.status_code})")

    # Test with wrong key
    response = requests.get(f"{BASE_URL}/analyze/tech", headers={"X-API-Key": "wrong-key"})
    if response.status_code == 403:
        print("[OK] Auth enforcement (Wrong Key): Passed (403)")
    else:
        print(f"[FAIL] Auth enforcement (Wrong Key): Failed ({response.status_code})")

def test_analysis():
    """Test the analysis endpoint with valid key."""
    print("\nTesting Analysis Endpoint...")
    headers = {"X-API-Key": API_KEY}
    
    response = requests.get(f"{BASE_URL}/analyze/technology", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if "analysis_report" in data:
            print("[OK] Analysis request successful.")
            print("Report Preview:", data["analysis_report"][:100].replace("\n", " "))
        else:
            print("[FAIL] Analysis response missing report field.")
    else:
        print(f"[FAIL] Analysis request failed: {response.status_code} - {response.text}")

def test_rate_limit():
    """Test rate limiting (5 per minute)."""
    print("\nTesting Rate Limiting...")
    headers = {"X-API-Key": API_KEY}
    
    limit_hit = False
    for i in range(6):
        response = requests.get(f"{BASE_URL}/analyze/rate_test_{i}", headers=headers)
        if response.status_code == 429:
            print("[OK] Rate limit hit (429 Too Many Requests).")
            limit_hit = True
            break
        time.sleep(0.2)
    
    if not limit_hit:
        print("[WARN] Rate limit might not have been triggered.")

if __name__ == "__main__":
    print("Wait for server to start...")
    time.sleep(5) # Give uvicorn time to startup if running in parallel
    test_root()
    test_auth()
    test_analysis()
    test_rate_limit()
