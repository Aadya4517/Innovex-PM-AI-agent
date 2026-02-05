export default function PriorityPanel({ tasks = [] }) {
  return (
    <div className="health-card">
      <h3 className="card-title">Task Priority Scorer</h3>

      {tasks.length === 0 && (
        <p className="empty">No tasks available</p>
      )}

      {tasks.map(task => (
        <div key={task.id} className="task-row">
          <div className="task-info">
            <span className="task-name">{task.title}</span>
            <span className={`priority-badge ${task.priority.toLowerCase()}`}>
              {task.priority}
            </span>
          </div>

          <span className="task-meta">
            {task.days_in_status} days
          </span>
        </div>
      ))}
    </div>
  )
}
