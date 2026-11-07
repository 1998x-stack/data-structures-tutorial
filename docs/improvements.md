# Portfolio Improvement History

### 2026-11-07 03:14 UTC — ChatGPT Portfolio Iteration
- Run ID: portfolio-20261107T0314Z-b72e
- Repo / Base SHA: 1998x-stack/data-structures-tutorial / d00779f9e6ca8206c7be459d3d977004f632ee2a
- Historical context: docs/improvements.md was absent on default branch (GitHub 404); first initialization. No prior PR found in repository search.
- Product problem & expected user value: README instructs opening index.html directly, but the page fetches courses.json; browsers may reject file:// fetch and users lose chapter navigation. Static fallback links preserve access to all 28 chapters without a server or JavaScript.
- Engineering diagnosis & evidence: index.html fetch('courses.json') only populated links after fetch succeeded; catch showed an error without links. Candidate alternatives: improve per-card accessible names (P2; 11), loading status (P2; 10), offline navigation (P1; 17). Scores: benefit + correctness + evidence + testability - cost - risk.
- Options & decision: Chose offline navigation, the highest-scoring low-risk improvement; no change to chapter content, JSON schema or existing card rendering.
- Changes: index.html adds 28 static links from courses.json and hides fallback after successful JSON loading; error text points to fallback. tests/test_offline_index.py adds manifest/link integrity and no-JS fallback checks.
- Validation: A (executed JS structural assertions against actual branch files): six checks passed for link order, uniqueness, visible fallback, success hide, error message and test presence. D: python -m unittest discover -s tests -v authored but not run; runtime cannot fetch branch to local test environment (DNS resolution failed). D: real browser file:// and served-page E2E not run. No claim of CI success.
- Security & regression review: no dependencies, scripts, permissions, deployment, workflows or sensitive files changed; fallback link paths come from existing manifest; original JSON-driven cards remain.
- Risk & rollback: Static link labels can drift from manifest; regression test checks filenames, not labels. Revert this feature branch commit(s) to restore original behavior; Draft PR must not merge without Python/browser verification.
- Follow-up: Run Python tests and browser smoke for file:// and HTTP, then verify GitHub checks/branch protection before merge.
- Commit: pending (history creation commit)
- PR: pending
