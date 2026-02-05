const express = require("express")
const axios = require("axios")
const cors = require("cors")

const app = express()
app.use(cors())
app.use(express.json())

app.get("/api/status", async (req, res) => {
  const response = await axios.get("http://127.0.0.1:8000/status-summary")
  res.json(response.data)
})

app.listen(3001, () => {
  console.log("Express server running on port 3001")
})

app.get("/api/slack/login", (req, res) => {
  res.redirect("http://127.0.0.1:8000/slack/oauth/login")
})

app.get("/api/jira/login", (req, res) => {
  res.redirect("http://127.0.0.1:8000/jira/oauth/login")
})
