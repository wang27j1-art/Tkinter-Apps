import tkinter as tk
import json
from datetime import datetime
import os
import random
import re
import unicodedata

print("Working directory:", os.getcwd())

base_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(base_dir, "attempt_log.jsonl")

cases = [
    {
        "case_id": "sore_throat_1",
        "opening_lines": [
            "Patient: Hola, me duele la garganta."
        ],
        "prompts": [
            {
                "prompt_id": "since_when",
                "patient_line": "¿Desde cuándo le duele?",
                "targets": ["time_expression_desde"]
            },
            {
                "prompt_id": "fever_or_cough",
                "patient_line": "¿Tiene fiebre o tos?",
                "targets": ["usted_register", "fiebre_gender", "medical_collocation_fiebre_alta"]
            },
        ],
        "closing_line": "Patient: Gracias, doctora."
    },
    {
        "case_id": "headache_1",
        "opening_lines": [
            "Patient: Buenas tardes. Me duele la cabeza."
        ],
        "prompts": [
            {
                "prompt_id": "pain_scale",
                "patient_line": "En una escala del 1 al 10, ¿qué tan fuerte es el dolor?",
                "targets": ["numbers_1_10", "usted_register"]
            }
        ],
        "closing_line": "Patient: Está bien, gracias."
    }
]

current_case = None
prompt_index = 0

skill_labels = {
    "usted_register": "Formal register (usted)",
    "fiebre_gender": "Gender agreement: 'una fiebre'",
    "medical_collocation_fiebre_alta": "Medical phrase: 'fiebre alta'",
    "numbers_1_10": "Pain scale number (1-10)",
    "time_expression_desde": "Time expression (desde / hace)"
}

review_drills = {
    "usted_register": [
        ("Ask formally: Do you have a pain?", "¿Tiene dolor?"),
        ("Ask formally: Since when?", "¿Desde cuándo?"),
        ("Ask formally: Do you have a cough?", "¿Tiene tos?")
        ],
    "fiebre_gender": [
        ("Correct the article: __ fiebre", "una fiebre"),
        ("Fill in: Tiene __ fiebre alta.", "una"),
        ("Choose: un/una fiebre", "una fiebre")
        ],
    "medical_collocation_fiebre_alta": [
        ("Say: high fever", "fiebre alta"),
        ("Rewrite: 'fiebre muy mal' (better medical Spanish)", "fiebre alta"),
        ("Complete: Tiene una __ alta.", "fiebre")
    ],
    "numbers_1_10": [
        ("Answer with a number 1-10: Pain is moderate.", "6"),
        ("Answer with a number 1-10: Pain is very strong.", "9"),
        ("Answer with a number 1-10: Pain is mild.", "3")
    ],
    "time_expression_desde": [
        ("Answer using 'desde': Since yesterday.", "desde ayer"),
        ("Answer using 'hace': For two days.", "hace dos dias"),
        ("Answer using 'desde': Since this morning.", "desde esta manana")
    ]
}

suggestions = {
    "numbers_1_10": ["Un 7.", "Diría que es un 6."],
    "time_expression_desde": ["Desde ayer.", "Hace dos días."],
    "usted_register": ["¿Tiene fiebre?", "¿Desde cuándo le duele?"],
    "fiebre_gender": ["Tiene una fiebre.", "Tiene fiebre alta."],
    "medical_collocation_fiebre_alta": ["Tiene fiebre alta.", "Parece fiebre alta."]
}

in_review = False
review_target = None
review_items = []
review_index = 0

case_mode = "adaptive" # "adaptive", "random", "manual"
manual_case_id = None

awaiting_retry = False
retry_prompt_snapshot = None
retry_targets = []

retry_attempts = 0
max_retries = 3 # pick any number you wnat

def choose_case():
    if case_mode == "random":
        return random.choice(cases)

    if case_mode == "manual" and manual_case_id:
        chosen = get_case_by_id(manual_case_id)
        if chosen:
            return chosen
        # fallback if id is missing
        return random.choice(cases)

    # default: adaptive
    return choose_case_based_on_gaps()

def choose_case_based_on_gaps():
    gaps = get_skill_gap_summary()

    # 30% random for variety, or if no data
    if not gaps or random.random() < 0.3:
        return random.choice(cases)

    top_skill = max(gaps.items(), key=lambda x: x[1])[0]
    candidates = [c for c in cases if any(top_skill in p["targets"] for p in c["prompts"])]

    return random.choice(candidates) if candidates else random.choice(cases)

def start_case():
    global current_case, prompt_index, current_prompt, in_review

    # Ensure we exit review mode when starting a case
    in_review = False

    prompt_index = 0
    current_case = choose_case()
    current_prompt = current_case["prompts"][prompt_index]
    
    history_box.config(state="normal")
    history_box.delete("1.0", tk.END)
    history_box.config(state="disabled")

    reason = "adaptive" if case_mode == "adaptive" else case_mode
    add_to_history(f"System: Selected case '{current_case['case_id']}' ({reason}).")
    
    for line in current_case["opening_lines"]:
        add_to_history(line)

    add_to_history("Patient: " + current_prompt["patient_line"])

def clear_retry_state():
    global awaiting_retry, retry_prompt_snapshot, retry_targets, retry_attempts
    awaiting_retry = False
    retry_prompt_snapshot = None
    retry_targets = []
    retry_attempts = 0

def submit_response():
    global review_index, current_case, prompt_index, current_prompt, in_review, review_target, review_items, awaiting_retry, retry_prompt_snapshot, retry_targets, retry_attempts
    
    response = response_box.get("1.0", tk.END).strip()
    if not response:
        return
    
    # Displays what the player typed
    add_to_history("You: " + response)

    # Review Mode Branch
    if in_review:
        if review_index >= len(review_items):
            add_to_history("System: Review Complete.")
            in_review = False
            response_box.delete("1.0", tk.END)
            return
        
        prompt_text, expected = review_items[review_index]
        is_correct = normalize_text(expected) in normalize_text(response)

        if is_correct:
            add_to_history("Feedback: Correct.")
            missed_targets = []
        else:
            add_to_history(f"Feedback: Not quite. Expected something like: {expected}")
            missed_targets = [review_target]

        # Log the review attempt
        log_attempt(
            prompt_id=f"review_{review_target}",
            patient_line=prompt_text,
            user_response=response,
            targets=[review_target],
            missed_targets=missed_targets
        )

        review_index += 1
        response_box.delete("1.0", tk.END)
        show_next_review_question()
        return
    
    # Normal Case Logic
    # If retrying, only evaluate the previously missed targets
    if awaiting_retry:
        if retry_prompt_snapshot is None:
            add_to_history("System: Retry state was missing. Resetting and moving on.")
            clear_retry_state()
            advance_case()
            return
        
        feedback_list, missed_targets = generate_feedback_and_missed(response, retry_targets)

        add_to_history(f"System: Retry attempt {retry_attempts + 1}.")
        for item in feedback_list:
            add_to_history("Feedback: " + item)

        for t in missed_targets:
            options = suggestions.get(t, [])
            if options:
                add_to_history("Suggestion: " + random.choice(options))

        # Log retry attempt distinctly
        log_attempt(
            prompt_id=retry_prompt_snapshot["prompt_id"] + f"_retry{retry_attempts + 1}",
            patient_line=retry_prompt_snapshot["patient_line"],
            user_response=response,
            targets=retry_targets,
            missed_targets=missed_targets
        )

        # If still missed, stay in retry mode (multi-retry)
        if missed_targets:
            retry_attempts += 1

            # Optional: stop after max_retries
            if retry_attempts >= max_retries:
                add_to_history("System: Max retries reached. Moving on.")
                clear_retry_state()
                response_box.delete("1.0", tk.END)
                advance_case()
                return

            add_to_history("System: Try again using the suggestions above (or click 'Skip Retry').")
            retry_targets = missed_targets[:]   # narrow to what’s still missed
            response_box.delete("1.0", tk.END)
            return

        # Success: exit retry mode and move on
        clear_retry_state()
        response_box.delete("1.0", tk.END)
        advance_case()
        return

    
    targets = current_prompt["targets"]
    feedback_list, missed_targets = generate_feedback_and_missed(response, targets)

    for item in feedback_list:
        add_to_history("Feedback: " + item)

    for t in missed_targets:
        options = suggestions.get(t, [])
        if options:
            add_to_history("Suggestion: " + random.choice(options))

    # Retry Trigger (enter retry mode)
    if missed_targets:
        log_attempt(
            prompt_id=current_prompt["prompt_id"],
            patient_line=current_prompt["patient_line"],
            user_response=response,
            targets=targets,
            missed_targets=missed_targets
        )
        
        add_to_history("System: Try again using the suggestions above (or click 'Skip Retry').")
        awaiting_retry = True
        retry_prompt_snapshot = dict(current_prompt)    # freeze the prompt once
        retry_targets = missed_targets[:]               # retry only what was missed
        retry_attempts = 0
        response_box.delete("1.0", tk.END)
        return

    log_attempt(
        prompt_id=current_prompt["prompt_id"],
        patient_line=current_prompt["patient_line"],
        user_response=response,
        targets=targets,
        missed_targets=missed_targets
    )

    print("Skill gap summary (updated):", get_skill_gap_summary())

    prompt_index += 1

    if current_case and prompt_index < len(current_case["prompts"]):
        current_prompt = current_case["prompts"][prompt_index]
        add_to_history("Patient: " + current_prompt["patient_line"])
    else:
        if current_case and "closing_line" in current_case:
            add_to_history(current_case["closing_line"])
        else:
            add_to_history("Patient: Perfecto. Terminamos por ahora.")

    response_box.delete("1.0", tk.END)

def add_to_history(text):
    history_box.config(state="normal")
    history_box.insert(tk.END, text + "\n\n")
    history_box.config(state="disabled")
    history_box.see(tk.END)

def generate_feedback_and_missed(response, targets):
    r = response.lower()
    feedback = []
    missed = []

    # Target: formal register (usted)
    if "usted_register" in targets:
        if "tienes" in r or " tú " in f" {r} " or " tu " in f" {r} ":
            feedback.append("Register: Use formal 'usted' → 'tiene', not 'tienes'.")
            missed.append("usted_register")
            
    # Target: gender agreement for 'fiebre'
    if "fiebre_gender" in targets:
        if "un fiebre" in r:
            feedback.append("Grammar: 'fiebre' is feminine → say 'una fiebre'.")
            missed.append("fiebre_gender")

    # Target: medical collocation for fever
    if "medical_collocation_fiebre_alta" in targets:
        if "fiebre" in r and ("muy mal" in r or "mal" in r):
            feedback.append("Medical Spanish: Say 'fiebre alta' (high fever) instead of 'muy mal'.")
            missed.append("medical_collocation_fiebre_alta")

    # Target: numbers 1-10 (pain scale)
    if "numbers_1_10" in targets:
        match = re.search(r"\b(10|[1-9])\b", r)
        if not match:
            feedback.append("Tip: Respond with a number from 1–10 (e.g., 'Un 7' or '7').")
            missed.append("numbers_1_10")


    if "time_expression_desde" in targets:
        rr = f" {r} "
        has_anchor = (" desde " in rr) or (" hace " in rr)
        if not has_anchor:
            feedback.append("Tip: For '¿Desde cuándo?', use 'Desde...' or 'Hace...' (e.g., 'Desde ayer' / 'Hace dos días').")
            missed.append("time_expression_desde")
            
    if not feedback:
        feedback.append("Good response for the target skills.")

    return feedback, missed

def log_attempt(prompt_id, patient_line, user_response, targets, missed_targets):
    entry = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "prompt_id": prompt_id,
        "patient_line": patient_line,
        "user_response": user_response,
        "targets": targets,
        "missed_targets": missed_targets
    }
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

def get_skill_gap_summary(log_file=log_file):
    gap_counts = {}

    try:
        with open(log_file, "r", encoding="utf-8") as f:
            for line in f:
                entry = json.loads(line)
                for target in entry["missed_targets"]:
                    gap_counts[target] = gap_counts.get(target, 0) +1
    except FileNotFoundError:
        return {}

    return gap_counts

def open_progress_window():
    gaps = get_skill_gap_summary()

    win = tk.Toplevel(root)
    win.title("Progress: Skill Gaps")
    win.resizable(False, False)

    title = tk.Label(win, text="Most Missed Targets", font=("Arial", 12, "bold"))
    title.pack(padx=15, pady=(15, 5))

    if not gaps:
        msg = tk.Label(win, text="No attempts logged yet. Submit a response first.")
        msg.pack(padx=15, pady=10)
        return

    sorted_gaps = sorted(gaps.items(), key=lambda x: x[1], reverse=True)

    N = 5
    for target, count in sorted_gaps[:N]:
        pretty = skill_labels.get(target, target.replace("_", " ").title())
        line = tk.Label(win, text=f"{pretty} - missed {count} time(s)")
        line.pack(anchor="w", padx=15)

    close_btn = tk.Button(win, text="Close", command=win.destroy)
    close_btn.pack(pady=15)

def count_attempts(log_file=log_file):
    try:
        with open(log_file, "r", encoding="utf-8") as f:
            return sum(1 for _ in f)
    except FileNotFoundError:
        return 0

def start_review_mode():
    global in_review, review_target, review_items, review_index

    gaps = get_skill_gap_summary()
    if not gaps:
        add_to_history("System: No attempts logged yet. Do a case first.")
        return

    # pick the most missed target
    review_target = max(gaps.items(), key=lambda x: x[1])[0]
    review_items = review_drills.get(review_target, [])
    review_index = 0
    in_review = True

    history_box.config(state="normal")
    history_box.delete("1.0", tk.END)
    history_box.config(state="disabled")

    add_to_history("System: Review Mode started.")
    pretty = skill_labels.get(review_target, review_target)
    add_to_history(f"System: Focusing on: {pretty}")

    if not review_items:
        add_to_history("System: No review drills found for this target yet.")
        in_review = False
        return
    
    show_next_review_question()

def show_next_review_question():
    global in_review, review_index

    if review_index >= len(review_items):
        add_to_history("System: Review complete. Great work.")
        in_review = False
        return
    
    prompt_text, _ = review_items[review_index]
    add_to_history(f"Review Q{review_index + 1}: {prompt_text}")

def get_case_by_id(case_id):
    for c in cases:
        if c["case_id"] == case_id:
            return c
    return None

def open_case_picker():
    global case_mode, manual_case_id

    win = tk.Toplevel(root)
    win.title("Choose Case Mode")
    win.resizable(False, False)

    # Local Tk variables (so UI reflects current state)
    mode_var = tk.StringVar(value=case_mode)
    case_ids = [c["case_id"] for c in cases]
    selected_case = tk.StringVar(value=manual_case_id or case_ids[0])

    tk.Label(win, text="Case selection mode:", font=("Arial", 11, "bold")).pack(padx=15, pady=(15, 5))

    tk.Radiobutton(win, text="Adaptive (based on skill gaps)", variable=mode_var, value="adaptive").pack(anchor="w", padx=15)
    tk.Radiobutton(win, text="Random", variable=mode_var, value="random").pack(anchor="w", padx=15)
    tk.Radiobutton(win, text="Manual (pick a case)", variable=mode_var, value="manual").pack(anchor="w", padx=15)

    tk.Label(win, text="Manual case:").pack(anchor="w", padx=15, pady=(10, 0))
    dropdown = tk.OptionMenu(win, selected_case, *case_ids)
    dropdown.pack(anchor="w", padx=15)

    def apply():
        global case_mode, manual_case_id
        case_mode = mode_var.get()
        manual_case_id = selected_case.get()
        add_to_history(f"System: Case mode set to '{case_mode}'.")
        if case_mode == "manual":
            add_to_history(f"System: Manual case set to '{manual_case_id}'.")
        win.destroy()

    btn_frame = tk.Frame(win)
    btn_frame.pack(pady=15)

    tk.Button(btn_frame, text="Apply", command=apply).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Cancel", command=win.destroy).pack(side="left", padx=5)

def normalize_text(s):
    s = s.strip().lower()
    s = unicodedata.normalize("NFD", s)
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
    s = re.sub(r"[^\w\s]", "", s) # remove punctuation
    s = re.sub(r"\s+", " ", s) # collapse whitespace
    return s

def advance_case():
    global prompt_index, current_prompt, current_case

    prompt_index += 1

    if current_case and prompt_index < len(current_case["prompts"]):
        current_prompt = current_case["prompts"][prompt_index]
        add_to_history("Patient: " + current_prompt["patient_line"])
    else:
        if current_case and "closing_line" in current_case:
            add_to_history(current_case["closing_line"])
        else:
            add_to_history("Patient: Perfecto. Terminamos por ahora.")

def skip_retry():
    global awaiting_retry, retry_prompt_snapshot, retry_targets, retry_attempts

    if not awaiting_retry:
        add_to_history("System: No retry pending.")
        return

    add_to_history("System: Retry skipped. Moving on.")
    clear_retry_state()
    response_box.delete("1.0", tk.END)
    advance_case()
    
root = tk.Tk()
root.title("Clinic Prototype")
root.resizable(False, False)

# Widgets
history_box = tk.Text(
    root,
    height=8,
    width=45,
    wrap="word",
    state="disabled"
)
history_box.pack(padx=20, pady=(15, 5))

response_box = tk.Text(root, height=4, width=40)
response_box.pack(padx=20, pady=5)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

start_btn = tk.Button(button_frame, text="Start Case", command=start_case)
start_btn.pack(side="left", padx=5)

review_btn = tk.Button(button_frame, text="Review", command=start_review_mode)
review_btn.pack(side="left", padx=5)

submit_btn = tk.Button(button_frame, text="Submit Response", command=submit_response)
submit_btn.pack(side="left", padx=5)

progress_btn = tk.Button(button_frame, text="Progress", command=open_progress_window)
progress_btn.pack(side="left", padx=5)

case_btn = tk.Button(button_frame, text="Case Mode", command=open_case_picker)
case_btn.pack(side="left", padx=5)

skip_btn = tk.Button(button_frame, text="Skip Retry", command=skip_retry)
skip_btn.pack(side="left", padx=5)

print("Skill gap summary:", get_skill_gap_summary())

root.mainloop()
