SYSTEM = (
  "You are a careful assistant. "
  "Always follow format:\n"
  "1) Final: <yes|no|maybe>\n"
  "2) Evidence:\n- <bullet 1>\n- <bullet 2>"
)

def wrap(user_block: str) -> str:
    return f"{SYSTEM}\n\n{user_block}"
