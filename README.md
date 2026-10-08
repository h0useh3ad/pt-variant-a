# pt-variant-a — Variant A (Detectable)

## Package Information

- **Name**: `pt-variant-a` (import `pt_variant_a`)
- **Version**: 1.1.0
- **Detection Level**: Easy (detectable — by design)
- **Purpose**: Purple team testing — demonstrates a package with verbose, obvious activity

## Characteristics

- Verbose console logging (`[pt-variant-a] ...`)
- Immediate execution on import (no delay)
- Harvests 19 sensitive environment variables (Vault, AWS, GitHub, Artifactory, DB, API keys, Azure, DigitalOcean)
- Queries GCP and AWS metadata services
- Plaintext beacon URL
- Synchronous execution

## What It Harvests

19 environment variables (Vault, AWS, GitHub, Artifactory, DB, API keys, Azure,
DigitalOcean), GCP + AWS metadata, and — via path-following — the contents of
`GOOGLE_APPLICATION_CREDENTIALS` (full service-account key JSON) and
`VAULT_TOKEN_FILE` (ephemeral Vault token) when those files exist.

## Deployment (Test Case 4)

**Pattern 1 — deploy-time (GCP host)**: the `demo-app-py-wheel` pipeline fetches the
wheel from Artifactory (`pt_team-pypi-local`), the `pt_pkg` Ansible role installs it
from the local file on the host, and the verify task imports it.
Trigger with `VERSION=pt-variant-a`.

**Pattern 2 — build-time (Jenkins agent)**: the `demo-app-py-sdist` pipeline installs
the package from GitHub (`git+https://github.com/h0useh3ad/pt-variant-a.git@v1.1.0`)
in the build pod and imports it there, harvesting the build-time credential files.
Trigger with `VERSION=pt-variant-a` and `TERRAFORM_COMMAND=skip`.

## Manual Test (any host with the wheel)

```bash
pip3 install --no-index pt_variant_a-1.0.0-py3-none-any.whl
python3 -c "import pt_variant_a"
```

Beacon: `https://collector.purple-test.com/0cfd83d5d513beae/beacon` — immediate, with
`[pt-variant-a]` log lines visible in the console where the import ran.

**Authorization Required**: Use only on systems where you have written authorization.
