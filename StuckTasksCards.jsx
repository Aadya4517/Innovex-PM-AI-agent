export default function StuckTasksCard({ tasks = [] }) {
  return (
    <div className="health-card danger">
      <h3 className="card-title">Bottleneck Finder</h3>

      {tasks.length === 0 && (
        <p className="empty">No delayed or blocked tasks</p>
      )}

      {tasks.map(task => (
        <div key={task.id} className="task-row">
          <span className="task-name">{task.title}</span>
          <span className="stuck-meta">{task.status}{task.days_in_status ? ` · ${task.days_in_status} days in status` : ""}</span>
        </div>
      ))}
    </div>
  )
}
