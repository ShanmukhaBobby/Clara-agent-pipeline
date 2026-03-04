import os
import json
import re

def extract_memo(text, account_id):

    memo = {
        "account_id": account_id,
        "company_name": "",
        "business_hours": "",
        "office_address": "",
        "services_supported": [],
        "emergency_definition": [],
        "emergency_routing_rules": [],
        "non_emergency_routing_rules": [],
        "call_transfer_rules": [],
        "integration_constraints": "",
        "after_hours_flow_summary": "",
        "office_hours_flow_summary": "",
        "questions_or_unknowns": [],
        "notes": "generated from demo call"
    }

    text_lower = text.lower()

    # -------- Company Name Extraction --------
    company_match = re.search(r"from\s(.+?)\s(located|in)", text_lower)

    if company_match:
        memo["company_name"] = company_match.group(1).title()
    else:
        first_line = text.split("\n")[0]
        memo["company_name"] = first_line.strip()

    # -------- Business Hours Extraction --------
    hours_pattern = r"\d{1,2}\s?(am|pm)\s?(to|-)\s?\d{1,2}\s?(am|pm)"
    hours_match = re.search(hours_pattern, text_lower)

    if hours_match:
        memo["business_hours"] = hours_match.group()

    # -------- Location Extraction --------
    location_match = re.search(r"located in\s([a-zA-Z\s]+)", text_lower)

    if location_match:
        memo["office_address"] = location_match.group(1).title()
    else:
        location_match = re.search(r"in\s([a-zA-Z\s]+)", text_lower)
        if location_match:
            memo["office_address"] = location_match.group(1).title()

    # -------- Service Extraction --------
    service_patterns = [
        r"services include(.*)",
        r"we provide(.*)",
        r"we offer(.*)"
    ]

    for pattern in service_patterns:

        match = re.search(pattern, text_lower)

        if match:
            services = match.group(1)
            services = services.replace(".", "")
            services_list = services.split(",")

            for service in services_list:

                clean_service = service.strip()

                if clean_service and clean_service not in memo["services_supported"]:
                    memo["services_supported"].append(clean_service)

    # -------- Emergency Definition Extraction --------
    emergency_sentences = re.findall(r"(.*emergency.*)", text_lower)

    for sentence in emergency_sentences:

        sentence = sentence.strip()

        if sentence and sentence not in memo["emergency_definition"]:
            memo["emergency_definition"].append(sentence)

    # -------- Routing Rules Extraction --------
    routing_patterns = [
        r"transfer.*",
        r"route.*",
        r"connect.*"
    ]

    for pattern in routing_patterns:

        matches = re.findall(pattern, text_lower)

        for rule in matches:

            rule = rule.strip()

            if rule and rule not in memo["emergency_routing_rules"]:
                memo["emergency_routing_rules"].append(rule)

    # -------- Save Memo --------
    output_path = f"outputs/accounts/{account_id}/v1"
    os.makedirs(output_path, exist_ok=True)

    with open(f"{output_path}/memo.json", "w", encoding="utf-8") as f:
        json.dump(memo, f, indent=2)

    print("Created memo for", account_id)

    return memo