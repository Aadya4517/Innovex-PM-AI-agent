export default function StatsCard({ title, value, color }) {
  return (
    <div style={card}>
      <p style={{ fontSize: 14, opacity: 0.6 }}>{title}</p>
      <h1 style={{ color, margin: 0 }}>{value}</h1>
    </div>
  )
}

const card = {
  background: "#ffffff",
  borderRadius: 18,
  padding: "20px 28px",
  minWidth: 180,
  boxShadow: "0 12px 30px rgba(0,0,0,0.15)"
}


function Card({ title, value, color, theme }) {
  return (
    <div
      style={{
        background: theme.card,
        borderRadius: 14,
        padding: 22,
        width: 190,
        boxShadow: "0 10px 20px rgba(0,0,0,0.15)",
        transition: "0.3s"
      }}
    >
      <p
        style={{
          margin: 0,
          fontSize: 14,
          fontWeight: 600,
          color: theme.muted
        }}
      >
        {title}
      </p>

      <h1
        style={{
          marginTop: 10,
          marginBottom: 0,
          fontSize: 36,
          color
        }}
      >
        {value}
      </h1>
    </div>
  )
}

const container = {
  display: "flex",
  gap: 20,
  flexWrap: "wrap",
  marginTop: 30
}
