# Implementation Plan: AITEA Web

## Prerequisites

- aitea-core package must be installed

## 1. Project Setup

- [ ] 1.1 Initialize Web package structure
  - Create pyproject.toml with package metadata (name: aitea-web)
  - Add dependency on aitea-core
  - Create src/aitea_web/ directory structure
  - Create api/, ui/, llm/, integrations/, services/ subdirectories
  - Add __init__.py files to all packages
  - Create requirements.txt (fastapi, uvicorn, nicegui, httpx, sqlalchemy, cohere, google-generativeai, mistralai)
  - _Requirements: 1.1_

- [ ] 1.2 Set up database
  - Create src/aitea_web/services/database.py
  - Configure SQLAlchemy with SQLite
  - Create User, AuditLog models
  - Set up Alembic for migrations
  - _Requirements: 7.1-7.4_

## 2. Multi-LLM Engine

- [ ] 2.1 Create LLM provider interface
  - Create src/aitea_web/llm/__init__.py
  - Create src/aitea_web/llm/base.py with ILLMProvider, LLMConfig, LLMResponse
  - Define abstract methods: complete, test_connection
  - _Requirements: 3.1_

- [ ] 2.2 Implement Cohere provider
  - Create src/aitea_web/llm/providers/cohere.py
  - Implement async complete using cohere SDK
  - Implement test_connection
  - _Requirements: 3.1_

- [ ] 2.3 Implement HuggingFace provider
  - Create src/aitea_web/llm/providers/huggingface.py
  - Implement async complete using huggingface_hub
  - _Requirements: 3.1_

- [ ] 2.4 Implement Gemini provider
  - Create src/aitea_web/llm/providers/gemini.py
  - Implement async complete using google-generativeai
  - _Requirements: 3.1_

- [ ] 2.5 Implement Grok provider
  - Create src/aitea_web/llm/providers/grok.py
  - Implement async complete using httpx
  - _Requirements: 3.1_

- [ ] 2.6 Implement Mistral provider
  - Create src/aitea_web/llm/providers/mistral.py
  - Implement async complete using mistralai SDK
  - _Requirements: 3.1_

- [ ] 2.7 Implement Ollama provider
  - Create src/aitea_web/llm/providers/ollama.py
  - Implement async complete using httpx to local API
  - _Requirements: 3.1_

- [ ] 2.8 Implement LLM Engine with fallback
  - Create src/aitea_web/llm/engine.py
  - Implement fallback chain logic (try providers in priority order)
  - Implement rate limiting with token bucket
  - Implement retry with exponential backoff
  - _Requirements: 3.2-3.5_

- [ ]* 2.9 Write tests for LLM fallback
  - Test fallback chain execution
  - Test rate limiting
  - **Property 1, 2**

- [ ] 2.10 Create feature extraction prompts
  - Create src/aitea_web/llm/prompts/feature_extraction.py
  - Define system prompt for BRD analysis
  - Define prompt template for feature extraction
  - Parse LLM response to ExtractedFeature list
  - _Requirements: 4.1-4.4_

- [ ] 2.11 Checkpoint - Ensure LLM tests pass

## 3. Integration Services

- [ ] 3.1 Implement GitHub Service
  - Create src/aitea_web/integrations/github.py
  - Implement authenticate (OAuth/PAT)
  - Implement list_repos, get_file_contents
  - Implement analyze_repo using LLM engine
  - _Requirements: 5.1-5.4_

- [ ]* 3.2 Write tests for GitHub integration
  - Mock GitHub API responses
  - **Property 3**

- [ ] 3.3 Implement Clockify Service
  - Create src/aitea_web/integrations/clockify.py
  - Implement authenticate, fetch_entries
  - Map entries to TimeEntry model
  - Track last sync timestamp
  - _Requirements: 6.1, 6.5_

- [ ] 3.4 Implement ClickUp Service
  - Create src/aitea_web/integrations/clickup.py
  - Implement authenticate, fetch_entries
  - _Requirements: 6.2, 6.5_

- [ ] 3.5 Implement Trello Service
  - Create src/aitea_web/integrations/trello.py
  - Implement authenticate, fetch_entries
  - _Requirements: 6.3, 6.5_

- [ ] 3.6 Implement feature mapping
  - Create src/aitea_web/integrations/mapper.py
  - Implement fuzzy matching of task names to features
  - Return mapped and unmapped entries
  - _Requirements: 6.4_

- [ ]* 3.7 Write tests for time tracking integrations
  - **Property 4, 5**

- [ ] 3.8 Checkpoint - Ensure integration tests pass

## 4. FastAPI Backend

- [ ] 4.1 Create FastAPI application
  - Create src/aitea_web/api/app.py
  - Configure CORS, error handling
  - Set up OpenAPI documentation
  - _Requirements: 1.1-1.4_

- [ ] 4.2 Implement feature routes
  - Create src/aitea_web/api/routes/features.py
  - GET /api/features - list features
  - POST /api/features - create feature
  - PUT /api/features/{id} - update feature
  - DELETE /api/features/{id} - delete feature
  - _Requirements: 2.2_

- [ ] 4.3 Implement estimation routes
  - Create src/aitea_web/api/routes/estimation.py
  - POST /api/estimate/brd - estimate from BRD
  - POST /api/estimate/features - estimate selected features
  - GET /api/estimate/table - get estimation table
  - POST /api/estimate/export - export estimates
  - _Requirements: 2.4_

- [ ] 4.4 Implement LLM routes
  - Create src/aitea_web/api/routes/llm.py
  - GET /api/llm/providers - list configured providers
  - POST /api/llm/providers - configure provider
  - POST /api/llm/test/{provider} - test provider
  - POST /api/llm/analyze - analyze text with LLM
  - _Requirements: 3.4_

- [ ] 4.5 Implement integration routes
  - Create src/aitea_web/api/routes/integrations.py
  - POST /api/integrations/github/connect
  - POST /api/integrations/clockify/connect
  - POST /api/integrations/clickup/connect
  - POST /api/integrations/trello/connect
  - POST /api/integrations/sync
  - GET /api/integrations/status
  - _Requirements: 5.1, 6.1-6.3_

- [ ] 4.6 Implement auth middleware
  - Create src/aitea_web/api/middleware/auth.py
  - JWT token validation
  - Role-based access control
  - _Requirements: 10.1-10.3_

- [ ] 4.7 Implement audit logging
  - Create src/aitea_web/services/audit.py
  - Log all data modifications
  - Include user, timestamp, changes
  - _Requirements: 7.4_

- [ ]* 4.8 Write tests for API routes
  - **Property 6, 7**

- [ ] 4.9 Checkpoint - Ensure API tests pass

## 5. NiceGUI Frontend

- [ ] 5.1 Create NiceGUI application
  - Create src/aitea_web/ui/app.py
  - Configure page routing
  - Create header/navigation component
  - Mount FastAPI app
  - _Requirements: 2.1_

- [ ] 5.2 Implement Dashboard page
  - Create src/aitea_web/ui/pages/dashboard.py
  - Display summary cards (features, entries, quality)
  - Display recent activity
  - _Requirements: 2.1_

- [ ] 5.3 Implement Feature Library page
  - Create src/aitea_web/ui/pages/features.py
  - Interactive table with sorting/filtering
  - Add feature dialog
  - Edit/delete functionality
  - Search input
  - _Requirements: 2.2_

- [ ] 5.4 Implement Estimation page
  - Create src/aitea_web/ui/pages/estimation.py
  - BRD text input tab
  - Feature selection tab
  - Results tables
  - Export buttons (JSON, CSV)
  - _Requirements: 2.4_

- [ ] 5.5 Implement Integrations page
  - Create src/aitea_web/ui/pages/integrations.py
  - GitHub connection card
  - Clockify/ClickUp/Trello connection cards
  - LLM provider configuration
  - Sync status display
  - _Requirements: 2.4_

- [ ] 5.6 Implement Settings page
  - Create src/aitea_web/ui/pages/settings.py
  - Estimation style selector
  - Working hours selector
  - Experience multipliers inputs
  - Buffer percentage slider
  - Save button
  - _Requirements: 2.5_

- [ ] 5.7 Create reusable components
  - Create src/aitea_web/ui/components/feature_table.py
  - Create src/aitea_web/ui/components/estimate_table.py
  - Create src/aitea_web/ui/components/charts.py
  - _Requirements: 2.2, 2.4_

## 6. Analytics & Notifications

- [ ] 6.1 Implement Analytics Service
  - Create src/aitea_web/services/analytics.py
  - Implement accuracy trends calculation
  - Implement velocity calculation
  - Implement complexity distribution
  - _Requirements: 8.1-8.3_

- [ ] 6.2 Implement Analytics page
  - Create src/aitea_web/ui/pages/analytics.py
  - Accuracy trend chart
  - Velocity chart
  - Complexity distribution chart
  - PDF export
  - _Requirements: 8.1-8.4_

- [ ] 6.3 Implement Notification Service
  - Create src/aitea_web/services/notifications.py
  - Implement Slack webhook integration
  - Implement email sending (SMTP)
  - Implement discrepancy alerts
  - _Requirements: 9.1-9.3_

## 7. User Management

- [ ] 7.1 Implement User Service
  - Create src/aitea_web/services/users.py
  - User CRUD operations
  - Role management (Admin, Manager, Viewer)
  - Password hashing
  - _Requirements: 10.1_

- [ ] 7.2 Implement Auth routes
  - Create src/aitea_web/api/routes/auth.py
  - POST /api/auth/login
  - POST /api/auth/register
  - POST /api/auth/refresh
  - GET /api/auth/me
  - _Requirements: 10.2_

- [ ] 7.3 Implement OAuth integration
  - Add Google OAuth support
  - Add Microsoft OAuth support
  - _Requirements: 10.2_

- [ ] 7.4 Implement Login page
  - Create src/aitea_web/ui/pages/login.py
  - Login form
  - OAuth buttons
  - _Requirements: 10.2_

## 8. Integration & Finalization

- [ ] 8.1 Create main entry point
  - Create src/aitea_web/main.py
  - Initialize all services
  - Mount FastAPI and NiceGUI
  - Configure startup/shutdown events
  - _Requirements: All_

- [ ] 8.2 Create Docker configuration
  - Create Dockerfile
  - Create docker-compose.yml
  - _Requirements: All_

- [ ] 8.3 Checkpoint - Ensure all tests pass
  - Run pytest
  - Test end-to-end workflows

- [ ]* 8.4 Write integration tests
  - Test BRD analysis workflow
  - Test GitHub integration workflow
  - Test time tracking sync workflow
  - Test multi-user scenarios
