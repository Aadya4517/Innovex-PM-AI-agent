# Innovex-PM-AI-agent

## Run locally

Start the FastAPI backend in one terminal:

```powershell
python -m uvicorn main:app --reload --port 8000
```

In a second terminal, start the React dashboard:

```powershell
npm install
npm run dev
```

Open the Vite URL printed in the terminal (by default, http://localhost:5173).
The API health endpoint at http://localhost:8000/ returns JSON; it is not the
dashboard page. The dashboard calls the backend on port 8000.

## Configure integrations

Install backend dependencies, then copy `.env.example` to `.env` in the project
root (the same folder as `main.py`) and replace the example values. Never commit
`.env`; it is ignored by Git.

```powershell
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

- `GEMINI_API_KEY`: enables Gemini-generated dashboard summaries and answers to
  project questions. Without it, the dashboard uses rule-based summaries and
  simple status/deadline questions.
- `JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN`, and `JIRA_PROJECT_KEY`: read
  issues from Jira. The Jira account also needs permission to add issue comments
  for the Send alerts action.
- `SLACK_WEBHOOK`: enables PM reports and alert delivery to the Slack channel
  selected when the webhook was created.
- `DAILY_SLACK_REPORT_ENABLED=true`: turns on the scheduled digest at 09:00 in
  `SCHEDULER_TIMEZONE` (default `Asia/Kolkata`). It is disabled by default.

Restart the backend after editing `.env`. Check which integrations are configured
without revealing their secret values at `http://localhost:8000/integrations/status`.

## Try the integrations and prediction features

1. **Gemini:** open the dashboard and check that the summary is marked “Gemini.”
   Ask a project question such as “Which tasks are delayed?” in “Ask about this
   project.” The answer shows its source. If Gemini is unavailable, the dashboard
   falls back to local rules.
2. **Delay model:** use the ML Delay Forecast form or send this request:

   ```powershell
   Invoke-RestMethod -Method Post -Uri http://localhost:8000/delay-forecast `
     -ContentType 'application/json' `
     -Body '{"estimated_days":5,"priority":3,"dependencies":2,"team_size":3}'
   ```

   This model was trained on a small sample dataset, so treat its probability as
   a demonstration signal. `/delay-risk` is a separate estimate-versus-actual
   duration calculator.
3. **Slack alerts:** set `SLACK_WEBHOOK`, restart the backend, then click “Send
   alerts now” on the dashboard. The response reports whether Slack accepted the
   message. The PM Sprint Report button also sends its report to Slack.
4. **Jira updates:** with Jira configured, make a test issue overdue, due within
   seven days, blocked, or delayed. Click “Send alerts now”; the app attempts to
   add an alert comment to each matching Jira issue. Confirm the comment in that
   issue’s Activity panel. This is an explicit action and can create comments.
5. **Scheduled Slack digest:** set `DAILY_SLACK_REPORT_ENABLED=true`, ensure the
   webhook is configured, and restart the backend. The daily job runs at 09:00
   in the configured timezone; use “Send alerts now” for an immediate delivery
   check rather than waiting for the schedule.

The `.github/workflows/ci.yml` workflow checks Python syntax and builds the
frontend on pushes and pull requests. It does not contain API credentials or call
the external Gemini, Jira, or Slack services.

Team name=Strangers Code
Team members are:
Mehak Sethi
Aadya Gupta
Akanchha Singh
Simarjeet Kaur

Problem statement selected- The PM AI agent

The PM AI Agent automates project management tasks by analyzing task data and
providing intelligent insights. It generates:

- Project status summaries
- Daily stand-up updates
- Deadline tracking alerts
- Risk prediction (Low / Medium / High)
- Natural language responses to user queries
- One click PM report
- Bottleneck Finder
- Task Priority Scorer

The AI logic is modular and designed to simulate real-world integrations with
tools like Jira, Trello, and Slack.




PM AI Agent – Project Proposal
Project Overview

The PM AI Agent is an intelligent project management assistant designed to help project managers monitor task progress, identify risks, and communicate updates efficiently.
It integrates with Jira for task tracking and Slack for team communication, supported by a web-based dashboard and automated reporting.

Phase 1: MVP with Real Integrations 
Objective

To build a fully functional, end-to-end PM AI Agent with real integrations, automation, and visualization, suitable for demonstrations and proof-of-concept.

Phase 1 Features
1. Jira Integration

Connects to Jira using REST APIs

Fetches real-time issues and task statuses

Categorizes tasks into:

Completed

In Progress

Delayed

Forms the primary data source for analytics

2️.  Slack Integration with OAuth

Slack OAuth 2.0 authentication

Bot user creation and workspace installation

Secure token-based communication

Sends:

Manual messages

Automated daily project summaries

3.  AI-Based Task Summarization

Analyzes task status data

Generates concise human-readable summaries

Uses structured text and emojis for clarity

Formats summaries suitable for Slack messages

4️.  PM Dashboard (Frontend)

Web dashboard built using React

Displays:

Number of completed tasks

Number of tasks in progress

Number of delayed tasks

Button to trigger daily Slack summary

Clean and intuitive UI for managers

5️.  Backend API Layer

Built using FastAPI

REST APIs for:

Jira issue retrieval

Project summary generation

Slack message delivery

Dashboard analytics

Auto-generated API documentation using Swagger UI

6️.  Scheduler Automation

Background scheduler to send daily summaries

Enables automated reporting without manual intervention

7️.  Ngrok Integration 

Ngrok used to expose the local backend server to the internet

Enables:

Slack OAuth callback handling

Slack webhook communication

Allows real Slack integration without cloud deployment

Essential for testing and demonstration in local environments

Phase 1 Technology Stack
Layer	Technology
Frontend	React.js
Backend	FastAPI (Python)
Integrations	Jira API, Slack API
Authentication	OAuth 2.0
AI Logic	Rule-based task summarization
Scheduler	Background jobs
Public Access	Ngrok
API Docs	Swagger (OpenAPI)
Phase 1 Outcome

Fully working project management assistant

Real-time Jira data processing

Real Slack message delivery

Web-based dashboard visualization

Automation enabled using scheduler

Demonstration-ready system

Phase 2: Intelligence, Prediction & Scalability (Future Scope)
 Objective

To transform the PM AI Agent into a predictive, scalable, and enterprise-ready system.

Phase 2 Planned Features
1.  Delay Risk Prediction

Analyze historical task data

Predict likelihood of delays

Machine learning models for risk scoring

Proactive alerts before deadlines are missed

2. Multi-Project Support

Track multiple projects simultaneously

Project-wise dashboards

Cross-project performance analytics

3. Advanced AI Summaries

Natural language summaries using LLMs

Personalized summaries for:

Project Managers

Team Members

Stakeholders

Priority-based insights

4. Smart Alerts & Notifications

Deadline reminders

Task stagnation alerts

Slack notifications based on AI rules

5. Role-Based Access Control

Admin, Manager, Developer roles

Permission-based data visibility

Secure authentication using JWT

6. Production-Ready Deployment

Dockerized backend and frontend

Cloud deployment (AWS / GCP / Azure)

CI/CD pipeline for automated deployment

Removal of Ngrok dependency

Phase 2 Technology Stack (Planned)
Feature	Technology
Machine Learning	Scikit-learn / TensorFlow
AI Summaries	LLM APIs
Database	PostgreSQL
Authentication	JWT
Deployment	Docker + Cloud
Monitoring	Logs & Metrics


Deployment Strategy
Phase 1

Local deployment

Ngrok for public access

Manual startup

Suitable for development & demo

Phase 2

Cloud-based deployment

Docker containers

CI/CD automation

Scalable and secure production setup

Conclusion

Phase-1 successfully demonstrates a real, working AI-assisted project management system with live integrations and automation.
Phase-2 will enhance intelligence, prediction, scalability, and enterprise usability.
