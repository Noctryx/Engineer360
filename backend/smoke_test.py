from pathlib import Path
import json
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request

BACKEND_DIR = Path(__file__).resolve().parent


def assert_ok(condition, message):
    if not condition:
        raise AssertionError(message)


def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def request_json(url, method="GET", payload=None):
    data = None
    headers = {}

    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = urllib.request.Request(url, data=data, method=method, headers=headers)

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            body = response.read().decode("utf-8")
            return response.status, json.loads(body)
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8")
        try:
            parsed = json.loads(body)
        except json.JSONDecodeError:
            parsed = {"detail": body}
        return error.code, parsed


def run_smoke_test():
    port = get_free_port()
    server = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "main:app",
            "--host",
            "127.0.0.1",
            "--port",
            str(port),
        ],
        cwd=str(BACKEND_DIR),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    base_url = f"http://127.0.0.1:{port}"

    try:
        for _ in range(30):
            try:
                status, _ = request_json(f"{base_url}/branches")
                if status == 200:
                    break
            except Exception:
                time.sleep(0.5)
        else:
            raise AssertionError("Backend did not start in time")

        branches_status, branches_data = request_json(f"{base_url}/branches")
        assert_ok(branches_status == 200, "/branches did not return 200")
        branches = branches_data.get("branches", [])
        assert_ok(isinstance(branches, list) and branches, "No branches returned")

        branch = "CSE"
        roles_status, roles_data = request_json(f"{base_url}/roles/{branch}")
        assert_ok(roles_status == 200, "/roles/{branch} did not return 200")
        roles = roles_data.get("roles", [])
        assert_ok(isinstance(roles, list) and roles, "No roles returned for CSE")

        role = "SOFTWARE_ENGINEER"
        skills_status, skills_data = request_json(f"{base_url}/skills/{role}")
        assert_ok(skills_status == 200, "/skills/{role} did not return 200")
        skills = skills_data.get("skills", {})
        assert_ok(isinstance(skills, dict) and skills, "No skills returned for SOFTWARE_ENGINEER")

        payload = {
            "name": "Smoke Test User",
            "branch": branch,
            "target_role": role,
            "skills": ["PYTHON", "GIT"],
            "sleep_hours": 7,
            "focus_score": 7,
            "stress_level": 4,
            "study_hours": 4,
        }

        analyze_status, analyze_data = request_json(f"{base_url}/analyze", method="POST", payload=payload)
        assert_ok(analyze_status == 200, "/analyze did not return 200")

        report = analyze_data
        assert_ok("skill_analysis" in report, "Missing skill_analysis in analyze response")
        assert_ok("burnout_analysis" in report, "Missing burnout_analysis in analyze response")
        assert_ok("final_recommendation" in report, "Missing final_recommendation in analyze response")
        assert_ok("learning_resources" in report, "Missing learning_resources in analyze response")

        invalid_role_status, _ = request_json(f"{base_url}/skills/NOT_A_REAL_ROLE")
        assert_ok(invalid_role_status == 404, "Invalid role should return 404")

        invalid_analyze_status, _ = request_json(
            f"{base_url}/analyze",
            method="POST",
            payload={**payload, "target_role": "NOT_A_REAL_ROLE"},
        )
        assert_ok(invalid_analyze_status == 400, "Invalid analyze request should return 400")

        print("Smoke test passed")
    finally:
        server.terminate()
        try:
            server.wait(timeout=10)
        except subprocess.TimeoutExpired:
            server.kill()
            server.wait(timeout=10)


if __name__ == "__main__":
    run_smoke_test()
