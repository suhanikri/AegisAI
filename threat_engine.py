from textblob import TextBlob

fear_words = ["urgent", "immediately", "last warning", "suspended", "legal action", "unauthorized"]
authority_words = ["bank", "government", "rbi", "police", "account", "court"]
money_words = ["transfer", "otp", "payment", "refund", "bitcoin", "charge"]
romance_words = ["love", "trust me", "only you", "secret"]

def calculate_scores(text):
    text_lower = text.lower()

    fear_count = sum(text_lower.count(word) for word in fear_words)
    authority_count = sum(text_lower.count(word) for word in authority_words)
    money_count = sum(text_lower.count(word) for word in money_words)
    romance_count = sum(text_lower.count(word) for word in romance_words)

    sentiment = TextBlob(text).sentiment.polarity

    eci = (fear_count * 2) + (authority_count * 1.5) + (money_count * 2) + (romance_count * 1.5)

    if sentiment < -0.2:
        eci += 2

    eci_score = min(eci * 10, 100)
    fraud_score = min((fear_count + authority_count + money_count + romance_count) * 20, 100)

    final_risk = min((eci_score * 0.6 + fraud_score * 0.4), 100)

    if final_risk > 70:
        threat_level = "HIGH"
    elif final_risk > 30:
        threat_level = "MEDIUM"
    else:
        threat_level = "LOW"

    # Threat Category Logic
    if authority_count and money_count:
        threat_category = "Authority-Based Financial Fraud"
    elif fear_count and authority_count:
        threat_category = "Urgency + Authority Impersonation"
    elif romance_count:
        threat_category = "Romance Manipulation Pattern"
    elif money_count:
        threat_category = "Financial Manipulation Pattern"
    else:
        threat_category = "General Suspicion"

    explanation = []
    if fear_count:
        explanation.append("Fear/Urgency trigger detected")
    if authority_count:
        explanation.append("Authority/Institution reference detected")
    if money_count:
        explanation.append("Financial manipulation indicators detected")
    if romance_count:
        explanation.append("Emotional bonding manipulation detected")
    if sentiment < -0.2:
        explanation.append("Negative sentiment pattern detected")

    return {
        "risk_score": round(final_risk, 2),
        "emotional_coercion_index": round(eci_score, 2),
        "threat_level": threat_level,
        "threat_category": threat_category,
        "explanation": explanation
    }