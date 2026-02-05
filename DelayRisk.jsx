import { useState } from "react"

export default function DelayRisk() {
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
    setResult(await res.json())
  }

  return (
    <>
      <h2>Delay Risk Prediction</h2>

      <input placeholder="Estimated Days"
        value={estimated}
        onChange={e => setEstimated(e.target.value)} />

      <input placeholder="Actual Days"
        value={actual}
        onChange={e => setActual(e.target.value)} />

      <button onClick={predict}>Predict</button>

      {result && (
        <div>
          <h3>Risk: {result.risk}</h3>
          <p>{result.explanation}</p>
        </div>
      )}
    </>
  )
}
