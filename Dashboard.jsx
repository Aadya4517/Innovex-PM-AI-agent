import { useEffect, useState } from "react"
import DelayRiskCard from "../components/DelayRiskCard"
import DeadlineRiskCard from "../components/DeadlineRiskCard"
import PriorityPanel from "../components/PriorityPanel"
import StuckTasksCard from "../components/StuckTasksCards"
import PMReportCard from "../components/PMReportCard"

export default function Dashboard() {
  const [dark, setDark] = useState(false)

  const [stats, setStats] = useState({
    projects: 0,
    completed: 0,
    in_progress: 0,
    delayed: 0,
    health: 100
  })

  const [reportStatus, setReportStatus] = useState("idle")

  /* Fetch dashboard stats */
  useEffect(() => {
    fetch("http://localhost:8000/dashboard")
      .then(res => res.json())
      .then(data => {
        const total =
          data.counts.completed +
          data.counts.in_progress +
          data.counts.delayed

        const health =
          total === 0
            ? 100
            : Math.round((data.counts.completed / total) * 100)

        setStats({
          projects: total,
          completed: data.counts.completed,
          in_progress: data.counts.in_progress,
          delayed: data.counts.delayed,
          health
        })
      })
      .catch(() => console.log("Backend not reachable"))
  }, [])

  /* Theme toggle */
  useEffect(() => {
    document.body.setAttribute("data-theme", dark ? "dark" : "light")
  }, [dark])

  /* PM Report trigger */
  const generatePMReport = () => {
    setReportStatus("loading")

    fetch("http://localhost:8000/pm-report", {
      method: "POST"
    })
      .then(() => setReportStatus("done"))
      .catch(() => setReportStatus("error"))
  }

  return (
    <div className="dashboard">
      {/* Header */}
      <div className="header">
        <div>
          <h1>PM AI Agent</h1>
          <p className="live">● Live – Jira Sync</p>
        </div>

        <button
          className="theme-btn"
          onClick={() => setDark(d => !d)}
        >
          {dark ? "☀ Light Mode" : "🌙 Dark Mode"}
        </button>
      </div>

      {/* Stats */}
      <div className="stats-grid">
        <Stat title="Projects" value={stats.projects} color="blue" />
        <Stat title="Completed" value={stats.completed} color="green" />
        <Stat title="In Progress" value={stats.in_progress} color="yellow" />
        <Stat title="Delayed" value={stats.delayed} color="red" />
        <Stat title="Health %" value={stats.health} color="green" />
      </div>

      {/* Risk Intelligence */}
      <h2 className="section-title">Risk Intelligence</h2>
      <div className="risk-grid">
        <DelayRiskCard />
        <DeadlineRiskCard />
      </div>

      {/* Task Health */}
      <h2 className="section-title">Task Health</h2>
      <div className="risk-grid">
        <PriorityPanel />
        <StuckTasksCard />
      </div>

      {/* Automation */}
      <h2 className="section-title">Automation</h2>
      <div className="automation-grid">
        <PMReportCard
          status={reportStatus}
          onGenerate={generatePMReport}
        />
      </div>
    </div>
  )
}

/* Reusable Stat Card */
function Stat({ title, value, color }) {
  return (
    <div className={`card stat ${color}`}>
      <p>{title}</p>
      <h2>{value}</h2>
    </div>
  )
}
