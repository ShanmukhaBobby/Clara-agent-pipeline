import os
from scripts.extract_memo import extract_memo
from scripts.generate_agent import generate_agent
from scripts.update_version import update_agent

demo_folder = "dataset/demo_calls"
onboard_folder = "dataset/onboarding_calls"

# -------- Pipeline A : Demo Calls --------
for file in os.listdir(demo_folder):

    if file.endswith(".txt"):

        path = os.path.join(demo_folder, file)
        account_id = file.split("_")[0]

        with open(path, "r", encoding="utf-8") as f:
            transcript = f.read()

        memo = extract_memo(transcript, account_id)
        generate_agent(memo)

print("Demo pipeline finished")


# -------- Pipeline B : Onboarding Updates --------
for file in os.listdir(onboard_folder):

    if file.endswith(".txt"):

        path = os.path.join(onboard_folder, file)
        account_id = file.split("_")[0]

        with open(path, "r", encoding="utf-8") as f:
            transcript = f.read()

        update_agent(transcript, account_id)

print("Onboarding pipeline finished")