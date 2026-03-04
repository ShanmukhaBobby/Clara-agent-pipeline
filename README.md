# Clara AI Automation Pipeline

## Overview

This project builds an automation pipeline that converts demo call transcripts into AI voice agent configurations and updates them after onboarding calls.

The system processes transcripts, extracts structured business information, generates an agent configuration, and stores versioned outputs.

The pipeline runs locally using rule-based extraction and zero-cost tools.

---

## Goal

The goal of the system is to automate the following workflow:

Demo Call → Extract Business Information → Generate Agent Configuration

Later when onboarding updates arrive:

Onboarding Call → Update Configuration → Generate Version 2

---

## Pipeline

Two pipelines are implemented.

### Pipeline A – Demo Call

Input:
Demo call transcript

Process:
Transcript  
→ Information extraction  
→ Create account memo  
→ Generate agent configuration  

Output:

outputs/accounts/<account_id>/v1

Files generated:

memo.json  
agent_spec.json

---

### Pipeline B – Onboarding Update

Input:
Onboarding call transcript

Process:
Load existing v1 memo  
→ Detect updates  
→ Update memo data  
→ Generate new agent configuration  

Output:

outputs/accounts/<account_id>/v2

Files generated:

memo.json  
agent_spec.json  

A changelog file is also created.

---

## Folder Structure


clara-agent-pipeline

dataset
demo_calls
onboarding_calls

outputs
accounts
account1
v1
v2

scripts
extract_memo.py
generate_agent.py
update_version.py

changelog

workflows
n8n_workflow.json

run_pipeline.py
README.md


---

## Dataset

The dataset contains transcripts.

Demo transcripts:


dataset/demo_calls


Onboarding transcripts:


dataset/onboarding_calls


Each account has two files:


account1_demo.txt
account1_onboarding.txt


Total dataset:

5 demo transcripts  
5 onboarding transcripts

---

## How to Run

Run the pipeline from the project root folder.


python run_pipeline.py


The pipeline will automatically process all transcripts.

---

## Output

For each account the system generates:


outputs/accounts/<account_id>/v1


Files:


memo.json
agent_spec.json


After onboarding updates:


outputs/accounts/<account_id>/v2


Files:


memo.json
agent_spec.json


Changelog files are stored in:


changelog/


---

## Extraction Method

The system uses rule-based extraction to identify:

business hours  
location  
services  
emergency conditions  
routing instructions  

Regular expressions and sentence pattern detection are used to extract information from transcripts.

This approach satisfies the zero-cost constraint.

---

## Automation Workflow

A simple orchestration workflow is included.

File:


workflows/n8n_workflow.json


The workflow triggers the pipeline execution.

---

## Limitations

Rule-based extraction may not capture every variation of natural language.

For production systems, a local or hosted language model could improve extraction accuracy.

---

## Possible Improvements

Improve entity extraction for company names.  
Use NLP models for better semantic extraction.  
Add a UI dashboard to visualize accounts and version changes.  
Integrate directly with Retell APIs.