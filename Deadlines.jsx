import { useState } from "react"
import api from "../services/api"

function Deadlines() {
  const [tasks, setTasks] = useState([])

  const fetchDeadlines = async () => {
    const res = await api.get("/deadlines")
    setTasks(res.data)
  }

  return (
    <div>
      <h2>Deadlines</h2>
      <button onClick={fetchDeadlines}>View Deadlines</button>
      <ul>
        {tasks.map((t, i) => (
          <li key={i}>
            {t.title} | {t.deadline} | {t.status}
          </li>
        ))}
      </ul>
    </div>
  )
}

export default Deadlines
