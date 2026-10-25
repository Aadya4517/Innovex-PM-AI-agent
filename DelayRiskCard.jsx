import { useState } from "react"

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000"

export default function DelayRiskCard() {
  const [estimated, setEstimated] = useState("")
  const [actual, setActual] = useState("")
  const [result, setResult] = useState(null)
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)

  const predict = async () => {
    setError("")
    setResult(null)
    setLoading(true)

    try {
      const res = await fetch(`${API_URL}/delay-risk`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          estimated_days: Number(estimated),
          actual_days: Number(actual)
        })
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.detail || "Risk prediction failed")
      setResult(data)
    } catch (err) {
      setError(err.message || "Could not calculate delay risk")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card">
      <h2>Delay Risk Prediction</h2>

      <input
        type="number"
        min="1"
        placeholder="Estimated days"
        value={estimated}
        onChange={e => setEstimated(e.target.value)}
      />

      <input
        type="number"
        min="0"
        placeholder="Actual days"
        value={actual}
        onChange={e => setActual(e.target.value)}
      />

      <button onClick={predict} disabled={!estimated || !actual || loading}>
        {loading ? "Calculating..." : "Predict Risk"}
      </button>

      {error && <p className="red">{error}</p>}

      {result && (
        <p>
          <strong>Risk:</strong> {result.risk} ({result.risk_percent}%)
          <br />
          {result.explanation}
        </p>
      )}
    </div>
  )
}
