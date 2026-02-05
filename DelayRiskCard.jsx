import { useState } from "react"

export default function DelayRiskCard() {
  const [estimated, setEstimated] = useState("")
  const [actual, setActual] = useState("")
  const [result, setResult] = useState(null)

  const predict = async () => {
    const res = await fetch("http://localhost:8000/delay-risk", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        estimated_days: Number(estimated),
        actual_days: Number(actual)
      })
    })

    const data = await res.json()
    setResult(data)
  }

  return (
    <div className="card">
      <h2>Delay Risk Prediction</h2>

      <input
        placeholder="Estimated days"
        value={estimated}
        onChange={e => setEstimated(e.target.value)}
      />

      <input
        placeholder="Actual days"
        value={actual}
        onChange={e => setActual(e.target.value)}
      />

      <button onClick={predict}>Predict Risk</button>

      {result && (
        <p>
          <strong>Risk:</strong> {result.risk}
          <br />
          {result.explanation}
        </p>
      )}
    </div>
  )
}
