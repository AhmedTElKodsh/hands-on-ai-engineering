# Git Collaboration Workflow — Week 1 Supplement

**Purpose:** Teach team-ready Git skills, not just solo commits
**When:** Week 1, Day 5 (alongside Git basics)
**Why:** Real teams use branches, PRs, and code review — not just `git commit`

---

## 📚 PREREQUISITES

Before this lesson, students should know:
- `git init`, `git add`, `git commit`
- Basic commit history (`git log`)
- What GitHub is

---

## 🎯 LEARNING OBJECTIVES

By the end of this lesson, students will be able to:
1. Create and switch branches
2. Write conventional commit messages
3. Open a Pull Request with proper description
4. Review code using a checklist
5. Merge PRs and handle simple conflicts

---

## 📖 GIT COLLABORATION FUNDAMENTALS

### Why Branches?

**Problem:** You're building a new feature (e.g., "add reranking to RAG"). If you commit directly to `main`:
- Breaking changes affect everyone immediately
- No way to review changes before they go live
- Can't work on multiple features simultaneously

**Solution:** Branches isolate work until it's ready.

```
main:        o———o———o———o (production-ready code)
              \
feature:        o———o———o (work in progress)
```

---

### Branch Naming Conventions

| Type | Format | Example |
|------|--------|---------|
| Feature | `feature/short-description` | `feature/reranking`, `feature/auth` |
| Bug Fix | `bugfix/short-description` | `bugfix/memory-leak`, `bugfix/typo` |
| Hotfix | `hotfix/urgent-fix` | `hotfix/security-patch` |
| Experiment | `experiment/idea` | `experiment/hybrid-search` |
| Documentation | `docs/topic` | `docs/api-reference`, `docs/readme` |

**Rules:**
- Use lowercase and hyphens
- Be specific (`feature/auth` not `feature/stuff`)
- Delete branch after merge

---

### Conventional Commits

**Format:**
```
<type>(<scope>): <subject>

<body> (optional)

<footer> (optional)
```

**Types:**
| Type | When to Use |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `test` | Adding or correcting tests |
| `chore` | Changes to build process, tools, dependencies |

**Examples:**
```
feat(api): add rate limiting to /chat endpoint

Implemented slowapi rate limiter with 100 requests/hour limit.
Added rate limit headers to responses.

Closes #42

---

fix(rag): handle empty retrieval results

Return "I don't know" when no documents match query.
Added test for empty retrieval case.

---

docs(readme): add deployment instructions

Added step-by-step guide for deploying to Render.
Included environment variable setup.
```

**Why Bother?**
- Changelog generation from commit history
- Clear communication with teammates
- Easier code review (know what to expect)

---

## 🔀 BRANCH WORKFLOW (Hands-On Exercise)

### Scenario: Add a New Endpoint to Your FastAPI API

**Current State:**
- You have a FastAPI app with CRUD endpoints for `/documents`
- `main` branch is working

**Goal:**
- Add a new `/documents/{id}/summary` endpoint
- Use a branch, proper commits, and PR

---

### Step 1: Create a Feature Branch

```bash
# Make sure you're on main and up to date
git checkout main
git pull origin main

# Create and switch to new branch
git checkout -b feature/document-summary
```

**Checkpoint:** Verify you're on the new branch
```bash
git branch  # Should show * feature/document-summary
```

---

### Step 2: Make Changes + Commit

**Task:** Add the summary endpoint

```python
# app/routes/documents.py
@router.post("/{document_id}/summary")
async def summarize_document(document_id: int, db: Session = Depends(get_db)):
    """
    Generate a summary of a document using LLM.
    """
    doc = db.get(Document, document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    summary = await llm.summarize(doc.content)
    return {"document_id": document_id, "summary": summary}
```

**Commit:**
```bash
git add app/routes/documents.py
git commit -m "feat(api): add document summary endpoint

Added POST /documents/{id}/summary endpoint.
Uses existing LLM client for summarization.
Returns 404 if document not found."
```

---

### Step 3: Add Tests + Commit

```python
# tests/test_documents.py
def test_summarize_document(client, test_document):
    response = client.post(f"/documents/{test_document.id}/summary")
    assert response.status_code == 200
    assert "summary" in response.json()

def test_summarize_nonexistent_document(client):
    response = client.post("/documents/99999/summary")
    assert response.status_code == 404
```

**Commit:**
```bash
git add tests/test_documents.py
git commit -m "test(api): add tests for document summary endpoint

Added tests for:
- Successful summary generation
- 404 for nonexistent document"
```

---

### Step 4: Push Branch to GitHub

```bash
# Push branch and set upstream
git push -u origin feature/document-summary
```

**Output:**
```
Enumerating objects: 15, done.
...
remote: Create a pull request for 'feature/document-summary' on GitHub by visiting:
remote:      https://github.com/your-username/your-repo/pull/new/feature/document-summary
```

---

## 📝 OPENING A PULL REQUEST

### Step 1: Navigate to GitHub

Go to your repo → Click "Compare & pull request"

### Step 2: Fill Out PR Template

**Title:**
```
feat(api): Add document summary endpoint
```

**Description (use this template):**
```markdown
## What does this PR do?
- Adds POST /documents/{id}/summary endpoint
- Uses existing LLM client for summarization
- Returns 404 for nonexistent documents

## Why is this change needed?
Users requested ability to quickly get document summaries without reading full content.

## How was it tested?
- [x] Unit tests for successful summary
- [x] Unit tests for 404 case
- [x] Manual testing with curl

## Screenshots (if applicable)
```

**Reviewers:** Assign a teammate or AI assistant

**Labels:** `feature`, `api`, `backend`

---

## 🔍 CODE REVIEW CHECKLIST

### For Reviewers

Use this checklist when reviewing PRs:

| Category | Check | Pass? |
|----------|-------|-------|
| **Functionality** | Does the code do what the PR description says? | ⬜ |
| **Testing** | Are there tests for new functionality? | ⬜ |
| **Error Handling** | Are edge cases handled (404, validation, etc.)? | ⬜ |
| **Code Quality** | Is the code readable and well-organized? | ⬜ |
| **Type Hints** | Are function signatures typed? | ⬜ |
| **Documentation** | Are public functions documented? | ⬜ |
| **Security** | Any obvious security issues (SQL injection, etc.)? | ⬜ |
| **Performance** | Any obvious performance issues? | ⬜ |

### Leaving Comments

**Good Comment:**
```
👍 Good use of existing LLM client!

🤔 Consider: What if the LLM call times out? Should we add a retry?

💡 Suggestion: Add type hint for `summary` variable.
```

**Bad Comment:**
```
looks good
```

---

## 🔄 HANDLING FEEDBACK

### Scenario: Reviewer Requests Changes

**Reviewer Comment:**
```
Great start! A few requests:

1. Add timeout handling for LLM calls
2. Add type hints to the response model
3. Update the API documentation

Let me know when you've addressed these!
```

**Your Response:**
```
Thanks for the review! I'll address these today.

- [x] Add timeout handling
- [ ] Add type hints (question: should I create a SummaryResponse model?)
- [x] Update API docs
```

**Make Changes + Commit:**
```bash
# Make changes based on feedback
git add app/routes/documents.py app/models.py
git commit -m "address review feedback: timeout, type hints, docs

- Added 30-second timeout for LLM calls with retry
- Created SummaryResponse model with proper types
- Added OpenAPI documentation with examples"

git push
```

**Note:** GitHub automatically updates the PR with new commits.

---

## ✅ MERGING THE PR

### When All Checks Pass

1. [ ] All tests passing (green checkmark)
2. [ ] Code review approved
3. [ ] No merge conflicts
4. [ ] CI/CD pipeline passed

### Merge Options

| Method | When to Use | Result |
|--------|-------------|--------|
| **Merge Commit** | Feature branches, preserving history | Keeps all commits, adds merge commit |
| **Squash and Merge** | Small features, cleaning up history | Combines all commits into one |
| **Rebase and Merge** | Linear history preference | Replays commits on top of main |

**Recommendation for Students:**
- Use **Squash and Merge** for small PRs (<5 commits)
- Use **Merge Commit** for larger features

---

### After Merge

```bash
# Delete the branch on GitHub (click "Delete branch")

# Clean up locally
git checkout main
git pull origin main
git branch -d feature/document-summary  # Delete local branch
```

---

## 🚨 HANDLING MERGE CONFLICTS

### Scenario: Someone Else Changed the Same File

**GitHub Shows:**
```
⚠️ This branch has conflicts that must be resolved
```

### Step-by-Step Resolution

```bash
# 1. Fetch latest main
git checkout main
git pull origin main

# 2. Switch back to your branch
git checkout feature/document-summary

# 3. Merge main into your branch
git merge main

# Git will show conflicts:
# CONFLICT (content): Merge conflict in app/routes/documents.py
# Automatic merge failed; fix conflicts and then commit the result.

# 4. Open the conflicted file in your editor
# You'll see:
"""
<<<<<<< HEAD
@router.post("/{document_id}/summary")
async def summarize_document(document_id: int, ...):
=======
@router.post("/{document_id}/analyze")
async def analyze_document(document_id: int, ...):
>>>>>>> main
"""

# 5. Resolve the conflict (choose one or combine)
@router.post("/{document_id}/summary")
async def summarize_document(document_id: int, ...):
    # Your code

# 6. Mark as resolved
git add app/routes/documents.py
git commit -m "resolve merge conflict with main"

# 7. Push
git push
```

---

## 📊 PRACTICE EXERCISES

### Exercise 1: Branch + Commit (15 min)

1. Create a branch: `feature/health-endpoint`
2. Add a `/health` endpoint to your FastAPI app
3. Commit with conventional commit message
4. Push to GitHub

**Checkpoint:** Show your branch on GitHub

---

### Exercise 2: Open a PR (10 min)

1. Open a PR from your branch to `main`
2. Fill out the PR template
3. Assign a reviewer (AI assistant or peer)

**Checkpoint:** PR is open and visible on GitHub

---

### Exercise 3: Code Review (20 min)

**Pair up with a classmate or use AI assistant:**

1. Review their PR using the checklist
2. Leave at least 2 comments (1 positive, 1 suggestion)
3. Respond to feedback on your own PR

**Checkpoint:** PR has review comments and responses

---

### Exercise 4: Merge + Clean Up (5 min)

1. Address any review feedback
2. Merge the PR (Squash and Merge)
3. Delete the branch (GitHub + local)

**Checkpoint:** PR is merged, branch deleted

---

## 🎯 WEEK 1 DAY 5 UPDATED AGENDA

| Time | Activity | Deliverable |
|------|----------|-------------|
| **80 min Learn** | Git basics + collaboration workflow | Notes + diagrams |
| **60 min Build** | Set up portfolio repo with branches | `main` + pre-commit |
| **60 min Build** | Practice: feature branch + PR | Open PR on GitHub |
| **40 min Ship** | Code review exercise + merge | Merged PR, clean history |

---

## 📝 CHECKPOINT QUESTIONS

Answer before proceeding to Week 2:

| # | Question | What a Good Answer Includes |
|---|----------|----------------------------|
| **1** | Why use branches instead of committing directly to main? | - Isolate work in progress<br>- Enable code review<br>- Prevent breaking changes to production<br>- Allow parallel feature development |
| **2** | What makes a good commit message? | - Conventional format (type: subject)<br>- Specific description<br>- Explains why, not just what<br>- References issues if applicable |
| **3** | What goes in a good PR description? | - What the PR does<br>- Why the change is needed<br>- How it was tested<br>- Screenshots if UI changes |
| **4** | What do you check when reviewing code? | - Functionality (does it work?)<br>- Testing (are there tests?)<br>- Code quality (readable, typed)<br>- Security/performance concerns |
| **5** | How do you resolve a merge conflict? | - Pull latest main<br>- Merge main into branch<br>- Edit conflicted files<br>- Stage + commit resolution<br>- Push updated branch |

---

## 🔗 RESOURCES

- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Conventional Commits](https://www.conventionalcommits.org)
- [Pull Request Templates](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository)
- [Resolving Merge Conflicts](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts/resolving-a-merge-conflict-using-the-command-line)

---

## 💡 WHY THIS MATTERS FOR AI ENGINEERS

**From Hiring Managers:**

> "I don't expect perfect Git skills from juniors. But I do expect them to know branches and PRs. If you commit directly to main in an interview, that's a red flag."
> — Engineering Manager, AI Startup

> "Code review is how we maintain quality. If you can't participate in review, you can't work on our team."
> — Senior AI Engineer, Big Tech

**Bottom Line:** Git collaboration is table stakes. Learn it early.

---

**Remember:** Git is a tool for teamwork. The goal is not perfect commits — it's clear communication with your team.

**Practice makes permanent. Use branches from Day 1.** 🚀

**Last Updated:** March 8, 2026
