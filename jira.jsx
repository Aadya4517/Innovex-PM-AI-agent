import { useState } from "react"
import api from "../services/api"

function Jira() {
  const [issues, setIssues] = useState([])

  const fetchIssues = async () => {
    const res = await api.get("/jira/issues")
    setIssues(res.data)
  }

  return (
    <div>
      <h2>Jira Issues</h2>
      <button onClick={fetchIssues}>Fetch Jira Issues</button>
      <ul>
        {issues.map((i, idx) => (
          <li key={idx}>{i.key} - {i.summary}</li>
        ))}
      </ul>
    </div>
  )
}

export default Jira
