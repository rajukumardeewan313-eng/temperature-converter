from flask import Flask, request, session, redirect, url_for
import json, os, random

app = Flask(__name__)
app.secret_key = "raju123"

QUESTIONS_FILE = "questions.json"

# ── 45 Questions in 3 sets of 15 ──
QUESTION_BANK = [
    # SET 1
    [
        {"question": "What is the capital of Pakistan?", "options": ["Lahore", "Karachi", "Islamabad", "Peshawar"], "answer": 2},
        {"question": "What is 5 x 6?", "options": ["25", "30", "35", "40"], "answer": 1},
        {"question": "Which planet is known as the Red Planet?", "options": ["Venus", "Saturn", "Mars", "Jupiter"], "answer": 2},
        {"question": "What is the chemical formula of water?", "options": ["O2", "CO2", "H2O", "NaCl"], "answer": 2},
        {"question": "What is Python?", "options": ["A Snake", "A Programming Language", "A Game", "An App"], "answer": 1},
        {"question": "How many teeth does an adult human have?", "options": ["28", "32", "30", "36"], "answer": 1},
        {"question": "How far is the Earth from the Sun?", "options": ["100 million km", "150 million km", "200 million km", "50 million km"], "answer": 1},
        {"question": "What is the national animal of Pakistan?", "options": ["Lion", "Markhor", "Cheetah", "Deer"], "answer": 1},
        {"question": "How many grams are in 1 kilogram?", "options": ["500", "100", "1000", "750"], "answer": 2},
        {"question": "Which is the largest ocean in the world?", "options": ["Atlantic", "Indian", "Arctic", "Pacific"], "answer": 3},
        {"question": "What is called the brain of a computer?", "options": ["RAM", "CPU", "Hard Disk", "Monitor"], "answer": 1},
        {"question": "When did Pakistan gain independence?", "options": ["1945", "1947", "1950", "1948"], "answer": 1},
        {"question": "What is the full name of Quaid-e-Azam?", "options": ["Muhammad Ali Jinnah", "Liaquat Ali Khan", "Allama Iqbal", "Ayub Khan"], "answer": 0},
        {"question": "How many days are in one week?", "options": ["5", "6", "7", "8"], "answer": 2},
        {"question": "How many colors are in a rainbow?", "options": ["5", "6", "7", "8"], "answer": 2},
    ],
    # SET 2
    [
        {"question": "Which is the highest mountain in the world?", "options": ["K2", "Mount Everest", "Nanga Parbat", "Broad Peak"], "answer": 1},
        {"question": "What does HTML stand for?", "options": ["Hyper Text Markup Language", "High Text Making Language", "Home Tool Markup Language", "Hyper Tool Making Language"], "answer": 0},
        {"question": "How many legs does a human have?", "options": ["4", "3", "2", "6"], "answer": 2},
        {"question": "How many seconds are in one minute?", "options": ["30", "100", "60", "90"], "answer": 2},
        {"question": "Which is the smallest continent?", "options": ["Europe", "Australia", "Antarctica", "South America"], "answer": 1},
        {"question": "What is the currency of Pakistan?", "options": ["Dollar", "Rupee", "Pound", "Riyal"], "answer": 1},
        {"question": "How does the Sun produce energy?", "options": ["Gas Burning", "Water Reaction", "Fire", "Nuclear Reaction"], "answer": 3},
        {"question": "Who is the founder of Microsoft?", "options": ["Steve Jobs", "Elon Musk", "Bill Gates", "Mark Zuckerberg"], "answer": 2},
        {"question": "Which country is Google from?", "options": ["UK", "China", "USA", "Germany"], "answer": 2},
        {"question": "How many minutes are in one hour?", "options": ["30", "90", "120", "60"], "answer": 3},
        {"question": "How many provinces does Pakistan have?", "options": ["3", "4", "5", "6"], "answer": 1},
        {"question": "Which province is Lahore in?", "options": ["Sindh", "KPK", "Punjab", "Balochistan"], "answer": 2},
        {"question": "What is Karachi famous for?", "options": ["Mountains", "Sea", "Desert", "Jungle"], "answer": 1},
        {"question": "What does CPU stand for?", "options": ["Central Process Unit", "Central Processing Unit", "Computer Process Unit", "Core Processing Unit"], "answer": 1},
        {"question": "What is the chemical symbol of Oxygen?", "options": ["Ox", "O2", "O", "Og"], "answer": 2},
    ],
    # SET 3
    [
        {"question": "Which is the largest lake in the world?", "options": ["Caspian Sea", "Lake Superior", "Dead Sea", "Lake Baikal"], "answer": 0},
        {"question": "How do you create a list in Python?", "options": ["{}", "[]", "()", "<>"], "answer": 1},
        {"question": "How many months are in a year?", "options": ["10", "11", "12", "13"], "answer": 2},
        {"question": "What color is blood?", "options": ["Blue", "Yellow", "Red", "Green"], "answer": 2},
        {"question": "What is Einstein's full name?", "options": ["Albert Einstein", "Alfred Einstein", "Adam Einstein", "Alex Einstein"], "answer": 0},
        {"question": "Who invented the Internet?", "options": ["Bill Gates", "Tim Berners-Lee", "Steve Jobs", "Elon Musk"], "answer": 1},
        {"question": "Which is the fastest land animal?", "options": ["Lion", "Cheetah", "Horse", "Deer"], "answer": 1},
        {"question": "What is the national flower of Pakistan?", "options": ["Rose", "Jasmine", "Tulip", "Sunflower"], "answer": 1},
        {"question": "What is 2 + 2 x 2?", "options": ["8", "6", "4", "10"], "answer": 1},
        {"question": "What is Urdu to Pakistan?", "options": ["State Language", "National Language", "Local Language", "Foreign Language"], "answer": 1},
        {"question": "What is it called when the Moon orbits the Earth?", "options": ["Revolution", "Rotation", "Orbit", "Cycle"], "answer": 0},
        {"question": "Who is the founder of Facebook?", "options": ["Bill Gates", "Jeff Bezos", "Mark Zuckerberg", "Larry Page"], "answer": 2},
        {"question": "Which is the lightest element?", "options": ["Helium", "Hydrogen", "Oxygen", "Carbon"], "answer": 1},
        {"question": "What does RAM stand for?", "options": ["Random Access Memory", "Read Access Memory", "Run All Memory", "Random All Memory"], "answer": 0},
        {"question": "Which is the largest city in Pakistan?", "options": ["Islamabad", "Lahore", "Karachi", "Peshawar"], "answer": 2},
    ],
]

def load_questions():
    if os.path.exists(QUESTIONS_FILE):
        with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return QUESTION_BANK[0]

def get_questions_for_attempt(attempt):
    set_index = (attempt - 1) % 3
    return QUESTION_BANK[set_index]

def save_questions(q):
    with open(QUESTIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(q, f, indent=2, ensure_ascii=False)

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🎯 Raju's Quiz App</title>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family:'Segoe UI',sans-serif; background:linear-gradient(135deg,#0f0c29,#302b63,#24243e); min-height:100vh; color:#fff; }}
  nav {{ background:rgba(255,255,255,0.05); padding:15px 30px; display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid rgba(255,255,255,0.1); }}
  nav .logo {{ font-size:1.4rem; font-weight:700; }}
  nav .logo span {{ color:#f7c948; }}
  nav a {{ color:rgba(255,255,255,0.7); text-decoration:none; margin-left:20px; }}
  nav a:hover {{ color:#f7c948; }}
  .container {{ max-width:700px; margin:0 auto; padding:40px 20px; }}
  .card {{ background:rgba(255,255,255,0.07); border:1px solid rgba(255,255,255,0.12); border-radius:20px; padding:40px; }}
  .btn {{ display:inline-block; padding:14px 36px; border-radius:50px; font-size:1rem; font-weight:600; cursor:pointer; border:none; text-decoration:none; transition:all 0.2s; }}
  .btn-primary {{ background:linear-gradient(135deg,#f7c948,#f0953a); color:#1a1a2e; }}
  .btn-primary:hover {{ transform:translateY(-2px); }}
  .btn-red {{ background:rgba(255,80,80,0.2); color:#ff8080; border:1px solid rgba(255,80,80,0.3); padding:8px 18px; font-size:0.85rem; border-radius:50px; cursor:pointer; }}
  input[type=text], select {{ width:100%; padding:12px 16px; background:rgba(255,255,255,0.07); border:1px solid rgba(255,255,255,0.15); border-radius:10px; color:white; font-size:1rem; margin-bottom:14px; outline:none; }}
  .opt {{ padding:16px 22px; border-radius:12px; border:2px solid rgba(255,255,255,0.12); background:rgba(255,255,255,0.04); display:flex; align-items:center; gap:16px; cursor:pointer; margin-bottom:14px; transition:all 0.2s; }}
  .opt:hover {{ border-color:rgba(247,201,72,0.5); }}
  .opt-label {{ width:36px; height:36px; border-radius:50%; background:rgba(255,255,255,0.08); display:flex; align-items:center; justify-content:center; font-weight:700; color:#f7c948; flex-shrink:0; }}
  .progress-bar {{ background:rgba(255,255,255,0.1); border-radius:50px; height:8px; margin-bottom:30px; }}
  .progress-fill {{ background:linear-gradient(90deg,#f7c948,#f0953a); height:100%; border-radius:50px; }}
  .msg {{ padding:12px 20px; border-radius:10px; margin-bottom:20px; background:rgba(255,255,255,0.08); border-left:4px solid #f7c948; }}
  .stat {{ text-align:center; }}
  .stat .num {{ font-size:2rem; color:#f7c948; font-weight:800; }}
  .stat .lbl {{ font-size:0.85rem; color:rgba(255,255,255,0.4); }}
</style>
</head>
<body>
<nav>
  <div class="logo">🎯 <span>Raju's</span> Quiz</div>
  <div><a href="/">Home</a><a href="/admin">Admin Panel</a></div>
</nav>
<div class="container">
{content}
</div>
</body>
</html>"""

# ── HOME ──
@app.route("/")
def home():
    attempt = session.get("attempt", 0)
    next_attempt = attempt + 1
    set_index = (next_attempt - 1) % 3 + 1
    content = f"""
    <div style="text-align:center; padding-top:60px;">
      <div style="font-size:5rem;">🎯</div>
      <h1 style="font-size:2.8rem; font-weight:800; margin:20px 0 10px;">Raju's <span style="color:#f7c948;">Quiz App</span></h1>
      <p style="color:rgba(255,255,255,0.5); margin-bottom:10px;">📋 15 Questions — Set {set_index} of 3</p>
      <p style="color:rgba(255,255,255,0.3); margin-bottom:40px;">Attempt #{next_attempt} — New questions every round!</p>
      <a href="/start" class="btn btn-primary" style="font-size:1.1rem;">Let's Start Quiz 🚀</a>
      <div style="display:flex; justify-content:center; gap:50px; margin-top:60px;">
        <div class="stat"><div class="num">15</div><div class="lbl">Questions</div></div>
        <div class="stat"><div class="num">3</div><div class="lbl">Sets</div></div>
        <div class="stat"><div class="num">45</div><div class="lbl">Total Questions</div></div>
      </div>
    </div>"""
    return HTML.format(content=content)

# ── START ──
@app.route("/start")
def start():
    attempt = session.get("attempt", 0) + 1
    questions = get_questions_for_attempt(attempt)
    shuffled = random.sample(questions, len(questions))
    final = []
    for q in shuffled:
        opts = q["options"][:]
        correct_text = opts[q["answer"]]
        random.shuffle(opts)
        new_answer = opts.index(correct_text)
        final.append({"question": q["question"], "options": opts, "answer": new_answer})
    session["score"] = 0
    session["current"] = 0
    session["answers"] = []
    session["questions"] = final
    session["attempt"] = attempt
    return redirect(url_for("quiz"))

# ── QUIZ ──
@app.route("/quiz", methods=["GET","POST"])
def quiz():
    questions = session.get("questions", load_questions())
    current = session.get("current", 0)

    if request.method == "POST":
        selected = request.form.get("answer")
        if selected is not None:
            selected = int(selected)
            correct = questions[current]["answer"]
            ans = session.get("answers", [])
            ans.append({"question": questions[current]["question"],
                        "selected": selected, "correct": correct,
                        "options": questions[current]["options"]})
            session["answers"] = ans
            if selected == correct:
                session["score"] = session.get("score", 0) + 1
            session["current"] = current + 1
            return redirect(url_for("quiz"))

    current = session.get("current", 0)
    if current >= len(questions):
        return redirect(url_for("result"))

    q = questions[current]
    progress = int((current / len(questions)) * 100)
    letters = ["A","B","C","D"]

    opts_html = ""
    for i, opt in enumerate(q["options"]):
        opts_html += f"""
        <label style="cursor:pointer;">
          <input type="radio" name="answer" value="{i}" required style="display:none;">
          <div class="opt">
            <div class="opt-label">{letters[i]}</div>
            {opt}
          </div>
        </label>"""

    btn_text = "Finish Quiz ✅" if current + 1 == len(questions) else "Next →"

    content = f"""
    <div style="margin-bottom:10px; display:flex; justify-content:space-between; font-size:0.9rem; color:rgba(255,255,255,0.5);">
      <span>Question {current+1} of {len(questions)}</span><span>{progress}%</span>
    </div>
    <div class="progress-bar"><div class="progress-fill" style="width:{progress}%"></div></div>
    <div class="card">
      <div style="font-size:0.85rem; color:#f7c948; margin-bottom:16px; font-weight:600; letter-spacing:1px;">QUESTION {current+1}</div>
      <h2 style="font-size:1.4rem; margin-bottom:30px; line-height:1.5;">{q["question"]}</h2>
      <form method="POST">
        {opts_html}
        <div style="margin-top:25px; text-align:right;">
          <button type="submit" class="btn btn-primary">{btn_text}</button>
        </div>
      </form>
    </div>
    <script>
      document.querySelectorAll('input[type=radio]').forEach(r => {{
        r.addEventListener('change', () => {{
          document.querySelectorAll('.opt').forEach(o => {{
            o.style.borderColor='rgba(255,255,255,0.12)';
            o.style.background='rgba(255,255,255,0.04)';
          }});
          r.parentElement.querySelector('.opt').style.borderColor='#f7c948';
          r.parentElement.querySelector('.opt').style.background='rgba(247,201,72,0.12)';
        }});
      }});
    </script>"""
    return HTML.format(content=content)

# ── RESULT ──
@app.route("/result")
def result():
    score = session.get("score", 0)
    answers = session.get("answers", [])
    total = len(answers)
    pct = int((score/total)*100) if total else 0

    if pct == 100: grade = "🏆 Perfect!"
    elif pct >= 80: grade = "🌟 Excellent!"
    elif pct >= 60: grade = "👍 Good Job!"
    elif pct >= 40: grade = "📚 Keep Studying!"
    else: grade = "💪 Practice More!"

    reviews = ""
    for i, a in enumerate(answers):
        ok = a["selected"] == a["correct"]
        reviews += f"""
        <div style="background:rgba(255,255,255,0.05); border-radius:14px; padding:18px; margin-bottom:12px;
             border-left:4px solid {'#4caf50' if ok else '#f44336'};">
          <div style="font-weight:600; margin-bottom:8px;">{i+1}. {a['question']}</div>
          <div style="font-size:0.9rem; color:rgba(255,255,255,0.5);">
            Your Answer: <span style="color:{'#4caf50' if ok else '#f44336'}; font-weight:600;">{a['options'][a['selected']]} {'✅' if ok else '❌'}</span>
          </div>
          {'<div style="font-size:0.9rem;color:rgba(255,255,255,0.5);margin-top:4px;">Correct Answer: <span style="color:#4caf50;font-weight:600;">'+a["options"][a["correct"]]+'</span></div>' if not ok else ''}
        </div>"""

    content = f"""
    <div class="card" style="text-align:center; margin-bottom:30px;">
      <div style="font-size:3.5rem; margin-bottom:10px;">{grade.split()[0]}</div>
      <h1 style="font-size:2rem; margin-bottom:8px;">Quiz Complete!</h1>
      <div style="font-size:4rem; font-weight:900; color:#f7c948; margin:20px 0;">{score}/{total}</div>
      <div style="color:rgba(255,255,255,0.5); margin-bottom:10px;">{pct}% Correct — {grade}</div>
      <div style="display:flex; gap:16px; justify-content:center; margin-top:25px; flex-wrap:wrap;">
        <a href="/start" class="btn btn-primary">🔄 Play Again</a>
        <a href="/" class="btn" style="background:rgba(255,255,255,0.1);color:white;">🏠 Home</a>
      </div>
    </div>
    <h3 style="margin-bottom:16px; color:rgba(255,255,255,0.5);">📋 Answer Review</h3>
    {reviews}"""
    return HTML.format(content=content)

# ── ADMIN ──
@app.route("/admin", methods=["GET","POST"])
def admin():
    questions = load_questions()
    msg = ""

    if request.method == "POST":
        action = request.form.get("action")
        if action == "add":
            qt = request.form.get("question","").strip()
            opts = [request.form.get(f"opt{i}","").strip() for i in range(4)]
            ans = int(request.form.get("answer", 0))
            if qt and all(opts):
                questions.append({"question": qt, "options": opts, "answer": ans})
                save_questions(questions)
                msg = "✅ Question added successfully!"
            else:
                msg = "⚠️ Please fill in all fields!"
        elif action == "delete":
            idx = int(request.form.get("index"))
            if 0 <= idx < len(questions):
                questions.pop(idx)
                save_questions(questions)
                msg = "🗑️ Question deleted!"

    letters = ["A","B","C","D"]
    q_list = ""
    for i, q in enumerate(questions):
        q_list += f"""
        <div style="background:rgba(255,255,255,0.05); border-radius:14px; padding:18px 22px; margin-bottom:12px;
             border:1px solid rgba(255,255,255,0.08); display:flex; justify-content:space-between; align-items:center; gap:16px;">
          <div>
            <div style="font-weight:600; margin-bottom:6px;">{i+1}. {q['question']}</div>
            <div style="font-size:0.85rem; color:rgba(255,255,255,0.4);">✅ Correct: <span style="color:#f7c948;">{q['options'][q['answer']]}</span></div>
          </div>
          <form method="POST" onsubmit="return confirm('Are you sure you want to delete this question?')">
            <input type="hidden" name="action" value="delete">
            <input type="hidden" name="index" value="{i}">
            <button type="submit" class="btn-red">🗑️ Delete</button>
          </form>
        </div>"""

    opt_selects = "".join([f'<option value="{i}">{letters[i]}</option>' for i in range(4)])

    content = f"""
    <h1 style="font-size:1.8rem; font-weight:800; margin-bottom:8px;">⚙️ Admin Panel</h1>
    <p style="color:rgba(255,255,255,0.4); margin-bottom:30px;">Add or delete quiz questions</p>
    {f'<div class="msg">{msg}</div>' if msg else ''}
    <div class="card" style="margin-bottom:30px;">
      <h2 style="font-size:1.2rem; margin-bottom:25px; color:#f7c948;">➕ Add New Question</h2>
      <form method="POST">
        <input type="hidden" name="action" value="add">
        <input type="text" name="question" placeholder="Type your question here..." required>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:14px;">
          <input type="text" name="opt0" placeholder="Option A" required>
          <input type="text" name="opt1" placeholder="Option B" required>
          <input type="text" name="opt2" placeholder="Option C" required>
          <input type="text" name="opt3" placeholder="Option D" required>
        </div>
        <div style="margin-bottom:20px;">
          <label style="color:rgba(255,255,255,0.6); font-size:0.9rem; display:block; margin-bottom:8px;">Correct Answer:</label>
          <select name="answer" style="width:auto;">{opt_selects}</select>
        </div>
        <button type="submit" class="btn btn-primary">➕ Add Question</button>
      </form>
    </div>
    <h2 style="font-size:1.2rem; margin-bottom:16px;">📋 All Questions ({len(questions)})</h2>
    {q_list if q_list else '<div style="text-align:center;padding:30px;color:rgba(255,255,255,0.3);">No questions yet — add one above!</div>'}"""

    return HTML.format(content=content)

if __name__ == "__main__":
    app.run(debug=True)
