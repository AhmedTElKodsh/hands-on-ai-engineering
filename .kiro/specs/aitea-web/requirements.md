# Requirements Document: AITEA Web

## Introduction

AITEA Web is an AI-powered web application for project time estimation. It extends aitea-core with multi-LLM support, external integrations (GitHub, time tracking tools), and a modern web interface built with FastAPI (backend) and NiceGUI (frontend).

## Dependencies

- **aitea-core**: Shared models, services, and utilities

## Glossary

- **LLM**: Large Language Model for AI-powered feature extraction
- **Multi-LLM Engine**: System supporting multiple LLM providers with fallback
- **Provider**: An LLM API service (Cohere, HuggingFace, Gemini, Grok, Mistral, Ollama)
- **Fallback Chain**: Ordered list of providers to try if primary fails
- **Integration**: Connection to external service (GitHub, Clockify, etc.)

## Requirements

### Requirement 1: FastAPI Backend

**User Story:** As a developer, I want a REST API backend, so that the web UI and external tools can interact with AITEA.

#### Acceptance Criteria

1. WHEN the server starts, THE System SHALL expose OpenAPI documentation at /docs
2. WHEN a request is made, THE System SHALL validate input using Pydantic models
3. WHEN an error occurs, THE System SHALL return appropriate HTTP status codes with error details
4. WHEN handling requests, THE System SHALL support async operations for external API calls

### Requirement 2: NiceGUI Frontend

**User Story:** As a Project Manager, I want a web-based interface, so that I can interact with AITEA visually.

#### Acceptance Criteria

1. WHEN accessing the app, THE System SHALL display a dashboard with summary statistics
2. WHEN viewing features, THE System SHALL display an interactive table with sorting and filtering
3. WHEN importing data, THE System SHALL provide file upload with progress indication
4. WHEN generating estimates, THE System SHALL display results in formatted tables with export options
5. WHEN configuring settings, THE System SHALL provide forms for all configuration options

### Requirement 3: Multi-LLM Engine

**User Story:** As a System Administrator, I want to configure multiple LLM providers, so that I have flexibility and redundancy.

#### Acceptance Criteria

1. WHEN configuring providers, THE System SHALL support Cohere, HuggingFace, Gemini, Grok, Mistral, and Ollama
2. WHEN a provider fails, THE System SHALL automatically try the next provider in the fallback chain
3. WHEN all providers fail, THE System SHALL fall back to non-AI estimation methods
4. WHEN testing a provider, THE System SHALL validate API key and connectivity
5. WHEN making requests, THE System SHALL implement rate limiting and retry with exponential backoff

### Requirement 4: AI-Powered BRD Analysis

**User Story:** As a Project Manager, I want AI to analyze BRDs intelligently, so that feature extraction is more accurate.

#### Acceptance Criteria

1. WHEN analyzing a BRD, THE System SHALL use LLM to extract features with context understanding
2. WHEN features are ambiguous, THE System SHALL generate clarifying questions
3. WHEN estimating, THE System SHALL suggest similar features from the library
4. WHEN analysis completes, THE System SHALL provide confidence scores and reasoning

### Requirement 5: GitHub Integration

**User Story:** As a Project Manager, I want to connect to GitHub repositories, so that the system can analyze project structure.

#### Acceptance Criteria

1. WHEN connecting GitHub, THE System SHALL authenticate via OAuth or Personal Access Token
2. WHEN selecting a repository, THE System SHALL fetch structure and file contents
3. WHEN analyzing code, THE System SHALL use LLM to identify features and patterns
4. WHEN features are extracted, THE System SHALL map them to the feature library with confidence scores

### Requirement 6: Time Tracking Integrations

**User Story:** As a Project Manager, I want to import time data from external tools automatically.

#### Acceptance Criteria

1. WHEN connecting Clockify, THE System SHALL authenticate via API key and fetch time entries
2. WHEN connecting ClickUp, THE System SHALL authenticate via API token and fetch task time
3. WHEN connecting Trello, THE System SHALL authenticate and fetch time tracking data
4. WHEN importing, THE System SHALL map external tasks to features using fuzzy matching
5. WHEN syncing, THE System SHALL track last sync timestamp and fetch only new entries

### Requirement 7: Data Persistence

**User Story:** As a user, I want data to persist reliably.

#### Acceptance Criteria

1. WHEN storing data, THE System SHALL use SQLite for relational data (users, audit)
2. WHEN storing estimation data, THE System SHALL use JSON for compatibility with CLI
3. WHEN multiple users access data, THE System SHALL implement optimistic locking
4. WHEN data changes, THE System SHALL create audit trail entries

### Requirement 8: Analytics Dashboard

**User Story:** As a Project Manager, I want analytics and trends visualization.

#### Acceptance Criteria

1. WHEN viewing analytics, THE System SHALL display estimation accuracy trends
2. WHEN analyzing velocity, THE System SHALL show hours completed per period
3. WHEN reviewing complexity, THE System SHALL display distribution by feature type
4. WHEN exporting, THE System SHALL generate PDF reports with charts

### Requirement 9: Notifications

**User Story:** As a Team Lead, I want notifications for important events.

#### Acceptance Criteria

1. WHEN configured, THE System SHALL send Slack notifications for key events
2. WHEN configured, THE System SHALL send email digest reports
3. WHEN estimates deviate >30% from actuals, THE System SHALL generate alerts

### Requirement 10: User Management

**User Story:** As an Administrator, I want to manage users and access.

#### Acceptance Criteria

1. WHEN managing users, THE System SHALL support Admin, Manager, Viewer roles
2. WHEN authenticating, THE System SHALL support local auth and OAuth (Google, Microsoft)
3. WHEN accessing data, THE System SHALL enforce role-based permissions
4. WHEN auditing, THE System SHALL log authentication events and permission changes
