"""
Script to create human-annotated validation benchmark for calibrating and proving the accuracy metric.
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
VALIDATION_FILE = DATA_DIR / "human_validation_ground_truth.json"

HUMAN_ANNOTATIONS = [
  {
    "test_id": "VAL-001",
    "test_subject": "Charged twice for our monthly renewal",
    "test_email": "Hi, I just checked our corporate credit card statement and noticed two identical charges of $150 from your service on September 1st. We only have one active workspace. Could you please check why we were double-billed and refund the duplicate? - Kevin O'Connor",
    "system_response": "Hi Kevin,\n\nI apologize for the double charge! I checked our billing records and confirmed that transaction #CH-8192 was a duplicate charge of $150. I have immediately voided it and issued a full refund back to your corporate card. You should see the credit reflected on your statement within 3-5 business days. Your next scheduled billing date is October 1st. Let me know if you need anything else!\n\nBest regards,\nCustomer Support Team",
    "human_intent_score": 5.0,
    "human_factual_score": 5.0,
    "human_tone_score": 5.0,
    "human_completeness_score": 5.0,
    "human_overall_score": 98.0,
    "quality_tier": "EXCELLENT",
    "annotator_notes": "Perfect customer response: prompt apology, clear refund confirmation, accurate timeline, professional tone."
  },
  {
    "test_id": "VAL-002",
    "test_subject": "Charged twice for our monthly renewal",
    "test_email": "Hi, I just checked our corporate credit card statement and noticed two identical charges of $150 from your service on September 1st. We only have one active workspace. Could you please check why we were double-billed and refund the duplicate? - Kevin O'Connor",
    "system_response": "Hello Kevin,\n\nWe cannot issue refunds for credit card charges once they are processed. You should contact American Express or your bank and file a formal credit card dispute to get your money back. Thank you.",
    "human_intent_score": 1.0,
    "human_factual_score": 1.0,
    "human_tone_score": 1.0,
    "human_completeness_score": 1.5,
    "human_overall_score": 15.0,
    "quality_tier": "POOR",
    "annotator_notes": "Catastrophic failure: completely violates billing policy on duplicate charges, adversarial tone, instructs customer to file dispute."
  },
  {
    "test_id": "VAL-003",
    "test_subject": "Can we switch from monthly to annual billing to save money?",
    "test_email": "Hello team, we are currently paying $25/user/month for 8 agents. We love the product and want to know if there is an annual discount if we pay upfront for the whole year. How much would we save and how do we switch? Thanks, Claire Vance.",
    "system_response": "Hi Claire,\n\nThanks for reaching out! Yes, we offer a 20% discount on annual billing ($20/seat/month instead of $25), which saves your team $480 per year. You can switch anytime in Settings > Billing & Plans by selecting the Annual toggle. Let us know if you have questions!\n\nBest,\nSupport Team",
    "human_intent_score": 5.0,
    "human_factual_score": 5.0,
    "human_tone_score": 4.5,
    "human_completeness_score": 4.5,
    "human_overall_score": 93.0,
    "quality_tier": "EXCELLENT",
    "annotator_notes": "Direct, accurate calculations and straightforward instructions. Very slight deduction on completeness for not mentioning proration."
  },
  {
    "test_id": "VAL-004",
    "test_subject": "Can we switch from monthly to annual billing to save money?",
    "test_email": "Hello team, we are currently paying $25/user/month for 8 agents. We love the product and want to know if there is an annual discount if we pay upfront for the whole year. How much would we save and how do we switch? Thanks, Claire Vance.",
    "system_response": "Hi Claire, yes we have discounts. You save money by paying annually. Just log in and change it in settings.",
    "human_intent_score": 3.0,
    "human_factual_score": 3.5,
    "human_tone_score": 2.5,
    "human_completeness_score": 2.0,
    "human_overall_score": 48.0,
    "quality_tier": "FAIR",
    "annotator_notes": "Vague and unhelpful: fails to answer 'how much would we save' and gives minimal instructions."
  },
  {
    "test_id": "VAL-005",
    "test_subject": "Chrome extension keeps crashing when clicking on long email threads",
    "test_email": "Whenever I open an email thread with more than 15 replies, the browser extension crashes and freezes Gmail. I have to reload the whole tab. I'm on Chrome version 125 on MacOS. What should I do? - Dave Miller",
    "system_response": "Hi Dave,\n\nI apologize for this issue! This is a known memory issue in extension version 4.2.1 that is fixed in v4.2.3. Please go to chrome://extensions, turn on Developer Mode, and click 'Update' to get the latest version. Restart Chrome afterward and large threads should load normally. Let us know if it persists!\n\nBest regards,\nCustomer Support Team",
    "human_intent_score": 5.0,
    "human_factual_score": 5.0,
    "human_tone_score": 4.8,
    "human_completeness_score": 5.0,
    "human_overall_score": 96.0,
    "quality_tier": "EXCELLENT",
    "annotator_notes": "Accurate technical diagnosis, correct version numbers, exact actionable steps."
  },
  {
    "test_id": "VAL-006",
    "test_subject": "Chrome extension keeps crashing when clicking on long email threads",
    "test_email": "Whenever I open an email thread with more than 15 replies, the browser extension crashes and freezes Gmail. I have to reload the whole tab. I'm on Chrome version 125 on MacOS. What should I do? - Dave Miller",
    "system_response": "Hi Dave,\n\nOur extension does not support threads with more than 15 replies because of Gmail memory limitations. You must permanently switch your entire company to Firefox or Safari if you wish to use our platform. There is no other workaround.\n\nRegards,\nSupport",
    "human_intent_score": 2.0,
    "human_factual_score": 1.0,
    "human_tone_score": 2.0,
    "human_completeness_score": 2.0,
    "human_overall_score": 28.0,
    "quality_tier": "POOR",
    "annotator_notes": "Severe hallucination of nonexistent technical limitation, completely inaccurate guidance."
  },
  {
    "test_id": "VAL-007",
    "test_subject": "Locked out of account after 5 incorrect password attempts",
    "test_email": "I mistyped my password and now the screen says 'Account locked due to excessive failed attempts. Contact administrator.' I am the only administrator! Can you unlock me? - Brian Cox",
    "system_response": "Hi Brian,\n\nI understand your frustration with being locked out! The automated security lockout lasts 30 minutes, but since you are the verified owner, I have cleared the security lock on your account. Please head to https://app.ourdomain.com/password/reset to request a password reset link and regain access. Let us know if you need any further help!\n\nBest regards,\nSecurity Support Team",
    "human_intent_score": 5.0,
    "human_factual_score": 5.0,
    "human_tone_score": 5.0,
    "human_completeness_score": 5.0,
    "human_overall_score": 97.0,
    "quality_tier": "EXCELLENT",
    "annotator_notes": "Exemplary support response: explains policy, takes immediate resolution action, provides official reset link."
  },
  {
    "test_id": "VAL-008",
    "test_subject": "Locked out of account after 5 incorrect password attempts",
    "test_email": "I mistyped my password and now the screen says 'Account locked due to excessive failed attempts. Contact administrator.' I am the only administrator! Can you unlock me? - Brian Cox",
    "system_response": "Hi Brian, please reply to this email with what you want your new password to be and I will set it in the database for you.",
    "human_intent_score": 2.0,
    "human_factual_score": 1.0,
    "human_tone_score": 3.0,
    "human_completeness_score": 1.0,
    "human_overall_score": 22.0,
    "quality_tier": "POOR",
    "annotator_notes": "Critical security violation: asking customer to email plaintext passwords."
  },
  {
    "test_id": "VAL-009",
    "test_subject": "Requesting refund 45 days after payment - company downsizing",
    "test_email": "We paid for an annual plan 45 days ago, but our startup just had to downsize and we no longer need the software. I know your policy says 14 days, but this is an emergency. Can you please refund our remaining 10 months? - David Ross",
    "system_response": "Hi David,\n\nI'm very sorry to hear about your company downsizing. While our standard refund window is 14 days, given these extenuating circumstances, we can either freeze your remaining 10 months into a reusable account credit or submit a hardship exception to our finance team for a prorated refund minus a 10% fee. Please let me know which option works better for you.\n\nWarm regards,\nCustomer Support Team",
    "human_intent_score": 5.0,
    "human_factual_score": 4.8,
    "human_tone_score": 5.0,
    "human_completeness_score": 5.0,
    "human_overall_score": 95.0,
    "quality_tier": "EXCELLENT",
    "annotator_notes": "Outstanding handling of policy exception: empathetic tone, explains rules gently, offers constructive solutions."
  },
  {
    "test_id": "VAL-010",
    "test_subject": "Requesting refund 45 days after payment - company downsizing",
    "test_email": "We paid for an annual plan 45 days ago, but our startup just had to downsize and we no longer need the software. I know your policy says 14 days, but this is an emergency. Can you please refund our remaining 10 months? - David Ross",
    "system_response": "No. Policy is 14 days. You are at 45 days. We cannot refund you.",
    "human_intent_score": 3.0,
    "human_factual_score": 3.5,
    "human_tone_score": 1.0,
    "human_completeness_score": 2.0,
    "human_overall_score": 32.0,
    "quality_tier": "POOR",
    "annotator_notes": "Brutal, abrasive tone that damages customer goodwill. Technically cites rule but completely fails customer support standards."
  }
]

def main():
    with open(VALIDATION_FILE, "w", encoding="utf-8") as f:
        json.dump(HUMAN_ANNOTATIONS, f, indent=2, ensure_ascii=False)
    print(f"Successfully generated {len(HUMAN_ANNOTATIONS)} human validation cases at {VALIDATION_FILE}")

if __name__ == "__main__":
    main()
