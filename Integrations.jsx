function Integrations() {
  const connectSlack = () => {
    window.location.href = "http://localhost:3001/api/slack/login"
  }

  const connectJira = () => {
    window.location.href = "http://localhost:3001/api/jira/login"
  }

  return (
    <div>
      <h2>Integrations</h2>

      <button onClick={() => window.location.href = "http://localhost:8000/slack/login"}>
        Connect Slack
      </button>


      <br /><br />

      <button onClick={connectJira}>
        Connect Jira
      </button>
    </div>
  )
}

export default Integrations
