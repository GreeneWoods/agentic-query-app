import requests
import traceback
import json


def create_record(base_url, lead_data):
    url = f'{base_url}/api/v1/leads'

    response = requests.post(url, json=lead_data)
    response.raise_for_status()
    return response.json()


def test_main():
    base_url = 'http://127.0.0.1:8001'
    test_lead = {
        "id": 1,
        "first_name": "Avery",
        "last_name": "Nguyen",
        "email": "avery.nguyen@aurorasoft.example",
        "job_title": "VP of Marketing",
        "company": "AuroraSoft",
        "company_size": 1200,
        "industry": "SaaS",
        "location": "Austin, TX",
        "website": "https://aurorasoft.example",
        "tech_stack": [
            "HubSpot",
            "Salesforce",
            "Segment",
            "Amplitude"
        ],
        "lead_source": "Inbound - webinar",
        "last_contacted": "2025-08-30",
        "notes": "Evaluating programmatic to scale ABM; comparing StackAdapt vs. The Trade Desk. Interested in retail media pilots and privacy-safe audience building.",
        "tags": [
            "ABM",
            "privacy",
            "retail media"
        ]
    }

    record = create_record(base_url, test_lead)
    print(record)


def pipeline_main():
    base_url = 'http://localhost:8001'
    with open('leads.json', 'r') as f:
        lead_data = json.load(f)
    for lead in lead_data:
        try:
            record = create_record(base_url, lead)
            print(f"Created record for {lead['id']}")
        except Exception as e:
            print(f"Failed to create record for {json.dumps(lead)}: {e}")
            traceback.print_exc()


def main():
    # test_main()
    pipeline_main()


if __name__ == "__main__":
    main()