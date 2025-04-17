def ask_questions():
    answers = {}

    print("== Personal Financial Questionnaire ==")

    answers["marital_status"] = input("Are you married, single, divorced, or widowed? ").lower()
    answers["dependents"] = int(input("How many children or dependents do you have? "))
    answers["retirement_age"] = int(input("At what age do you plan to retire? "))
    answers["already_saving"] = input("Have you started saving for retirement? (yes/no) ").lower()
    answers["risk_comfort"] = input("Are you comfortable with market ups and downs? (yes/no) ").lower()
    answers["debt_level"] = input("Do you have significant debt? (yes/no) ").lower()
    answers["sector_prefs"] = input("Preferred sectors (comma-separated, e.g., tech,healthcare,utilities): ").lower().split(",")

    return answers

def calculate_risk_score(answers):
    score = 5  # start from neutral

    if answers["marital_status"] == "single":
        score += 1
    elif answers["marital_status"] == "married":
        score -= 1

    if answers["dependents"] > 0:
        score -= 1

    if answers["retirement_age"] > 60:
        score += 1

    if answers["already_saving"] == "no":
        score -= 1

    if answers["risk_comfort"] == "yes":
        score += 2
    else:
        score -= 1

    if answers["debt_level"] == "yes":
        score -= 1
    else:
        score += 1

    return max(1, min(10, score))
