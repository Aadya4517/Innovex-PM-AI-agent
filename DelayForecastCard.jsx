import { useState } from "react"

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000"

export default function DelayForecastCard() {
  const [values, setValues] = useState({ estimated_days: "5", priority: "3", dependencies: "2", team_size: "3" })
  const [result, setResult] = useState(null)
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)

  function update(event) {
    setValues(current => ({ ...current, [event.target.name]: event.target.value }))
  }

  async function predict(event) {
    event.preventDefault()
    setLoading(true)
    setError("")
    setResult(null)
    try {
      const response = await fetch(`${API_URL}/delay-forecast`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(Object.fromEntries(Object.entries(values).map(([key, value]) => [key, Number(value)])))
      })
      const data = await response.json()
      if (!response.ok) throw new Error(data.detail || "Forecast failed")
      setResult(data)
    } catch (err) {
      setError(err.message || "Could not reach the delay model")
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="health-card">
      <h3 className="card-title">ML Delay Forecast</h3>
      <form className="forecast-form" onSubmit={predict}>
        <label>Estimated days<input name="estimated_days" type="number" min="0.1" step="0.1" value={values.estimated_days} onChange={update} required /></label>
        <label>Priority (1–5)<input name="priority" type="number" min="1" max="5" value={values.priority} onChange={update} required /></label>
        <label>Dependencies<input name="dependencies" type="number" min="0" max="100" value={values.dependencies} onChange={update} required /></label>
        <label>Team size<input name="team_size" type="number" min="1" max="100" value={values.team_size} onChange={update} required /></label>
        <button className="add-task-btn" disabled={loading}>{loading ? "Predicting…" : "Forecast delay"}</button>
      </form>
      {error && <p className="error-banner">{error}</p>}
      {result && <p><strong>{result.risk} — {result.risk_percent}%</strong><br />{result.note}</p>}
    </section>
  )
}
