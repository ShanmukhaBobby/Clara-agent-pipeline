import json
import os
import re
from scripts.generate_agent import generate_agent

def update_agent(transcript, account_id):

    v1_path = f"outputs/accounts/{account_id}/v1/memo.json"

    if not os.path.exists(v1_path):
        return

    with open(v1_path, encoding="utf-8") as f:
        memo = json.load(f)

    old_memo = memo.copy()

    text = transcript.lower()

    # Detect new business hours
    hours = re.search(r"\d{1,2}\s?am\s?(to|-)\s?\d{1,2}\s?pm", text)
    if hours:
        memo["business_hours"] = hours.group()

    # Detect new services
    services = ["telemedicine", "cardiology", "diabetes"]

    for s in services:
        if s in text and s not in memo["services_supported"]:
            memo["services_supported"].append(s)

    # Detect emergency routing updates
    if "triage nurse" in text:
        memo["emergency_routing_rules"] = ["transfer to triage nurse"]

    if "emergency physician" in text:
        memo["emergency_routing_rules"] = ["transfer to emergency physician"]

    # -------- Save v2 memo --------
    v2_path = f"outputs/accounts/{account_id}/v2"
    os.makedirs(v2_path, exist_ok=True)

    with open(f"{v2_path}/memo.json", "w", encoding="utf-8") as f:
        json.dump(memo, f, indent=2)

    # -------- Generate v2 agent --------
    memo["version"] = "v2"
    generate_agent(memo)

    # -------- Create changelog --------
    os.makedirs("changelog", exist_ok=True)

    changes = f"Changes for {account_id}\n\n"

    if old_memo["business_hours"] != memo["business_hours"]:
        changes += f"Business hours updated: {old_memo['business_hours']} -> {memo['business_hours']}\n"

    if old_memo["services_supported"] != memo["services_supported"]:
        changes += "Services updated\n"

    if old_memo["emergency_routing_rules"] != memo["emergency_routing_rules"]:
        changes += "Emergency routing updated\n"

    with open(f"changelog/{account_id}.md", "w", encoding="utf-8") as f:
        f.write(changes)

    print("Updated to v2 for", account_id)