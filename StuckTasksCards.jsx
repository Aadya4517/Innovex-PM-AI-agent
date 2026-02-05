export default function StuckTasksCard({ tasks = [] }) {
  return (
    <div className="health-card danger">
      <h3 className="card-title">⏳ Stuck Tasks</h3>

      {tasks.length === 0 && (
        <p className="empty">No stuck tasks 🎉</p>
      )}

      {tasks.map(task => (
        <div key={task.id} className="task-row">
          <span className="task-name">{task.title}</span>
          <span className="stuck-meta">
            Stuck for {task.days_in_status} days
          </span>
        </div>
      ))}
    </div>
  )
}
