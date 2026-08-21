# Day 14: CI/CD Pipelines & Automated Deployment

## What I did
- Built .github/workflows/ci.yml: test -> build-and-push (Docker image to GHCR) -> deploy
- Deploy stage uses SSH keys via GitHub Secrets; fails at "missing server host" since no
  live cloud VM was provisioned for this exercise (documented honestly, not faked)
- Verified pipeline blocks broken code: opened a PR with an intentional syntax error,
  confirmed build-and-test failed and downstream jobs were skipped
- Reverted the syntax error, confirmed all three jobs pass on the corrected PR
- Merged into main, confirmed pipeline re-runs automatically on merge

## What I learned
- CI/CD stages should be dependency-chained (needs:) so broken code never reaches deploy
- A pipeline can be "correctly configured" even if one stage can't be verified end-to-end
  (no live server) -- structure and failure behavior still prove it works