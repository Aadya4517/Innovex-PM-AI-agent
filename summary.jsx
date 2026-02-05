import { useEffect, useState } from "react"

export default function Summary() {
  const [summary, setSummary] = useState("")

  const fetchSummary = async () => {
    const res = await fetch("http://localhost:8000/summary")
    const data = await res.json()
    setSummary(data.summary)
  }

  return (
    <div style={{ padding: "20px" }}>
      <h2>📊 Daily Project Summary</h2>

      <button onClick={fetchSummary}>
        Generate Summary
      </button>

      <pre style={{
        background: "#f3f4f6",
        padding: "15px",
        marginTop: "15px",
        borderRadius: "8px",
        fontSize: "16px"
      }}>
        {summary}
      </pre>
      <button
        style={{ marginTop: "10px", background: "#22c55e", color: "white", padding: "8px 12px" }}
        onClick={async () => {
        await fetch("http://localhost:8000/slack/send-summary", { method: "POST" })
     alert("Summary sent to Slack 🚀")
  }}
>
  Send to Slack
</button>

    </div>
  )
}
