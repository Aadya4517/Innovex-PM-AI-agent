import { useTheme } from "../context/ThemeContext"

export default function ThemeToggle() {
  const { theme, toggleTheme } = useTheme()

  return (
    <button
      onClick={toggleTheme}
      style={{
        position: "fixed",
        top: 20,
        right: 20,
        padding: "10px 16px",
        borderRadius: 12,
        border: "none",
        cursor: "pointer",
        background: "var(--card)",
        color: "var(--text)",
        fontWeight: 600
      }}
    >
      {theme === "dark" ? "🌙 Dark" : "☀️ Light"}
    </button>
  )
}
