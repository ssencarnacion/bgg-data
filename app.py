# made with ChatGPT https://chatgpt.com/s/t_696a1db8829c8191a29e89daf59d5200

import os
import json
from flask import Flask, render_template_string, request

app = Flask(__name__)
PARSED_DIR = "parsed_data"

def pearson_similarity(user1_games, user2_games, min_common=5):
    # Find overlapping games with valid ratings
    common_games = [game for game in user1_games
                    if user1_games[game] is not None and user2_games.get(game) is not None]
    
    n_common = len(common_games)
    if n_common < 2:
        return None, n_common  # not enough overlap to compute meaningful correlation

    # Extract ratings
    u1 = [user1_games[game] for game in common_games]
    u2 = [user2_games[game] for game in common_games]

    # Means
    mean1 = sum(u1) / n_common
    mean2 = sum(u2) / n_common

    # Compute numerator and denominator
    numerator = sum((a - mean1) * (b - mean2) for a, b in zip(u1, u2))
    denominator = (sum((a - mean1)**2 for a in u1) * sum((b - mean2)**2 for b in u2)) ** 0.5

    if denominator == 0:
        return None, n_common

    r = numerator / denominator
    # normalize to 0-1 for user-friendly display
    similarity_normalized = (r + 1) / 2

    # Apply confidence adjustment: small overlap lowers the effective score
    confidence = min(1, n_common / min_common)
    similarity_confident = similarity_normalized * confidence

    return similarity_confident, n_common

@app.route("/", methods=["GET", "POST"])
def index():
    usernames = sorted(f.replace(".json", "") for f in os.listdir(PARSED_DIR) if f.endswith(".json"))
    similarity_score = None
    n_common = 0
    selected_user1 = selected_user2 = None

    if request.method == "POST":
        selected_user1 = request.form.get("user1")
        selected_user2 = request.form.get("user2")

        if selected_user1 and selected_user2:
            path1 = os.path.join(PARSED_DIR, f"{selected_user1}.json")
            path2 = os.path.join(PARSED_DIR, f"{selected_user2}.json")

            with open(path1, "r", encoding="utf-8") as f:
                user1_data = json.load(f)

            with open(path2, "r", encoding="utf-8") as f:
                user2_data = json.load(f)

            similarity_score, n_common = pearson_similarity(user1_data["games"], user2_data["games"])

    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>User Taste Similarity</title>
      <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        select { margin: 10px 0; padding: 5px; width: 200px; }
        label { display: block; margin-top: 20px; }
        .score { margin-top: 20px; font-weight: bold; }
      </style>
    </head>
    <body>
      <h1>Board Game Geek Taste Similarity (Pearson)</h1>

      <form method="POST">
        <label for="user1">Select first user:</label>
        <select id="user1" name="user1" required>
          <option value="">--Select a user--</option>
          {% for user in usernames %}
            <option value="{{ user }}" {% if user == selected_user1 %}selected{% endif %}>{{ user }}</option>
          {% endfor %}
        </select>

        <label for="user2">Select second user:</label>
        <select id="user2" name="user2" required>
          <option value="">--Select a user--</option>
          {% for user in usernames %}
            {% if user != selected_user1 %}
              <option value="{{ user }}" {% if user == selected_user2 %}selected{% endif %}>{{ user }}</option>
            {% endif %}
          {% endfor %}
        </select>

        <button type="submit">Compute Similarity</button>
      </form>

      {% if similarity_score is not none %}
        <div class="score">
          Pearson similarity between {{ selected_user1 }} and {{ selected_user2 }}: {{ "%.2f"|format(similarity_score) }}<br>
          Number of common games rated: {{ n_common }}
        </div>
      {% elif selected_user1 and selected_user2 %}
        <div class="score">
          Not enough overlapping ratings to compute similarity.
        </div>
      {% endif %}
    </body>
    </html>
    """
    return render_template_string(html,
                                  usernames=usernames,
                                  similarity_score=similarity_score,
                                  n_common=n_common,
                                  selected_user1=selected_user1,
                                  selected_user2=selected_user2)

if __name__ == "__main__":
    app.run(debug=True)
