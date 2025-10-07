# Repository Guidelines

## Project Structure & Module Organization
- `TechBlogNotifications/TechBlogNotifications` contains the SwiftUI app; `Domain/`, `Model/`, and `Repository/` split business rules, data shapes, and Firestore access, while `View/` and `Utils/` hold UI screens and shared helpers.
- `Assets.xcassets`, `Preview Content/`, and `Config/Config.swift` store design assets, sample data, and runtime configuration alongside `GoogleService-Info.plist`.
- `tech-blog-scraper-functions/` is the Python Firebase Functions project; `scrapers/` implements per-blog crawlers, `firestore_uploader.py` manages writes, and `main.py` exposes HTTP and scheduler entry points.
- `scripts/` captures research notes such as scraping strategies; other top-level folders are unused unless populated in feature branches.

## Build, Test, and Development Commands
- Open the iOS app with `open TechBlogNotifications/TechBlogNotifications.xcodeproj`, or build headless via `xcodebuild -scheme TechBlogNotifications -destination 'platform=iOS Simulator,name=iPhone 15' build`.
- Run the simulator target from Xcode using the `TechBlogNotifications` scheme; ensure the Firebase bundle ID matches the active `GoogleService-Info.plist`.
- For scraper work: `cd tech-blog-scraper-functions && python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements-dev.txt` to prepare dependencies.
- Execute quick smoke checks with `python test_scrapers.py`; use `python test_integration.py` for end-to-end scraping and `python test_firestore_upload.py` before deploying functions.

## Coding Style & Naming Conventions
- Swift uses 4-space indentation, `camelCase` identifiers, and `UpperCamelCase` types; co-locate view-specific modifiers and favor extensions for reusable view builders.
- Respect the repository layering: keep Firestore logic inside `Repository/` and surface UI-ready models via `Domain/` types; reuse constants in `Utils/Constants.swift`.
- Python modules follow PEP 8 with type hints; scraper classes expose `scrape()` and `get_blog_name()` and must return dicts matching `firestore_uploader` expectations.

## Testing Guidelines
- Prefer lightweight SwiftUI previews for UI smoke tests and document manual scenarios when adding asynchronous flows or new repositories.
- Add targeted Python unit tests per scraper under `tech-blog-scraper-functions/tests`; name helpers `test_<context>`. Keep sample responses deterministic and avoid network calls in CI.
- Validate Firestore writes locally with the provided uploader test before touching production collections.

## Commit & Pull Request Guidelines
- Match the existing history style: `<type>: <short summary>` such as `feat: 네트워크 모니터링 기능 추가`. Use `feat`, `fix`, `chore`, or `refactor` as needed.
- Reference related issues in the description, note any migrations (e.g., schema or Firestore path changes), and attach screenshots for UI-facing work.
- Before requesting review, confirm Xcode builds cleanly, Python tests pass, and new configuration files are documented or gitignored as appropriate.

## Configuration & Security Notes
- Keep secrets out of commits; rotate or encrypt `GoogleService-Info.plist` values if distributing builds externally.
- Update the Firebase project settings and scheduler cron definitions alongside code changes, capturing the steps in `AGENTS.md` or linked runbooks.
