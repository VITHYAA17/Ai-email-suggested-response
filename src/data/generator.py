"""
Synthetic Dataset Generator for AI Email Suggested-Response System.
Allows generating, augmenting, and scaling realistic customer support email pairs.
"""

import random
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any

from src.config import SUPPORT_CATEGORIES

CUSTOMER_NAMES = [
    "Sarah Jenkins", "Marcus Vance", "Elena Rostova", "Alex Chen",
    "Priya Patel", "Henrik Lindqvist", "Chloe Bennett", "David Ross",
    "Teresa Mendoza", "Brian Cox", "Danica Patrick", "Timothy Chen"
]

COMPANY_NAMES = [
    "ApexFin", "CloudFlow GmbH", "Nexus Logistics", "BioHealth Labs",
    "StripeLine Media", "Vanguard Retail", "Quantum Software", "Acme Corp"
]

CATEGORY_TEMPLATES = {
    "billing_and_invoicing": [
        {
            "subject": "Question regarding unexpected invoice charge for {product}",
            "body": "Hi Support team,\n\nWe noticed a charge of ${amount} on our credit card for {company}. Can you explain what this charge corresponds to and send us the updated invoice PDF?\n\nThanks,\n{name}",
            "intent": "Inquiring about unexpected billing charge and requesting invoice PDF",
            "reply": "Hi {name},\n\nThank you for reaching out! I checked your account for {company} and confirmed the charge of ${amount} was for your monthly seat renewals. I have re-sent the itemized PDF receipt to your billing address. Please let us know if you have any questions!\n\nBest regards,\nBilling Support Team",
            "key_facts": ["Charge explained: monthly seat renewals", "Itemized PDF receipt re-sent"],
            "policy": "Billing Policy §2.1"
        },
        {
            "subject": "Cancel subscription before next cycle for {company}",
            "body": "Hello, please cancel our subscription for {company} starting immediately. We will not be renewing for next month. Please confirm no further charges will occur.\n\nRegards,\n{name}",
            "intent": "Customer requesting subscription cancellation and confirmation of no future charges",
            "reply": "Hi {name},\n\nI have processed the cancellation for {company} effective at the conclusion of your current billing period. You will retain full access until then, and no future charges will be processed. Thank you for your past business with us!\n\nBest regards,\nCustomer Success Team",
            "key_facts": ["Cancellation processed effective end of cycle", "Access retained until expiration", "No further charges"],
            "policy": "Billing Policy §3.1"
        }
    ],
    "technical_bugs": [
        {
            "subject": "Shared mailbox notifications not arriving on Chrome for {company}",
            "body": "Hi, our agents at {company} are not getting desktop popup notifications when new tickets are assigned to them in Chrome. We checked browser settings and notifications are allowed. Can you help?\n\n- {name}",
            "intent": "Desktop notifications failing to display in Chrome browser",
            "reply": "Hi {name},\n\nThank you for reporting this. In Chrome 120+, desktop notifications require the tab to retain background permissions or use the desktop companion app. Please ensure 'Background Sync' is allowed under chrome://settings/content/notifications. We also recommend refreshing the tab once. Let us know if notifications resume!\n\nBest regards,\nTechnical Support Team",
            "key_facts": ["Check background sync under chrome://settings/content/notifications", "Hard refresh tab"],
            "policy": "Technical Support §4.2"
        }
    ],
    "account_access": [
        {
            "subject": "Password reset token expired for {company}",
            "body": "Hello, I requested a password reset link for our workspace at {company} but when I clicked it, it said 'Token expired'. Can you send me a fresh link?\n\nThanks,\n{name}",
            "intent": "Expired password reset link; requesting fresh token",
            "reply": "Hi {name},\n\nFor security reasons, our password reset links expire after 15 minutes. I have triggered a fresh secure reset link to your registered email address. Please click it within 15 minutes to establish your new password.\n\nBest regards,\nSecurity Team",
            "key_facts": ["Reset links expire in 15 minutes for security", "Fresh link dispatched"],
            "policy": "Security Policy §1.4"
        }
    ],
    "product_how_to": [
        {
            "subject": "How to set up automated email tags based on keywords for {company}",
            "body": "Hi, we want incoming emails containing the word 'Urgent' or 'Billing' to automatically get tagged in our shared mailbox. How do we configure this rule?\n\n- {name}",
            "intent": "Setting up automated email tagging based on keyword rules",
            "reply": "Hi {name},\n\nSetting up automated keyword tagging is easy! Go to Settings > Workflows & Automation > Create Rule. Set condition: 'Subject or Body contains keyword' and Action: 'Add Tag'. Click Save & Activate, and new incoming emails will be tagged automatically!\n\nBest regards,\nCustomer Support Team",
            "key_facts": ["Settings > Workflows & Automation > Create Rule", "Condition: contains keyword", "Action: Add Tag"],
            "policy": "Product Feature Guidance"
        }
    ]
}


def generate_synthetic_tickets(count: int = 10, seed: int = 42) -> List[Dict[str, Any]]:
    """Generate synthetic customer support email pairs with realistic variations."""
    random.seed(seed)
    results = []
    
    categories = list(CATEGORY_TEMPLATES.keys())
    
    for i in range(count):
        cat = random.choice(categories)
        template = random.choice(CATEGORY_TEMPLATES[cat])
        name = random.choice(CUSTOMER_NAMES)
        company = random.choice(COMPANY_NAMES)
        product = random.choice(["Shared Inbox Pro", "Enterprise Mailbox", "Helpdesk Suite"])
        amount = random.choice([75, 150, 250, 500, 1200])
        
        subject = template["subject"].format(name=name, company=company, product=product, amount=amount)
        body = template["body"].format(name=name, company=company, product=product, amount=amount)
        reply = template["reply"].format(name=name, company=company, product=product, amount=amount)
        
        ticket = {
            "id": f"SYN-{1000 + i}",
            "category": cat,
            "subject": subject,
            "customer_email": body,
            "customer_sentiment": random.choice(["neutral", "polite", "urgent", "confused"]),
            "intent": template["intent"],
            "ground_truth_reply": reply,
            "key_facts": template["key_facts"],
            "prohibited_actions": ["Do not make unauthorized commitments", "Do not ignore customer tone"],
            "policy_applied": template["policy"]
        }
        results.append(ticket)
        
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate synthetic email dataset")
    parser.add_argument("--count", type=int, default=10, help="Number of tickets to generate")
    parser.add_argument("--output", type=str, default="data/synthetic_sample.json", help="Output file path")
    args = parser.parse_args()
    
    tickets = generate_synthetic_tickets(count=args.count)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(tickets, f, indent=2)
    print(f"Generated {len(tickets)} synthetic tickets at {out_path}")
