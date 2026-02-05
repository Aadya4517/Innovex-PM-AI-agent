export default function SlackActions() {
  const sendSummary = async () => {
    await fetch("http://localhost:8000/slack/send-summary", {
      method: "POST"
    })
    alert("Daily summary sent to Slack")
  }

  return (
    <div className="card white">
      <h3>Slack Actions</h3>

      <button className="action-btn" onClick={sendSummary}>
        📩 Send Daily Summary
      </button>

      <p className="hint">
        Auto alerts are sent for overdue & high-risk Jira tasks
      </p>
    </div>
  )
}
