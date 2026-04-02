# Security Review

## Overview

This review covers potential security vulnerabilities, data handling practices, and API interaction concerns.

---

## 1. Missing User-Agent Header (MEDIUM Severity)

**Location:** `reddit/base.py`

Reddit API documentation strongly recommends that clients send a User-Agent header to identify themselves. Without it:

- Reddit may block or rate-limit requests
- Difficult to troubleshoot issues
- May violate Reddit API terms

**Current Code:**
```python
async def __aenter__(self) -> "RedditClient":
    self._client = httpx.AsyncClient(
        base_url=self.BASE_URL,
        timeout=httpx.Timeout(self.TIMEOUT, connect=5.0)
    )
    return self
```

**Recommendation:**
```python
async def __aenter__(self) -> "RedditClient":
    self._client = httpx.AsyncClient(
        base_url=self.BASE_URL,
        timeout=httpx.Timeout(self.TIMEOUT, connect=5.0),
        headers={"User-Agent": "better-reddit-cli/0.4.4"}
    )
```

---

## 2. URL Injection via Subreddit Names (LOW Severity)

**Location:** Multiple files - API path construction

```python
# posts.py:33
path = f"/r/{subreddit}/{sort}.json"

# subreddits.py:20
data = await self._client.get(f"/r/{name}/about.json")
```

**Risk:** User could provide malicious subreddit name containing:
- Path traversal: `../../etc/passwd`
- Additional path segments: `python/../../../etc/passwd`
- Unicode confusion: Homoglyph attacks

**Reddit-Specific Context:** Reddit's API has its own validation, so direct injection is unlikely. However, no sanitization is performed.

**Recommendation:** Validate subreddit names with regex:
```python
import re
SUBREDDIT_PATTERN = re.compile(r'^[a-zA-Z0-9_]{3,21}$')
```

---

## 3. No Input Sanitization for Search Queries (LOW Severity)

**Location:** `posts.py:121-156`

```python
async def search_posts(self, query: str, ...):
    params: dict[str, int | str] = {
        "q": query,  # Direct pass-through
    }
```

Reddit's search API likely handles XSS/special characters, but passing user input directly without sanitization is a concern.

**Current:** No sanitization of `query` parameter.

---

## 4. Command Injection in Print Output (LOW Severity)

**Location:** Multiple command files

```python
print(f"[{post.score}] {post.title}")
```

**Risk:** If Reddit returns malicious content in `title` field (e.g., terminal escape codes), output could:
- Clear the terminal
- Change terminal colors
- Execute bell characters

**Current mitigation:** Some files use encode/decode:
```python
body.encode(sys.stdout.encoding, errors="replace").decode(sys.stdout.encoding)
```

**Issue:** Not applied consistently to all user-visible output.

---

## 5. No HTTPS Enforcement (N/A for this project)

The code uses HTTPS by default:
```python
BASE_URL = "https://www.reddit.com"
```

No issues here.

---

## 6. Secrets/API Keys (NOT APPLICABLE)

README states: "No API key needed, no authentication, no hassle."

The project intentionally does not use authentication, so no secrets handling issues.

---

## 7. Dependency Vulnerabilities (REQUIRES REVIEW)

Dependencies:
- typer
- httpx
- pydantic

**Recommendation:** Run safety check:
```bash
pip audit
# or
safety check
```

---

## 8. File Operations (NOT APPLICABLE)

The codebase does not read or write files (except __pycache__). No file operation security concerns.

---

## 9. Environment Variables (NOT USED)

No environment variables are used for configuration. The timeout is hardcoded.

---

## 10. Logging of Sensitive Information (NOT A CONCERN)

No logging of sensitive data since:
- No authentication
- No user credentials
- No personal data beyond public Reddit content

---

## 11. Race Conditions (NOT A CONCERN)

Single-threaded async CLI tool makes one request at a time. No concurrent state mutation concerns.

---

## 12. Error Message Information Disclosure (LOW Severity)

**Location:** `commands/subreddit.py:47-48`

```python
except Exception:
    print("Moderators list is not publicly available (requires authentication)")
```

Error messages reveal that authentication exists even though the app doesn't support it.

---

## Security Summary

| Issue | Severity | Exploitable | Impact |
|-------|----------|-------------|--------|
| Missing User-Agent | MEDIUM | Yes | Rate limiting, blocks |
| URL injection (subreddit names) | LOW | Unlikely | Data exfiltration (theoretical) |
| Search query injection | LOW | Unlikely | XSS (theoretical) |
| Terminal escape codes in output | LOW | Unlikely | Annoyance |
| Error message disclosure | LOW | Yes | Information gathering |

---

## Recommendations

1. **HIGH PRIORITY:** Add User-Agent header
2. **MEDIUM PRIORITY:** Sanitize/validate all user input (subreddit names, post IDs)
3. **MEDIUM PRIORITY:** Sanitize output to prevent terminal escape code injection
4. **LOW PRIORITY:** Run dependency vulnerability scan

---

## Overall Security Posture

**Assessment:** MODERATE

The project is a read-only public API client with no authentication requirements. The main risks are:
1. API access disruption (missing User-Agent)
2. Information disclosure in error messages
3. Potential terminal escape code issues

No critical security vulnerabilities identified.

---

*Report generated for project: better-reddit-cli v0.4.4*
