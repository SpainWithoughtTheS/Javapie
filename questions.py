def calculate_risk_score(answers):
    score = 5  # Start neutral

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
        if answers["debt_amount"] > 50000:
            score -= 2
        elif answers["debt_amount"] > 20000:
            score -= 1
        else:
            score -= 0.5
    else:
        score += 1

    return max(1, min(10, round(score)))
