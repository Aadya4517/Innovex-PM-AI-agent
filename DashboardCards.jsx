export default function DashboardCards({ counts }) {
  return (
    <div style={{ display: "flex", gap: "20px" }}>
      <Card title="Completed" value={counts.completed} color="green" />
      <Card title="In Progress" value={counts.in_progress} color="orange" />
      <Card title="Delayed" value={counts.delayed} color="red" />
    </div>
  )
}

function Card({ title, value, color }) {
  return (
    <div style={{
      border: `3px solid ${color}`,
      borderRadius: "12px",
      padding: "20px",
      width: "200px",
      textAlign: "center"
    }}>
      <h3>{title}</h3>
      <h1 style={{ color }}>{value}</h1>
    </div>
  )
}
