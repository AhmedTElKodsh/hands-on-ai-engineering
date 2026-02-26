# Technology Research & Selection Guide for Layer 1

## Ensuring Curriculum Uses Modern, Production-Ready Tools

**Purpose**: Establish standards for researching and selecting technologies when creating Layer 1 curriculum content
**Layer**: Layer 1 — The Mechanic Level
**Last Updated**: 2026-02-25
**Critical Rule**: ALWAYS research latest technologies before writing setup instructions or choosing dependencies

---

## 🎯 Core Principle

Layer 1 teaches production-ready practices. This means using current best-in-class tools, not legacy approaches that happen to be more common in old tutorials.

**Don't default to what you know — default to what the industry is moving toward.**

---

## 🔍 The Research Process

### Step 1: Identify the Technology Category

Before researching, clearly identify what you're selecting:

- Package managers (Python: pip/uv, Node: npm/pnpm/yarn)
- Testing frameworks (pytest, vitest, jest)
- Development tools (linters, formatters, type checkers)
- API clients (official SDKs vs community libraries)
- Deployment tools (CI/CD, containerization)
- Database tools (ORMs, query builders, migration tools)

### Step 2: Search for Current Best Practices

Use MCP tools to research:

```bash
# Use Exa web search for current best practices
mcp_exa_web_search_exa: "best Python package manager 2026"
mcp_exa_web_search_exa: "modern Python virtual environment tools"
mcp_exa_web_search_exa: "fastest Python dependency resolver"
```

**What to look for**:

- Publication dates (prefer 2025-2026 content)
- Benchmark comparisons (speed, reliability)
- Community adoption signals
- Production usage examples

### Step 3: Verify with Code Examples

```bash
# Search GitHub for real-world usage
mcp_github_search_code: "uv venv language:Python"
mcp_github_search_code: "uv pip install language:Python"
```

**What to check**:

- Are major projects adopting this?
- Recent commits (active maintenance)?
- GitHub stars and forks (community size)?
- Is it production-ready or experimental?

### Step 4: Get Technical Context

```bash
# Get API examples and usage patterns
mcp_exa_get_code_context_exa: "uv Python package manager examples"
```

**What to extract**:

- Installation instructions
- Common usage patterns
- Integration with existing workflows
- Known limitations or gotchas

### Step 5: Compare Alternatives

Document the comparison:

| Aspect                | Modern Tool (uv)         | Traditional Tool (pip) |
| --------------------- | ------------------------ | ---------------------- |
| Speed                 | 10-100x faster           | Baseline               |
| Dependency resolution | Better conflict handling | Can have issues        |
| Installation          | Single binary            | Comes with Python      |
| Maturity              | Newer (2023+)            | Established            |
| Ecosystem             | Growing                  | Universal              |

### Step 6: Make the Decision

Choose the modern tool if:

- ✅ It's production-ready (not experimental)
- ✅ It has active maintenance
- ✅ It provides clear benefits (speed, reliability, DX)
- ✅ It's being adopted by the industry
- ✅ Setup is straightforward

Include the traditional tool if:

- ✅ For educational context
- ✅ As a fallback option
- ✅ To explain the evolution

---

## 📋 Technology Selection Checklist

Before finalizing any setup instructions, verify:

- [ ] **Searched** for "best [tool category] 2026" using `mcp_exa_web_search_exa`
- [ ] **Verified** production-readiness via GitHub search (`mcp_github_search_code`)
- [ ] **Checked** GitHub activity (recent commits, stars, active issues)
- [ ] **Tested** the setup instructions on a fresh environment
- [ ] **Documented** why this tool is better than alternatives
- [ ] **Included** traditional approach for educational context
- [ ] **Explained** trade-offs clearly (speed vs maturity, etc.)
- [ ] **Provided** fallback instructions if modern tool unavailable

---

## 🎓 Writing Technology Choices in Curriculum

### Format: Modern Primary, Traditional Reference

```markdown
### Setup: Modern Approach with `uv`

We'll use `uv` — a modern Python package manager that's 10-100x faster than `pip`
with better dependency resolution. It's built in Rust and designed for the current
Python ecosystem.

**Why `uv`?**

- 10-100x faster dependency resolution and installation
- Better conflict detection and resolution
- Modern design for current Python workflows
- Single binary installation (no Python required)

**Installation**:

# Windows (PowerShell):

powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Mac/Linux:

curl -LsSf https://astral.sh/uv/install.sh | sh

**Usage**:

# Create environment and install dependencies

uv venv
uv pip install -r requirements.txt

---

**Traditional approach (for reference)**:

The older `venv + pip` workflow still works but is significantly slower:

python -m venv venv

# Windows:

venv\Scripts\activate

# Mac/Linux:

source venv/bin/activate
pip install -r requirements.txt

Use this if you're in an environment where `uv` isn't available or if you need
compatibility with legacy tooling.
```

### What to Include

1. **Modern tool first** with clear benefits
2. **Why this tool** (2-3 specific advantages)
3. **Installation instructions** (tested on target platforms)
4. **Usage examples** (common commands)
5. **Traditional alternative** (labeled as reference)
6. **When to use traditional** (specific scenarios)

### What NOT to Do

❌ **Don't**: Default to traditional tools without research

```markdown
### Setup

Create a virtual environment:
python -m venv venv
pip install -r requirements.txt
```

❌ **Don't**: Mention modern tools without explaining benefits

```markdown
You can use uv or pip for this.
```

❌ **Don't**: Skip the traditional approach entirely

```markdown
Everyone should use uv. [No fallback provided]
```

---

## 🔄 When to Research Technology Choices

### Always Research For:

1. **New curriculum days** — Check for latest tools before writing
2. **Package managers** — Python (uv vs pip), Node (pnpm vs npm), etc.
3. **Testing frameworks** — pytest, vitest, jest (check latest versions)
4. **Development tools** — Linters (ruff vs pylint), formatters (black vs ruff format)
5. **API clients** — Official SDKs vs community libraries (check maintenance)
6. **Deployment tools** — CI/CD platforms, containerization approaches
7. **Database tools** — ORMs, query builders, migration frameworks

### Update Existing Content When:

1. **Major version releases** — New tool versions with breaking changes
2. **Industry shifts** — Community moving to new standard (e.g., pip → uv)
3. **Deprecations** — Tool maintainers announce end-of-life
4. **Security issues** — Vulnerabilities in recommended tools
5. **Performance improvements** — New tool offers significant speed gains

---

## 📊 Technology Categories & Current Best Practices (2026)

### Python Ecosystem

| Category        | Modern Choice | Traditional        | Why Modern                        |
| --------------- | ------------- | ------------------ | --------------------------------- |
| Package Manager | `uv`          | `pip`              | 10-100x faster, better resolution |
| Linter          | `ruff`        | `pylint`, `flake8` | 10-100x faster, all-in-one        |
| Formatter       | `ruff format` | `black`            | Faster, integrated with ruff      |
| Type Checker    | `pyright`     | `mypy`             | Faster, better IDE integration    |
| Testing         | `pytest`      | `unittest`         | More features, better DX          |

### JavaScript/TypeScript Ecosystem

| Category        | Modern Choice     | Traditional | Why Modern               |
| --------------- | ----------------- | ----------- | ------------------------ |
| Package Manager | `pnpm`            | `npm`       | Faster, disk-efficient   |
| Runtime         | `bun` (for tools) | `node`      | Much faster for scripts  |
| Bundler         | `vite`            | `webpack`   | Faster, simpler config   |
| Testing         | `vitest`          | `jest`      | Faster, Vite integration |
| Linter          | `biome`           | `eslint`    | Faster, all-in-one       |

### Infrastructure & Deployment

| Category   | Modern Choice        | Traditional    | Why Modern                 |
| ---------- | -------------------- | -------------- | -------------------------- |
| Containers | `docker` + `compose` | `docker` alone | Orchestration built-in     |
| CI/CD      | GitHub Actions       | Jenkins        | Cloud-native, easier setup |
| Hosting    | Vercel, Railway      | Heroku         | Better DX, modern features |

---

## 🎯 Interview Implications

Teaching modern tools has direct interview benefits:

### Signals to Employers

When learners use modern tools, they demonstrate:

- **Staying current** with industry trends
- **Valuing productivity** and developer experience
- **Understanding trade-offs** between tools
- **Ability to evaluate** and adopt new technologies
- **Production mindset** (not just tutorial-following)

### Interview Talking Points

Learners can say:

> "I used `uv` instead of `pip` for this project because it's 10-100x faster and has
> better dependency resolution. In a production environment with frequent deployments,
> that speed difference compounds. I kept `pip` as a fallback for environments where
> `uv` isn't available, but the modern tooling significantly improved my development
> workflow."

This demonstrates:

- Technical decision-making
- Awareness of production concerns
- Pragmatic approach (modern + fallback)
- Quantified benefits (10-100x faster)

---

## 🚫 Common Pitfalls

### Pitfall 1: "Everyone Uses X"

**Don't assume** the most common tool is the best tool.

**Why**: Tutorials lag behind industry adoption. What's "common" in tutorials from 2022 may not be current best practice in 2026.

**Fix**: Research current adoption, not historical popularity.

### Pitfall 2: "I Know How to Use Y"

**Don't default** to tools you're familiar with.

**Why**: Your familiarity doesn't help learners. They need to learn current best practices.

**Fix**: Research first, learn the modern tool, then teach it.

### Pitfall 3: "Z is Too New"

**Don't avoid** new tools just because they're recent.

**Why**: "New" doesn't mean "experimental." Many modern tools are production-ready within months.

**Fix**: Check production usage, GitHub activity, and community adoption. If it's being used in production by major projects, it's ready.

### Pitfall 4: "No Fallback Provided"

**Don't teach** only the modern tool without alternatives.

**Why**: Learners may encounter environments where modern tools aren't available.

**Fix**: Always include traditional approach as reference with clear "when to use" guidance.

---

## 📚 Related Guides

- `WRITING-STYLE-GUIDE.md` — Pattern 8: Modern Tooling First
- `QUALITY-CHECKLIST.md` — Section 7.1: Code Standards (includes modern tooling check)
- `ACTION-FIRST-GUIDE.md` — Pre-Writing Technology Research Checklist
- `GUIDES-INDEX.md` — Full guide reference order

---

## 🔄 Maintenance Schedule

This guide should be reviewed and updated:

- **Quarterly** — Check for new tools and industry shifts
- **Before major curriculum updates** — Verify all technology choices
- **When learners report issues** — Tool may be deprecated or superseded
- **After major conferences** — New tools often announced at PyCon, JSConf, etc.

---

**Layer**: Layer 1 — The Mechanic Level
**Last Updated**: 2026-02-25
**Next Review**: 2026-05-25
