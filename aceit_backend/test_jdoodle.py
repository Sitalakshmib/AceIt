"""
Quick test script to verify JDoodle API connectivity for all 4 languages.
Run with: python test_jdoodle.py
"""
import os
import sys
import requests
from dotenv import load_dotenv

# Force UTF-8 output so Windows terminal doesn't choke
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

CLIENT_ID     = os.environ.get("JDOODLE_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("JDOODLE_CLIENT_SECRET", "")
API_URL       = "https://api.jdoodle.com/v1/execute"

if not CLIENT_ID or CLIENT_ID == "your_jdoodle_client_id_here":
    print("[FAIL] JDOODLE_CLIENT_ID is not set in .env -- please add your real credentials.")
    exit(1)
if not CLIENT_SECRET or CLIENT_SECRET == "your_jdoodle_client_secret_here":
    print("[FAIL] JDOODLE_CLIENT_SECRET is not set in .env -- please add your real credentials.")
    exit(1)

print(f"[OK] Credentials loaded: client_id={CLIENT_ID[:6]}...")

# -- Test cases ---------------------------------------------------------------
TESTS = [
    {
        "name": "Java",
        "language": "java",
        "versionIndex": "4",
        "script": """
public class Main {
    public static void main(String[] args) {
        System.out.println("{\\"passed\\":1,\\"total\\":1,\\"results\\":[]}");
    }
}
""",
    },
    {
        "name": "C",
        "language": "c",
        "versionIndex": "5",
        "script": r"""
#include <stdio.h>
int main() {
    printf("{\"passed\":1,\"total\":1,\"results\":[]}\n");
    return 0;
}
""",
    },
    {
        "name": "C++",
        "language": "cpp17",
        "versionIndex": "0",
        "script": r"""
#include <iostream>
using namespace std;
int main() {
    cout << "{\"passed\":1,\"total\":1,\"results\":[]}" << endl;
    return 0;
}
""",
    },
    {
        "name": "R",
        "language": "r",
        "versionIndex": "3",
        "script": """
cat('{"passed":1,"total":1,"results":[]}\\n')
""",
    },
]

# -- Run tests ----------------------------------------------------------------
all_passed = True
for t in TESTS:
    payload = {
        "clientId": CLIENT_ID,
        "clientSecret": CLIENT_SECRET,
        "script": t["script"],
        "language": t["language"],
        "versionIndex": t["versionIndex"],
    }
    try:
        resp = requests.post(API_URL, json=payload, timeout=25)
        data = resp.json()
        output = data.get("output", "").strip()
        status = data.get("statusCode", resp.status_code)

        if resp.status_code == 200 and status == 200 and output:
            print(f"[OK]   {t['name']:6s} -> output: {output[:80]}")
        else:
            print(f"[FAIL] {t['name']:6s} -> HTTP {resp.status_code} | statusCode={status} | output={output[:200]}")
            all_passed = False
    except Exception as e:
        print(f"[FAIL] {t['name']:6s} -> Exception: {e}")
        all_passed = False

print()
if all_passed:
    print("[DONE] All 4 languages (Java, C, C++, R) are working with JDoodle!")
else:
    print("[WARN] Some tests failed -- check the output above.")
