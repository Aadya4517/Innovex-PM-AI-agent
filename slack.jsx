import { useState } from "react"

export default function Slack() {
  const [message, setMessage] = useState("")

  const sendMessage = async () => {
    await fetch("http://localhost:8000/slack/send", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        channel: "#general",
        text: message
      })
    })
  }

  return (
    <>
      <h2>Send Slack Message</h2>
      <input
        value={message}
        onChange={e => setMessage(e.target.value)}
        placeholder="Message"
      />
      <button onClick={sendMessage}>Send</button>
    </>
  )
}
