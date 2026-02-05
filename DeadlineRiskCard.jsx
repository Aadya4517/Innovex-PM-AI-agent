import { useEffect, useState } from "react"

function DeadlineRiskCard() {
  const [risk, setRisk] = useState({
    warning: 0,
    overdue: 0
  })

  useEffect(() => {
    fetch("http://localhost:8000/deadline-risk")
      .then(res => res.json())
      .then(data => {
        setRisk({
          warning: data.warning ?? 0,
          overdue: data.overdue ?? 0
        })
      })
      .catch(() => {
        setRisk({ warning: 0, overdue: 0 })
      })
  }, [])

  return (
    <div className="card">
      <h3>Deadline Risk</h3>

      <p style={{ color: "orange" }}>
        ⚠ Near Deadline: {risk.warning}
      </p>

      <p style={{ color: "red" }}>
        ⛔ Overdue: {risk.overdue}
      </p>
    </div>
  )
}

export default DeadlineRiskCard
