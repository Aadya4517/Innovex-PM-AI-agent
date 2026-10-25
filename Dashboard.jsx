import { useEffect, useState } from "react"
import DelayRiskCard from "./DelayRiskCard"
import DeadlineRiskCard from "./DeadlineRiskCard"
import PriorityPanel from "./PriorityPanel"
import StuckTasksCard from "./StuckTasksCards"
import PMReportCard from "./PMReportCard"
import DelayForecastCard from "./DelayForecastCard"

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000"

export default function Dashboard() {
  const [dark, setDark] = useState(false)
  const [stats, setStats] = useState({
    total: 0,
    completed: 0,
    in_progress: 0,
    delayed: 0,
    health: 100
  })
  const [tasks, setTasks] = useState([])
  const [summary, setSummary] = useState("")
  const [summarySource, setSummarySource] = useState("")
  const [standup, setStandup] = useState("")
  const [error, setError] = useState("")
  const [taskTitle, setTaskTitle] = useState("")
  const [taskStatus, setTaskStatus] = useState("Not Started")
  const [taskDueDate, setTaskDueDate] = useState("")
  const [savingTask, setSavingTask] = useState(false)
  const [taskMessage, setTaskMessage] = useState("")
  const [projectQuestion, setProjectQuestion] = useState("")
  const [projectAnswer, setProjectAnswer] = useState("")
  const [queryLoading, setQueryLoading] = useState(false)
  const [alertMessage, setAlertMessage] = useState("")
  const [alertLoading, setAlertLoading] = useState(false)
  const [integrationStatus, setIntegrationStatus] = useState(null)

  function loadDashboard() {
    return fetch(`${API_URL}/dashboard`)
      .then(res => {
        if (!res.ok) throw new Error(`Dashboard request failed (${res.status})`)
        return res.json()
      })
      .then(data => {
        const total = data.counts.total
        const health =
          total === 0
            ? 100
            : Math.round((data.counts.completed / total) * 100)

        setStats({
          total,
          completed: data.counts.completed,
          in_progress: data.counts.in_progress,
          delayed: data.counts.delayed,
          health
        })
        setTasks(data.tasks || [])
        setSummary(data.summary || "")
        setSummarySource(data.summary_source || "rules")
        setStandup(data.standup || "")
      })
      .catch(() => setError("Could not load dashboard data. Check that the backend is running on port 8000."))
  }

  useEffect(() => {
    loadDashboard()
    fetch(`${API_URL}/integrations/status`).then(response => response.json()).then(setIntegrationStatus).catch(() => {})
  }, [])

  async function askProject(event) {
    event.preventDefault()
    setQueryLoading(true)
    setProjectAnswer("")
    try {
      const response = await fetch(`${API_URL}/query`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: projectQuestion })
      })
      const data = await response.json()
      if (!response.ok) throw new Error(data.detail || "Could not answer the question")
      setProjectAnswer(`${data.answer} (via ${data.source})`)
    } catch (err) {
      setProjectAnswer(err.message || "Could not reach the backend")
    } finally {
      setQueryLoading(false)
    }
  }

  async function sendAlerts() {
    setAlertLoading(true)
    setAlertMessage("")
    try {
      const response = await fetch(`${API_URL}/alerts/send`, { method: "POST" })
      const data = await response.json()
      if (!response.ok) throw new Error(data.detail || "Could not send alerts")
      const slack = data.slack?.sent ? "Slack sent" : `Slack not sent: ${data.slack?.reason || "not configured"}`
      const jiraSent = data.jira_comments.filter(item => item.sent).length
      const jiraFailed = data.jira_comments.filter(item => !item.sent).length
      const jira = !integrationStatus?.jira
        ? "; Jira not configured"
        : data.jira_comments.length
          ? `; Jira comments ${jiraSent} sent, ${jiraFailed} failed`
          : "; no Jira issues needed comments"
      setAlertMessage(`${data.alert_count} alert(s) checked. ${slack}${jira}`)
    } catch (err) {
      setAlertMessage(err.message || "Could not send alerts")
    } finally {
      setAlertLoading(false)
    }
  }

  async function handleAddTask(event) {
    event.preventDefault()
    setSavingTask(true)
    setTaskMessage("")
    try {
      const response = await fetch(`${API_URL}/tasks`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: taskTitle,
          status: taskStatus,
          due_date: taskDueDate || null
        })
      })
      const result = await response.json()
      if (!response.ok) throw new Error(result.detail || "Could not add task")
      setTaskTitle("")
      setTaskStatus("Not Started")
      setTaskDueDate("")
      setTaskMessage("Task added.")
      await loadDashboard()
    } catch (err) {
      setTaskMessage(err.message || "Could not add task. Check that the backend is running.")
    } finally {
      setSavingTask(false)
    }
  }

  useEffect(() => {
    document.body.setAttribute("data-theme", dark ? "dark" : "light")
  }, [dark])

  return (
    <div className="dashboard">
      <div className="header">
        <div>
          <h1>PM AI Agent</h1>
          <p className="live">● Connected to project data</p>
        </div>

        <button
          className="theme-btn"
          onClick={() => setDark(d => !d)}
        >
          {dark ? "☀ Light Mode" : "🌙 Dark Mode"}
        </button>
      </div>

      {error && <p className="error-banner">{error}</p>}

      <div className="stats-grid">
        <Stat title="Total Tasks" value={stats.total} color="blue" />
        <Stat title="Completed" value={stats.completed} color="green" />
        <Stat title="In Progress" value={stats.in_progress} color="yellow" />
        <Stat title="Delayed" value={stats.delayed} color="red" />
        <Stat title="Health %" value={stats.health} color="green" />
      </div>

      <h2 className="section-title">Project Overview</h2>
      <div className="overview-grid">
        <section className="health-card">
          <h3 className="card-title">Status Summary {summarySource && <span className="muted">({summarySource === "gemini" ? "Gemini" : "rule based"})</span>}</h3>
          <pre className="feature-text">{summary || "Loading summary..."}</pre>
        </section>
        <section className="health-card">
          <h3 className="card-title">Daily Stand-up</h3>
          <pre className="feature-text">{standup || "Loading stand-up..."}</pre>
        </section>
      </div>

      <section className="health-card project-query-card">
        <h3 className="card-title">Ask about this project</h3>
        <form className="query-form" onSubmit={askProject}>
          <input value={projectQuestion} onChange={event => setProjectQuestion(event.target.value)} minLength={2} maxLength={500} required placeholder="Which tasks are overdue? What is blocked?" />
          <button className="add-task-btn" disabled={queryLoading}>{queryLoading ? "Thinking…" : "Ask"}</button>
        </form>
        {projectAnswer && <p className="feature-text" role="status">{projectAnswer}</p>}
      </section>

      <h2 className="section-title">Risk Intelligence</h2>
      <div className="risk-grid">
        <DelayRiskCard />
        <DeadlineRiskCard />
        <DelayForecastCard />
      </div>

      <h2 className="section-title">Task Health</h2>
      <div className="risk-grid">
        <PriorityPanel tasks={tasks} />
        <StuckTasksCard tasks={tasks.filter(task => ["delayed", "blocked", "overdue"].includes(task.status.toLowerCase()) || (task.days_in_status || 0) >= 5)} />
      </div>

      <h2 className="section-title">All Tasks</h2>
      <section className="health-card task-list">
        <form className="add-task-form" onSubmit={handleAddTask}>
          <h3 className="card-title">Add a task</h3>
          <label>
            Task name
            <input value={taskTitle} onChange={event => setTaskTitle(event.target.value)} maxLength={200} required placeholder="e.g. Prepare launch checklist" />
          </label>
          <label>
            Status
            <select value={taskStatus} onChange={event => setTaskStatus(event.target.value)}>
              <option>Not Started</option>
              <option>In Progress</option>
              <option>Completed</option>
              <option>Delayed</option>
              <option>Blocked</option>
            </select>
          </label>
          <label>
            Due date
            <input type="date" value={taskDueDate} onChange={event => setTaskDueDate(event.target.value)} />
          </label>
          <button className="add-task-btn" type="submit" disabled={savingTask}>{savingTask ? "Adding…" : "Add task"}</button>
          {taskMessage && <p className="task-message" role="status">{taskMessage}</p>}
        </form>
        {tasks.length === 0 ? (
          <p className="empty">No tasks were returned by the backend.</p>
        ) : (
          <div className="task-table-wrap">
            <table>
              <thead>
                <tr><th>Task</th><th>Status</th><th>Priority</th><th>Due date</th></tr>
              </thead>
              <tbody>
                {tasks.map(task => (
                  <tr key={task.id}>
                    <td>{task.title}</td>
                    <td>{task.status}</td>
                    <td><span className={`badge ${task.priority.toLowerCase()}`}>{task.priority}</span></td>
                    <td>{task.due_date || "Not set"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>

      <h2 className="section-title">Automation</h2>
      <div className="automation-grid">
        <PMReportCard />
        <section className="health-card">
          <h3 className="card-title">Deadline and risk alerts</h3>
          <p className="muted">Send current alerts to Slack and add comments to matching Jira issues.</p>
          <button className="add-task-btn" onClick={sendAlerts} disabled={alertLoading}>{alertLoading ? "Sending…" : "Send alerts now"}</button>
          {alertMessage && <p className="task-message" role="status">{alertMessage}</p>}
          {integrationStatus && <p className="integration-status">Gemini: {integrationStatus.gemini ? "connected" : "not configured"} · Jira: {integrationStatus.jira ? "connected" : "not configured"} · Slack: {integrationStatus.slack ? "connected" : "not configured"} · ML model: {integrationStatus.delay_model ? "available" : "missing"}</p>}
        </section>
      </div>
    </div>
  )
}

function Stat({ title, value, color }) {
  return (
    <div className={`card stat ${color}`}>
      <p>{title}</p>
      <h2>{value}</h2>
    </div>
  )
}
