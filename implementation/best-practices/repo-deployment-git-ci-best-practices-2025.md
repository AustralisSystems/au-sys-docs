# Repository Deployment, Git & CI Best Practices (2025)

**Version:** 1.0.0  •  **Last Updated:** 2026-01-03

This document consolidates the project's operational best practices covering: Git & GitHub conventions, Make & dependency management, Docker & BuildKit, docker-compose, CI/CD workflows, artifacts (SBOM/wheelhouse), signing, scanning, and how to replicate the setup across repositories.

Audience: maintainers, release engineers, platform/security teams, and repo owners who need a reusable, auditable standard for building and deploying Python containerized apps.

---

## Principles (short) ✅
- Reproducible builds: pin base images and dependencies; store wheel artifacts and SBOMs. 🔁
- Minimal runtime images: compile/build in a builder stage, remove build tools from runtime. 🧱
- Supply-chain hygiene: generate SBOMs, sign images (cosign), enforce vulnerability scanning (Trivy/pip-audit). 🔒
- Secure defaults: avoid `curl | sh` patterns, require checksums for third-party installers, use secrets for credentials. 🚫
- Clear DX: document CI flows and local validation steps so others can replicate quickly. 📋

---

## Files & structure to include (canonical template) 📁
- `Dockerfile` (builder & runtime stages, BuildKit mounts, healthcheck, non-root user)
- `requirements.in`, `requirements.lock.txt` (pin with `pip-compile --generate-hashes`)
- `Makefile` with `lock-deps`/`regen-pins` targets
- `.github/workflows/build-and-push-container.yml` (build + SBOM + sign + scans + wheelhouse upload)
- `.github/workflows/cd-*.yml` (deploy & verify signatures prior to production deploy)
- `.github/workflows/regen-pins.yml` (optional automated pin refresh)
- `.github/workflows/README.md` — short, actionable guide for maintainers
- `docker-compose.*.yml` (dev & production variants with env_file usage)
- `.env.example` (dev defaults, no secrets)
- `docs/GIT_AND_CI_README.md` — developer guide + validation commands

---

## Git & GitHub conventions ✳️
- Branch naming: `feature/*`, `fix/*`, `chore/*`. Keep names short and descriptive.
- PRs: include purpose, testing notes, and the CI run URL. Use Conventional Commits (e.g., `feat:`, `fix:`).
- Protected branches: `main` and `production` protected with required status checks (build, scans, tests) and required reviewers.
- CODEOWNERS: set for critical paths to ensure correct reviewers.
- Secrets: store in GitHub Secrets; never commit private keys or `.env` with secrets.
- Tagging: `v<major>.<minor>.<patch>`; tags trigger release/CD workflows.

---

## Makefile & dependency workflow 🛠
- Track direct deps in `requirements.in`.
- Use `pip-tools`/`pip-compile` to produce `requirements.lock.txt` with hashes:
  - `python -m pip install --upgrade pip pip-tools`
  - `python -m piptools.scripts.compile --generate-hashes --output-file=requirements.lock.txt requirements.in`
- Add targets:
  - `lock-deps`: generate hashed lock file
  - `regen-pins`: commit the new lock file (CI may run this via a scheduled job)
- Store a pre-built wheelhouse artifact in CI or an artifact storage to reduce resolver work during builds.

---

## Docker & image build best practices (BuildKit) 🐳
- Use BuildKit (`# syntax=docker/dockerfile:1.7`) and `docker buildx` for multi-arch and caching.
- Use a builder stage to compile wheels and build native extensions; copy only wheels / installed site-packages to final runtime.
- Prefer pinned base image digests in production: `FROM python:3.12-slim@sha256:<digest>`.
- Use cache mounts: `/root/.cache/pip`, `/var/cache/apt`, and `/wheels`.
- Do not keep build deps (gcc, python3-dev, build-essential) in runtime image. Remove or keep them in builder stage.
- Set secure Python environment envs: `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUNBUFFERED=1`, `PIP_NO_CACHE_DIR=1`, `PIP_DISABLE_PIP_VERSION_CHECK=1`.
- Add non-root `appuser` and set ownership of runtime directories.
- Expose only required ports; include `HEALTHCHECK`.
- Avoid `curl | sh`; if unavoidable, require a checksum via build-arg (e.g., `AZURE_CLI_INSTALLER_SHA256`) and verify it in the Dockerfile.
- Use `pip wheel --wheel-dir=/wheels -r requirements.lock.txt` in builder stage, `pip install --no-index --find-links /wheels -r requirements.lock.txt` in runtime.

Example small pattern (builder → runtime):
```dockerfile
# Builder
FROM python:3.12-slim AS builder
COPY requirements.lock.txt /build/
RUN python -m pip wheel --wheel-dir=/wheels -r requirements.lock.txt

# Runtime
FROM python:3.12-slim
COPY --from=builder /wheels /wheels
RUN python -m pip install --no-index --find-links /wheels -r requirements.lock.txt
```

---

## CI flow standard (Build & Push) ⚙️
Minimum CI job steps (in `build-and-push-container.yml`):
1. Checkout & static checks (grep problematic patterns e.g., `curl | sh`).
2. Build wheelhouse artifact (download wheels from lock file) and upload as `wheelhouse-${IMAGE_TAG}`.
Example `prepare-wheels` job (CI) — grouped wheelhouses & fail-fast:
```yaml
jobs:
  prepare-wheels:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'

      - name: Generate locked `requirements.lock.txt`
        run: |
          python -m pip install --upgrade pip pip-tools setuptools wheel
          python -m piptools.scripts.compile --generate-hashes --output-file=requirements.lock.txt requirements.in

      - name: Build core wheelhouse (required)
        run: |
          mkdir -p wheels-core wheels
          HEAVY='(azure|google|msgraph|opentelemetry|grpc|protobuf|opencv|pillow|pdf|platformdirs|microsoft-kiota|pyasn1|pyasn1-modules|kiota|mistralai|fastmcp|langgraph|kubernetes|google-auth)'
          grep -E -v "$HEAVY" requirements.lock.txt > requirements.core.txt || true
          python -m pip wheel --wheel-dir=wheels-core -r requirements.core.txt

      - name: Upload core wheelhouse artifact
        uses: actions/upload-artifact@v4
        with:
          name: wheelhouse-core-${{ github.sha }}
          path: wheels-core/

      - name: Build heavy wheelhouse (best-effort)
        run: |
          mkdir -p wheels-heavy
          HEAVY='(azure|google|msgraph|opentelemetry|grpc|protobuf|opencv|pillow|pdf|platformdirs|microsoft-kiota|pyasn1|pyasn1-modules|kiota|mistralai|fastmcp|langgraph|kubernetes|google-auth)'
          grep -E "$HEAVY" requirements.lock.txt > requirements.heavy.txt || true
          set +e
          python -m pip wheel --wheel-dir=wheels-heavy -r requirements.heavy.txt || true
          set -e

      - name: Upload heavy wheelhouse artifact (if any)
        uses: actions/upload-artifact@v4
        with:
          name: wheelhouse-heavy-${{ github.sha }}
          path: wheels-heavy/
```
3. Build & push Docker image (Buildx, cache-from/ cache-to).
4. Generate image SBOM (e.g., `syft`) and upload `sbom-${IMAGE_TAG}`.
5. (Optional) Sign image with `cosign` (`COSIGN_PRIVATE_KEY` secret) after push.
6. Vulnerability scanning: Trivy image & filesystem (SARIF upload), and `pip-audit` for Python dependencies.
7. Upload scan artifacts for triage.

CI best-practices:
- Fail on `HIGH`/`CRITICAL` by default, or use policy-controlled thresholds.
- Keep artifacts (SBOM, Trivy SARIF, wheelhouse) retained for X days (e.g., 90).
- Provide a post-push optional signing step: support keyless cosign or KMS-backed cosign.
- Provide a separate `cd-*.yml` deploy workflow that verifies image signature before production deploy.

Snippet: Cosign sign & verify
```yaml
- name: Sign image
  run: cosign sign --key cosign.key $IMAGE

- name: Verify signature
  run: cosign verify --key cosign.pub $IMAGE
```

---

## SBOM, signing & scanning (supply chain hygiene) 🔎
- Generate SBOM during CI using `syft` (or `trivy sbom`) and store artifacts.
- Sign images using `cosign`; store verification public key in `COSIGN_PUBKEY` for deployment verification.
- Run vulnerability scanners: Trivy (image & fs) and `pip-audit` for Python dependencies; upload results as SARIF and raw JSON for triage.
- Add a static detector step that fails PRs if unapproved remote install patterns exist.

---

## Docker-Compose & local dev vs prod patterns 🧩
- Use `env_file: - .env` as the single source of truth for configuration.
- Do not commit `.env` with secrets; include `.env.example` for templates.
- Separate local/dev compose files and production compose files (avoid bind-mounts in production composition). For example:
  - `docker-compose.standalone.yml` – production-minded single-instance compose (no source mounts).
  - `docker-compose.dev.yml` – mounts source for local development.
- Include healthchecks and resource limits; use `deploy.resources` if Docker Swarm or Compose v3+ supports it.
- Prefer Docker secrets or platform secret managers for production secrets.

---

## Replication & templating checklist (how to apply to another repo) 🧾
1. Copy templates into target repo:
   - `Dockerfile` (builder/runtime pattern), `docker-compose.standalone.yml`.
   - `.github/workflows/build-and-push-container.yml` and `cd-*.yml`.
   - `Makefile` with `lock-deps`.
   - `.env.example` and `README` (developer guide).
2. Set up GitHub secrets: `AZURE_*`/`REGISTRY_*`, `COSIGN_PRIVATE_KEY` & `COSIGN_PASSWORD` (if signing), `COSIGN_PUBKEY`.
3. Run `make lock-deps` locally, verify `pip-compile` output, and populate `requirements.lock.txt` (store in repo).
4. Test local build: `DOCKER_BUILDKIT=1 docker build --progress=plain -t app-local .`
5. Push branch to trigger CI; validate wheelhouse artifact, SBOM, and Trivy/pip-audit steps.
6. Adjust thresholds & policies (Trivy severities, signing enforcement) per team policy.

---

## Secrets & production readiness checklist ✅
- All production secrets stored in GitHub Secrets or cloud KMS (don’t embed into repo).
- `COSIGN_PUBKEY` present for deploy verification.
- `AZURE_*` / registry credentials present for push.
- `AZURE_CLI_INSTALLER_SHA256` build-arg must be provided when `INSTALL_AZURE_CLI=true`.
- Verify that the production `docker-compose` or orchestrator does not mount source code and uses secrets.

---

## Local validation quick commands (copy into README or docs) 🧪
- Build image: `DOCKER_BUILDKIT=1 docker build --progress=plain -t app-standalone:local .`
- Build wheelhouse: `python -m pip download --dest wheels -r requirements.lock.txt`
- Generate SBOM: `docker run --rm -v /var/run/docker.sock:/var/run/docker.sock anchore/syft:latest app-standalone:local -o spdx-json > sbom-image.spdx.json`
- Scan image: `trivy image --format table --severity CRITICAL,HIGH app-standalone:local`
- Sign (requires keys): `cosign sign --key cosign.key app-standalone:local` and `cosign verify --key cosign.pub app-standalone:local`

---

## Governance & rollout notes 📝
- When enabling signing verification: initially run as advisory (warn-only) for one release cycle, then enforce verification for production deployments.
- Schedule regular pin-regeneration (weekly/monthly) with `regen-pins.yml`, review for incompatibilities and involve break-fix team for runtime regressions.
- Retain SBOMs and scan reports for audit for a minimum of 90 days.

---

## References & templates
- See `docs/implementation/best-practices/docker-containerization-best-practices-2025.md` for extended Docker patterns and examples.
- See `.github/workflows/build-and-push-container.yml` and `docs/GIT_AND_CI_README.md` for CI and developer procedures used in this repo.

---

## Contribution & updates
To propose improvements to this document: open a PR describing the change, link CI/Build evidence, and add tests or example validation commands where appropriate.

---

By following this standard, teams can replicate secure, reproducible builds and deployment patterns across repositories with consistent developer experience and supply-chain hygiene.
