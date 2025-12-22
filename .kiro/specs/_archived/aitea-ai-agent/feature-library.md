# AITEA AI Agent Feature Library Reference

## Overview

This document defines the standard feature library for AITEA AI Agent estimation, organized in a three-tier hierarchy:
- **Team (Category)**: Top-level grouping (Frontend, Backend)
- **Process**: Middle-level functional area (e.g., User Management, Content Management)
- **Feature**: Atomic development task with time estimate

## Hierarchical Structure

```
Team → Process → Feature (with seed time)
```

## Frontend Features

### Process: User Management
| Feature | Seed Time (hours) | Synonyms | Notes |
|---------|-------------------|----------|-------|
| RBAC | 12 | role-based-access, permissions-ui, access-control-ui | Role-based access control UI components |

### Process: Content Management
| Feature | Seed Time (hours) | Synonyms | Notes |
|---------|-------------------|----------|-------|
| ui-Page | 6 | page-layout, landing-page, static-page, page-component | Single page/view implementation |
| tables | 5 | data-tables, grid, data-grid, table-component | Data table with sorting/pagination |
| forms | 3 | form-components, input-forms, form-validation | Form components with validation |
| filtering | 4 | search-filter, data-filter, filter-component | Client-side filtering/search |

### Process: Communication
| Feature | Seed Time (hours) | Synonyms | Notes |
|---------|-------------------|----------|-------|
| messaging | 12 | chat-ui, inbox, message-center | In-app messaging interface |
| notifications | 12 | notification-center, alerts-ui, toast-notifications | Notification display components |

### Process: Data Operations
| Feature | Seed Time (hours) | Synonyms | Notes |
|---------|-------------------|----------|-------|
| CRUD | 4 | crud-ui, data-management-ui, admin-crud | Create/Read/Update/Delete interface |
| analytics | 8 | dashboard-charts, statistics-ui, charts, reporting-ui | Analytics/charts display |

### Process: Media Handling
| Feature | Seed Time (hours) | Synonyms | Notes |
|---------|-------------------|----------|-------|
| file-upload | 6 | upload-component, file-picker, drag-drop-upload | File upload with preview |
| streaming | 12 | video-player, media-player, stream-viewer | Media streaming playback |

### Process: Integration
| Feature | Seed Time (hours) | Synonyms | Notes |
|---------|-------------------|----------|-------|
| 3rd-party-integration | 8 | external-api-ui, oauth-ui, social-login | Third-party service integration UI |

### Process: Visual Enhancement
| Feature | Seed Time (hours) | Synonyms | Notes |
|---------|-------------------|----------|-------|
| animations | 6 | transitions, motion, ui-animations | UI animations and transitions |

---

## Backend Features

### Process: User Management
| Feature | Seed Time (hours) | Synonyms | Notes |
|---------|-------------------|----------|-------|
| RBAC | 8 | role-based-access, permissions, access-control, authorization | Role-based access control backend |

### Process: Data Operations
| Feature | Seed Time (hours) | Synonyms | Notes |
|---------|-------------------|----------|-------|
| CRUD | 4 | crud-api, rest-crud, data-operations | Create/Read/Update/Delete API |
| filtering | 4 | query-filter, search-api, data-filter | Server-side filtering/search |
| caching | 1 | cache-layer, redis-cache, memory-cache | Caching implementation |
| statistics-and-charts | 8 | analytics-api, reporting-api, metrics | Analytics data processing |

### Process: Communication
| Feature | Seed Time (hours) | Synonyms | Notes |
|---------|-------------------|----------|-------|
| emails | 2 | email-service, smtp, email-notifications | Email sending service |
| push-notifications | 12 | fcm, apns, mobile-notifications | Push notification service |

### Process: Media Handling
| Feature | Seed Time (hours) | Synonyms | Notes |
|---------|-------------------|----------|-------|
| file-upload | 4 | file-storage, s3-upload, upload-api | File upload/storage backend |
| streaming | 12 | media-streaming, video-stream, hls | Media streaming backend |
| video-handling | 20 | video-processing, transcoding, video-api | Video processing/transcoding |

### Process: Integration
| Feature | Seed Time (hours) | Synonyms | Notes |
|---------|-------------------|----------|-------|
| 3rd-party-integration | 8 | external-api, webhook, api-integration | Third-party API integration |
| payment | 8 | stripe, payment-gateway, billing | Payment processing |

### Process: Real-time
| Feature | Seed Time (hours) | Synonyms | Notes |
|---------|-------------------|----------|-------|
| websocket | 12 | socket-io, real-time, live-updates | WebSocket server implementation |

### Process: Background Processing
| Feature | Seed Time (hours) | Synonyms | Notes |
|---------|-------------------|----------|-------|
| background-tasks | 12 | job-queue, celery, async-tasks, scheduled-jobs | Background job processing |

---

## Process Definitions

| Process | Description | Typical Features |
|---------|-------------|------------------|
| **User Management** | Authentication, authorization, user profiles, access control | RBAC, auth-ui, user-profile |
| **Content Management** | Pages, forms, tables, data display and manipulation | ui-Page, tables, forms, filtering |
| **Communication** | Messaging, notifications, emails, alerts | messaging, notifications, emails, push-notifications |
| **Data Operations** | CRUD operations, filtering, caching, analytics | CRUD, filtering, caching, analytics |
| **Media Handling** | File uploads, streaming, video/audio processing | file-upload, streaming, video-handling |
| **Integration** | Third-party APIs, payment gateways, webhooks | 3rd-party-integration, payment |
| **Real-time** | WebSocket, live updates, streaming connections | websocket, streaming |
| **Background Processing** | Async tasks, scheduled jobs, queues | background-tasks |
| **Visual Enhancement** | Animations, transitions, UI polish | animations |

---

## AI-Powered Feature Extraction

When the AI Agent analyzes a BRD or repository, it maps extracted features to this hierarchy:

```python
@dataclass
class ExtractedFeature:
    name: str
    team: Team
    process: Process
    matched_library_feature: Optional[Feature] = None
    is_new_feature: bool = False
    confidence: float = 0.0
    source_text: str = ""
    suggested_seed_hours: Optional[float] = None
```

### LLM Prompt for Feature Extraction

```
Given the following requirement text, extract development features and categorize them:

Teams: Frontend, Backend
Processes: User Management, Content Management, Communication, Data Operations, 
           Media Handling, Integration, Real-time, Background Processing, Visual Enhancement

For each feature, provide:
- feature_name: The atomic task name
- team: frontend or backend
- process: The functional area from the list above
- estimated_hours: Based on complexity (use standard seed times as reference)
- confidence: 0.0-1.0 based on clarity of requirement

Standard seed times for reference:
- Simple features (CRUD, forms, filtering, caching): 1-4 hours
- Medium features (ui-Page, tables, file-upload, emails): 4-8 hours
- Complex features (RBAC, messaging, websocket, payment): 8-12 hours
- Very complex features (video-handling, streaming): 12-20 hours
```

---

## Estimation Rules

### Repeatable Features
Some features are implemented multiple times in a project. The time estimate applies **per instance**:

| Feature | Typical Repetitions | Example |
|---------|---------------------|---------|
| ui-Page | 5-20 | Landing, Dashboard, Settings, Profile, etc. |
| forms | 3-10 | Login, Registration, Contact, Settings, etc. |
| tables | 2-8 | Users list, Orders list, Products list, etc. |
| file-upload | 1-3 | Profile photo, Documents, Media gallery |
| CRUD | 3-10 | Users, Products, Orders, Categories, etc. |

### Single Implementation Features
These features are typically implemented once per project:

| Feature | Notes |
|---------|-------|
| RBAC | One permission system per app |
| websocket | One real-time infrastructure |
| payment | One payment integration |
| caching | One caching layer |
| background-tasks | One job queue system |

---

## Sample Project Estimation with Process Breakdown

### E-commerce Project Example

| Team | Process | Feature | Count | Hours/Each | Total Hours |
|------|---------|---------|-------|------------|-------------|
| Backend | Data Operations | CRUD | 5 | 4 | 20 |
| Backend | Real-time | websocket | 1 | 12 | 12 |
| Backend | Media Handling | file-upload | 2 | 4 | 8 |
| Backend | Data Operations | filtering | 3 | 4 | 12 |
| Backend | Communication | push-notifications | 1 | 12 | 12 |
| Backend | Integration | payment | 1 | 8 | 8 |
| Frontend | Content Management | ui-Page | 8 | 6 | 48 |
| Frontend | Content Management | tables | 4 | 5 | 20 |
| Frontend | User Management | RBAC | 1 | 12 | 12 |
| Frontend | Communication | messaging | 1 | 12 | 12 |
| Frontend | Content Management | filtering | 3 | 4 | 12 |
| **Total** | | | | | **176** |

### Summary by Process

| Process | Frontend Hours | Backend Hours | Total |
|---------|----------------|---------------|-------|
| User Management | 12 | 0 | 12 |
| Content Management | 80 | 0 | 80 |
| Communication | 12 | 12 | 24 |
| Data Operations | 0 | 32 | 32 |
| Media Handling | 0 | 8 | 8 |
| Integration | 0 | 8 | 8 |
| Real-time | 0 | 12 | 12 |
| **Total** | **104** | **72** | **176** |
