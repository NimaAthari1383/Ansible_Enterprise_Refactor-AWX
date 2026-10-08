#!/usr/bin/env python3
import json
import os
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request

url = os.environ["AWX_URL"].rstrip("/")
token = os.environ["AWX_TOKEN"]
template_id = os.environ["AWX_JOB_TEMPLATE_ID"]

if not template_id.isdecimal() or int(template_id) < 1:
    sys.exit("Invalid AWX_JOB_TEMPLATE_ID")

expected_host = "asma-wp-test"

# Use the system's trusted CA certificates.
context = ssl.create_default_context()

def api(method, path, payload=None):
    data = None if payload is None else json.dumps(payload).encode()

    request = urllib.request.Request(
        url + path,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(
            request, timeout=20, context=context
        ) as response:
            return json.load(response)

    except urllib.error.HTTPError as exc:
        print(f"AWX HTTP error: {exc.code}", file=sys.stderr)
        sys.exit(1)

    except urllib.error.URLError as exc:
        print(f"AWX connection failed: {exc.reason}", file=sys.stderr)
        sys.exit(1)


# Verify the Job Template is tied to a dedicated inventory.
template = api("GET", f"/api/v2/job_templates/{template_id}/")

inventory_id = template.get("inventory")
if not inventory_id:
    sys.exit("Job Template has no fixed inventory")

hosts = api(
    "GET",
    f"/api/v2/inventories/{inventory_id}/hosts/?page_size=2"
)

results = hosts.get("results", [])

if hosts.get("count") != 1 or len(results) != 1:
    sys.exit("AWX inventory must contain exactly one host")

if results[0].get("name") != expected_host:
    sys.exit("AWX inventory host does not match lab target")

if not results[0].get("enabled", True):
    sys.exit("AWX inventory host is disabled")

print("AWX target validated:", expected_host, flush=True)

# Launch the Job Template using its fixed inventory.
job = api(
    "POST",
    f"/api/v2/job_templates/{template_id}/launch/",
    {}
)

if job.get("ignored_fields"):
    sys.exit("AWX reported ignored launch fields")

job_id = job.get("job")
if not job_id:
    sys.exit("AWX did not return a Job ID")

print(f"AWX Job launched: {job_id}")
print(f"AWX Job URL: {url}/#/jobs/playbook/{job_id}")
print("Job was submitted; execution success is not yet confirmed.")
