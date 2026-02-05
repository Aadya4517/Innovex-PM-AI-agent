import { useState } from "react"

export default function PMReportCard() {
  const [loading, setLoading] = useState(false)
  const [report, setReport] = useState(null)
  const [error, setError] = useState(null)

  const generateReport = async () => {
    setLoading(true)
    setError(null)
    setReport(null)

    try {
      const res = await fetch("http://localhost:8000/pm-report", {
        method: "POST"
      })

      if (!res.ok) {
        throw new Error("Request failed")
      }

      const data = await res.json()
      setReport(data)
    } catch (e) {
      setError("Failed to generate report or send to Slack")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card">
      <h3>PM Sprint Report</h3>

      {!loading && !report && (
        <button className="primary-btn" onClick={generateReport}>
          Generate & Send to Slack
        </button>
      )}

      {loading && <p>⏳ Generating report & sending to Slack...</p>}

      {error && <p className="red">{error}</p>}

      {report && (
        <div style={{ marginTop: "12px", textAlign: "left" }}>
          <p><b>Total Tasks:</b> {report.total_tasks ?? 0}</p>
          <p><b>Completed:</b> {report.completed ?? 0}</p>
          <p><b>In Progress:</b> {report.in_progress ?? 0}</p>
          <p><b>Delayed:</b> {report.delayed ?? 0}</p>

          {Array.isArray(report.high_risk_tasks) && report.high_risk_tasks.length > 0 ? (
            <>
              <p><b>⚠ High Risk Tasks:</b></p>
              <ul>
                {report.high_risk_tasks.map((t, i) => (
                  <li key={i}>
                    {t.id} – {t.title}
                  </li>
                ))}
              </ul>
            </>
          ) : (
            <p>🎉 No high-risk tasks</p>
          )}
        </div>
      )}
    </div>
  )
}
