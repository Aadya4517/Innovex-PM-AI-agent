import { useState } from "react"
import api from "../services/api"

function Status() {
  const [data, setData] = useState(null)

  const fetchStatus = async () => {
    const res = await api.get("/status")
    setData(res.data)
  }

  return (
    <div>
      <h2>Project Status</h2>
      <button onClick={fetchStatus}>Get Project Status</button>
      {data && <pre>{JSON.stringify(data, null, 2)}</pre>}
    </div>
  )
}

export default Status
