import json
import os

def generate_agent(memo):

    account_id = memo["account_id"]
    company = memo["company_name"]
    hours = memo["business_hours"]

    # Detect version
    version = memo.get("version", "v1")

    agent = {
        "agent_name": f"{company} AI Receptionist",
        "voice_style": "friendly and professional",
        "system_prompt": f"""
You are the phone receptionist for {company}.

During business hours ({hours}):
- greet the caller
- ask their name and phone number
- ask what medical assistance they need
- route emergency calls immediately

After hours:
- greet the caller
- determine if it is an emergency
- collect caller name, phone, and address
- assure them someone will follow up

Always remain polite and professional.
""",
        "key_variables": {
            "business_hours": hours,
            "company_name": company,
            "location": memo["office_address"]
        },
        "call_transfer_protocol": "transfer emergency calls immediately",
        "fallback_protocol": "collect caller details if transfer fails",
        "version": version
    }

    path = f"outputs/accounts/{account_id}/{version}"
    os.makedirs(path, exist_ok=True)

    with open(f"{path}/agent_spec.json", "w", encoding="utf-8") as f:
        json.dump(agent, f, indent=2)

    print("Agent spec created for", account_id)