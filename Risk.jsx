import { useState } from "react"
import api from "../services/api"

function Risk() {
  const [estimated, setEstimated] = useState("")
  const [actual, setActual] = useState("")
  const [result, setResult] = useState(null)

  const predictRisk = async () => {
    const res = await api.post("/predict", {
      estimated_days: Number(estimated),
      actual_days: Number(actual)
    })
    setResult(res.data)
  }

  return (
    <div>
      <h2>Delay Risk Prediction</h2>
      <input
        placeholder="Estimated Days"
        value={estimated}
        onChange={e => setEstimated(e.target.value)}
      />
      <input
        placeholder="Actual Days"
        value={actual}
        onChange={e => setActual(e.target.value)}
      />
      <button onClick={predictRisk}>Predict</button>
      {result && <pre>{JSON.stringify(result, null, 2)}</pre>}
    </div>
  )
}

export default Risk
