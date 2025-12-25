# Innovex-PM-AI-agent
The PM AI Agent automates project management tasks by analyzing task data and
providing intelligent insights. It generates:

- Project status summaries
- Daily stand-up updates
- Deadline tracking alerts
- Risk prediction (Low / Medium / High)
- Natural language responses to user queries

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
