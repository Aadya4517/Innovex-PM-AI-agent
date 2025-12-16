# ML API Contract

Input:
{
  "estimated_days": int,
  "priority": int,
  "dependencies": int,
  "team_size": int
}

Output:
{
  "risk_percentage": float,
  "risk_level": string
}

Purpose:
Used by backend API to predict task delay risk.
