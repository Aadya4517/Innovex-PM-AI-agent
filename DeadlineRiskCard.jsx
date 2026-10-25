import { useEffect, useState } from "react"

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000"

function DeadlineRiskCard() {
  const [risk, setRisk] = useState({
    warning: 0,
    overdue: 0,
    warningTasks: [],
    overdueTasks: [],
    error: ""
  })

  useEffect(() => {
    fetch(`${API_URL}/deadline-risk`)
      .then(res => {
        if (!res.ok) throw new Error(`Deadline request failed (${res.status})`)
        return res.json()
      })
      .then(data => {
        setRisk({
          warning: data.warning ?? 0,
          overdue: data.overdue ?? 0,
          warningTasks: data.warning_tasks ?? [],
          overdueTasks: data.overdue_tasks ?? [],
          error: ""
        })
      })
      .catch(error => setRisk(current => ({ ...current, error: error.message })))
  }, [])

  return (
    <div className="card">
      <h3>Deadline Risk</h3>

      <p style={{ color: "orange" }}>
        ⚠ Near Deadline: {risk.warning}
      </p>

      <p style={{ color: "red" }}>
        ⛔ Overdue: {risk.overdue}
      </p>
      {risk.error && <p className="red">{risk.error}</p>}
      {risk.overdueTasks.map(task => (
        <p className="deadline-task" key={task.id}>{task.id}: {task.title} ({task.due_date})</p>
      ))}
      {risk.warningTasks.map(task => (
        <p className="deadline-task" key={task.id}>{task.id}: {task.title} ({task.due_date})</p>
      ))}
    </div>
  )
}

export default DeadlineRiskCard
