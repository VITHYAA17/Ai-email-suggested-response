"""
Script to generate the canonical 20-ticket Evaluation Benchmark for accuracy measurement.
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
EVAL_FILE = DATA_DIR / "eval_benchmark.json"

EVAL_TEST_CASES = [
  {
    "id": "EVAL-001",
    "category": "billing_and_invoicing",
    "subject": "Charged twice for our monthly renewal",
    "customer_email": "Hi, I just checked our corporate credit card statement and noticed two identical charges of $150 from your service on September 1st. We only have one active workspace. Could you please check why we were double-billed and refund the duplicate? - Kevin O'Connor",
    "customer_sentiment": "confused",
    "intent": "Resolve duplicate charge on monthly renewal and refund second transaction",
    "reference_reply": "Hi Kevin,\n\nThank you for reaching out, and I apologize for the duplicate charge on your corporate card.\n\nI investigated your billing ledger and found that an automated retry coincided with a bank gateway confirmation, resulting in two charges of $150 (#CH-8191 and #CH-8192).\n\nI have immediately voided the duplicate transaction (#CH-8192) and issued a full refund of $150 back to your card. Depending on your financial institution, this credit will reflect on your statement within 3 to 5 business days.\n\nYour next regular billing date remains scheduled for October 1st. Please let me know if you need an updated receipt for your accounting records!\n\nBest regards,\nCustomer Support Team",
    "expected_facts": [
      "Acknowledge the duplicate charge of $150",
      "Confirm immediate refund processed for duplicate transaction",
      "Refund timeline: 3 to 5 business days",
      "State next normal billing date or offer updated receipt"
    ],
    "prohibited_promises": [
      "Do not refuse refund for duplicate charges",
      "Do not ask user to file a credit card dispute or chargeback"
    ],
    "difficulty": "standard"
  },
  {
    "id": "EVAL-002",
    "category": "billing_and_invoicing",
    "subject": "Can we switch from monthly to annual billing to save money?",
    "customer_email": "Hello team, we are currently paying $25/user/month for 8 agents. We love the product and want to know if there is an annual discount if we pay upfront for the whole year. How much would we save and how do we switch? Thanks, Claire Vance.",
    "customer_sentiment": "polite",
    "intent": "Inquiring about annual prepayment discount and instructions to switch billing cadence",
    "reference_reply": "Hi Claire,\n\nWe're so thrilled to hear your team is loving the product!\n\nYes! We offer a 20% discount when you switch from monthly to annual billing. Here is how the savings look for your 8 seats:\n- Monthly billing: $25/seat/month ($200/month = $2,400/year)\n- Annual billing: $20/seat/month ($160/month billed as $1,920 annually)\n- Total annual savings: $480/year (2 months free!)\n\nTo switch to annual billing:\n1. Go to Settings > Billing & Plans as an Account Admin.\n2. Click 'Manage Subscription' and toggle the billing frequency to 'Annual'.\n3. Click 'Confirm Plan Change'.\n\nYour account will be prorated for any remaining days on your current monthly cycle. Let me know if you would like me to switch this over for you directly!\n\nBest regards,\nCustomer Success Team",
    "expected_facts": [
      "20% annual discount",
      "Calculate or explain savings (e.g. 2 months free / $20 per seat)",
      "Settings > Billing & Plans > Manage Subscription > Toggle Annual",
      "Proration applied for remaining days"
    ],
    "prohibited_promises": [
      "Do not quote inaccurate discounts (e.g., 50%)",
      "Do not claim annual plans cannot be canceled"
    ],
    "difficulty": "standard"
  },
  {
    "id": "EVAL-003",
    "category": "billing_and_invoicing",
    "subject": "Requesting refund 45 days after payment - company downsizing",
    "customer_email": "We paid for an annual plan 45 days ago, but our startup just had to downsize and we no longer need the software. I know your policy says 14 days, but this is an emergency. Can you please refund our remaining 10 months? - David Ross",
    "customer_sentiment": "urgent",
    "intent": "Customer requesting exception to 14-day refund policy after 45 days due to company downsizing",
    "reference_reply": "Hi David,\n\nI am truly sorry to hear about your company's downsizing—we understand how difficult these organizational shifts can be.\n\nWhile our standard billing terms limit full refunds to within 14 days of purchase, we recognize these are extenuating circumstances. Under our Enterprise Hardship Exception Policy, we can offer you two flexible resolutions:\n1. **Prorated Account Credit**: We can freeze your workspace and convert the remaining 10 months of prepaid balance into transferable credit valid for 24 months.\n2. **Exceptional Prorated Refund**: We can submit a one-time hardship review to our Finance Director to release a prorated refund for the unused months, less a standard 10% administrative processing fee.\n\nPlease let me know which option you would prefer so I can process the approval immediately for you.\n\nWarm regards,\nCustomer Support Operations",
    "expected_facts": [
      "Empathetic tone regarding company downsizing",
      "Acknowledge the 14-day standard policy window while offering hardship options",
      "Provide concrete alternatives (e.g., credit freeze or hardship review for unused months)"
    ],
    "prohibited_promises": [
      "Do not bluntly reject without empathy",
      "Do not guarantee 100% unconditional refund without required approval steps"
    ],
    "difficulty": "edge_case"
  },
  {
    "id": "EVAL-004",
    "category": "technical_bugs",
    "subject": "Tag colors not saving and resetting to default gray",
    "customer_email": "Whenever we assign custom color tags (like red for 'Urgent' or green for 'VIP') in our shared mailbox, they revert back to gray after refreshing the page. This is confusing our reps. Browser: Firefox 126 on Windows 11. - Tara Sterling",
    "customer_sentiment": "frustrated",
    "intent": "Shared mailbox tag colors reverting to default gray upon browser refresh in Firefox",
    "ground_truth_reply": "Hi Tara,\n\nThank you for reaching out, and I apologize for the confusion this color reset is causing your support reps.\n\nThis issue was identified in our Firefox extension cache layer when 'Enhanced Tracking Protection' blocks local storage writes for tag metadata. Here is how to resolve it immediately:\n\n1. In Firefox, click the shield icon to the left of the address bar on your dashboard page and toggle 'Enhanced Tracking Protection' to **OFF for this site**.\n2. In your shared inbox, go to Settings > Tags, select your 'Urgent' and 'VIP' tags, re-select the desired color, and click 'Save Tag Palette'.\n3. We also released an extension hotfix (v4.2.4) that bypasses this storage restriction in Firefox.\n\nCould you please follow those steps and confirm if your tag colors persist upon reload? We're standing by to ensure this works smoothly for your team.\n\nBest regards,\nTechnical Support Team",
    "expected_facts": [
      "Identify Firefox storage/caching interaction",
      "Provide step-by-step resolution (whitelist site / save tag palette)",
      "Mention hotfix update v4.2.4",
      "Test reload persistence"
    ],
    "prohibited_promises": [
      "Do not advise switching to an unsupported third-party tool",
      "Do not tell customer tag colors are not supported"
    ],
    "difficulty": "standard"
  },
  {
    "id": "EVAL-005",
    "category": "technical_bugs",
    "subject": "URGENT: All incoming emails failing to assign automatically since morning",
    "customer_email": "NONE of our auto-assignment rules are working today! We have over 120 customer emails sitting in 'Unassigned' and our agents are stepping on each other's toes. What is going on?! Fix this ASAP! - Greg Henderson, Support VP",
    "customer_sentiment": "frustrated",
    "intent": "High-urgency escalation of broken auto-assignment rules causing unassigned ticket backlog",
    "reference_reply": "Hi Greg,\n\nI understand the severe impact this is having on your operations with 120 unassigned tickets, and I am treating this with highest priority.\n\nI immediately ran a diagnostic on your workspace routing engine. It appears an automation rule created this morning had a conflicting condition (filtering for an archived tag) which caused the downstream assignment queue to pause.\n\nHere is what I have done:\n1. I corrected the conflicting rule condition and verified your assignment triggers are now active.\n2. I executed a retroactive auto-assignment job across the 120 backlogged tickets. They are currently being distributed round-robin across your active team members (will finish within 3 minutes).\n3. Real-time routing is now operating normally.\n\nPlease check your team's assigned views in a moment to confirm the queue has cleared. I will remain on standby to monitor your queue closely.\n\nSincerely,\nMarcus Sterling\nSenior Technical Support Engineer",
    "expected_facts": [
      "Urgent, empathetic tone acknowledging operational impact and ticket count (120)",
      "Diagnosis: conflicting automation rule or paused routing queue",
      "Immediate action: repaired rule and ran retroactive assignment across backlogged tickets",
      "Confirmation that real-time assignment is restored"
    ],
    "prohibited_promises": [
      "Do not dismiss the urgency or ask customer to manually reassign 120 tickets one by one",
      "Do not blame the VP without resolving the situation"
    ],
    "difficulty": "edge_case"
  },
  {
    "id": "EVAL-006",
    "category": "technical_bugs",
    "subject": "API Rate Limit exceeded (HTTP 429) during batch contact sync",
    "customer_email": "Hi, our developer script syncing contacts to shared mailboxes received HTTP 429 'Too Many Requests'. What are your exact REST API rate limits and how can we request a temporary limit bump for our initial data migration? - Sean Wu, Software Engineer",
    "customer_sentiment": "neutral",
    "intent": "Inquiring about REST API rate limits and requesting rate limit increase for initial migration",
    "reference_reply": "Hi Sean,\n\nThanks for reaching out! Happy to clarify our API rate limits for your migration.\n\nOur standard REST API enforces the following rate limits:\n- **Standard Tiers**: 100 requests per minute per API token.\n- **Burst Allowance**: Up to 150 requests in a 10-second burst window.\n- **Headers**: When throttled, check the `Retry-After` and `X-RateLimit-Reset` headers in the HTTP 429 response.\n\nFor large-scale contact migrations:\n1. We strongly recommend using our Batch Endpoint (`POST /api/v2/contacts/batch`) which accepts up to 500 contacts per single HTTP request, minimizing API call volume.\n2. I have provisioned a temporary migration rate limit increase to **300 req/min** on your token, valid for the next 7 days.\n\nPlease let us know if you need any assistance optimizing your batch ingestion script!\n\nBest regards,\nDeveloper Relations Support",
    "expected_facts": [
      "Explain rate limit structure (100 req/min, burst limits)",
      "Explain HTTP 429 Retry-After headers",
      "Recommend batch endpoint POST /api/v2/contacts/batch (up to 500 records)",
      "Provision or guide temporary rate limit increase for migration"
    ],
    "prohibited_promises": [
      "Do not give infinite unlimited API access",
      "Do not claim rate limits cannot be increased"
    ],
    "difficulty": "standard"
  },
  {
    "id": "EVAL-007",
    "category": "account_access",
    "subject": "Need to transfer Account Ownership to new VP of Operations",
    "customer_email": "Hello, our current account owner (jenny@company.com) is transitioning out of the company. We need to transfer primary Account Ownership to our new VP, Alex Morgan (alex.m@company.com). How do we complete this transfer? - Jenny Vance",
    "customer_sentiment": "polite",
    "intent": "Transfer primary account ownership to a new team member",
    "reference_reply": "Hi Jenny,\n\nI can certainly guide you through transferring your Account Ownership smoothly!\n\nBecause you are the current Account Owner, you can perform this transfer directly from your dashboard in two simple steps:\n\n1. Ensure Alex (`alex.m@company.com`) has already accepted an invitation and is an active Admin in your workspace under Settings > Team Management.\n2. Navigate to Settings > Team Management > Account Owner section.\n3. Click 'Transfer Ownership', select Alex Morgan from the dropdown, and confirm with your login password.\n\nOnce submitted, ownership privileges (including billing management and master control) will transfer to Alex immediately, and your user role will automatically adjust to Admin. If you need any assistance or prefer us to verify via security call, please let us know!\n\nBest regards,\nCustomer Support Team",
    "expected_facts": [
      "Existing owner must initiate or approve transfer",
      "New owner must be an existing active user/admin",
      "Settings > Team Management > Transfer Ownership",
      "Requires password confirmation"
    ],
    "prohibited_promises": [
      "Never transfer ownership upon a third party request without existing owner verification",
      "Do not delete the previous owner's account prematurely"
    ],
    "difficulty": "standard"
  },
  {
    "id": "EVAL-008",
    "category": "account_access",
    "subject": "Locked out of account after 5 incorrect password attempts",
    "customer_email": "I mistyped my password and now the screen says 'Account locked due to excessive failed attempts. Contact administrator.' I am the only administrator! Can you unlock me? - Brian Cox",
    "customer_sentiment": "urgent",
    "intent": "Account lockout after 5 failed password attempts for single workspace administrator",
    "reference_reply": "Hi Brian,\n\nI completely understand how frustrating it is to be locked out when you're the sole administrator, and I'm here to help you get back in right away.\n\nOur automated security lockout is a protective measure that automatically resets after **30 minutes**. However, since you are the verified account owner, I have manually cleared the security lock on your email address (`brian.cox@company.com`).\n\nTo securely access your account now:\n1. Visit `https://app.ourdomain.com/password/reset`.\n2. Enter your email address to receive a secure, one-time password reset link.\n3. Create your new password and log in.\n\nPlease check your inbox (and spam folder) for the reset link arriving in the next 1-2 minutes. Let me know if you run into any issues!\n\nBest regards,\nSecurity Support Team",
    "expected_facts": [
      "Security lockout period is 30 minutes",
      "Lock cleared on email address",
      "Direct to official password reset link https://app.ourdomain.com/password/reset",
      "Security precautions maintained"
    ],
    "prohibited_promises": [
      "Never send raw plaintext passwords over email",
      "Do not ask user to tell you their intended password"
    ],
    "difficulty": "standard"
  },
  {
    "id": "EVAL-009",
    "category": "account_access",
    "subject": "Enforcing Mandatory Two-Factor Authentication (2FA) for all team members",
    "customer_email": "Hi, our security audit requires that all 45 support agents in our organization have 2FA enforced. Can we make 2FA mandatory so agents cannot access the shared inbox without setting it up? - Danica Patrick, CISO",
    "customer_sentiment": "neutral",
    "intent": "How to enforce mandatory organization-wide 2FA for all agents",
    "reference_reply": "Hi Danica,\n\nYes, absolutely. Enforcing organization-wide Two-Factor Authentication (2FA) is fully supported on your plan.\n\nHere is how to enforce 2FA across all 45 workspace members:\n1. Log in as an Account Owner or Admin and go to Settings > Security & Compliance.\n2. Under 'Authentication Policies', toggle **'Enforce Two-Factor Authentication (2FA)'** to **ON**.\n3. Choose an enforcement grace period (we recommend '48-hour Grace Period' so active agents can set up an authenticator app without immediate interruption).\n4. Click 'Save Security Policy'.\n\nOnce the grace period concludes, any member who has not configured 2FA will be prompted to scan a QR code using Google Authenticator, Authy, or 1Password before accessing any shared inboxes. Admins can track compliance status under Settings > Team Management > 2FA Audit Column.\n\nBest regards,\nEnterprise Security Support",
    "expected_facts": [
      "Settings > Security & Compliance > Authentication Policies > Enforce 2FA",
      "Grace period recommendation (e.g. 48 hours) to prevent team lockout",
      "Supports standard TOTP authenticator apps (Google Authenticator, Authy)",
      "Audit dashboard to monitor team compliance"
    ],
    "prohibited_promises": [
      "Do not recommend disabling 2FA",
      "Do not claim SMS 2FA is the only method"
    ],
    "difficulty": "standard"
  },
  {
    "id": "EVAL-010",
    "category": "feature_requests",
    "subject": "Can we export customer email threads to PDF or CSV with full conversation history?",
    "customer_email": "Hello, our compliance team needs to periodically export entire customer email threads (including all replies, internal notes, and timestamps) into a single PDF or CSV file for legal auditing. Is this possible? Thanks, Melissa Reed.",
    "customer_sentiment": "neutral",
    "intent": "Inquiring how to export email threads with full replies, notes, and audit history to PDF/CSV",
    "reference_reply": "Hi Melissa,\n\nYes, exporting complete conversation threads for compliance and legal auditing is fully supported!\n\nHere are the two ways you can export records:\n\n1. **Single Conversation PDF Export**:\n   - Open any customer email thread.\n   - Click the '...' (More Options) icon in the top right header.\n   - Select **'Print / Export as PDF'**.\n   - Ensure the checkbox **'Include Internal Notes & Audit History'** is checked. This compiles all messages, internal notes, and chronological timestamps into a formatted PDF.\n\n2. **Bulk CSV Export for Auditing**:\n   - Navigate to Settings > Data Management > Audit Exports.\n   - Select your desired date range and choose 'Full Conversation Thread Archive (CSV/JSON)'.\n   - Click 'Generate Export' to receive an encrypted download package containing message bodies, participant headers, and SLA timestamps.\n\nPlease let us know if your legal team requires any specific audit formatting!\n\nBest regards,\nCustomer Support Team",
    "expected_facts": [
      "Single thread export: '...' More Options > Print / Export as PDF",
      "Option to include internal notes and audit history",
      "Bulk audit export: Settings > Data Management > Audit Exports (CSV/JSON)",
      "Includes timestamps and participant headers"
    ],
    "prohibited_promises": [
      "Do not state that export requires custom engineering scripts",
      "Do not state internal notes cannot be exported"
    ],
    "difficulty": "standard"
  },
  {
    "id": "EVAL-011",
    "category": "feature_requests",
    "subject": "Integration with Salesforce CRM to view deal stage inside Gmail",
    "customer_email": "Hey team, do you have a Salesforce integration? Our account managers want to see the lead status and open deal size directly inside the Gmail sidebar while answering customer inquiries. - Brad Simmons",
    "customer_sentiment": "curious",
    "intent": "Inquiring about Salesforce CRM integration to display lead status and deal size in sidebar",
    "reference_reply": "Hi Brad,\n\nGreat news—yes, we have a native **Salesforce CRM Integration** built directly into our shared inbox extension sidebar!\n\nWith the Salesforce integration active:\n- When an agent opens an email, the sidebar automatically pulls and displays the customer's Salesforce Contact/Lead profile, Account name, and Open Opportunities (including Deal Value and Stage).\n- Agents can edit Salesforce records or log email activities without ever leaving Gmail.\n\nTo connect your Salesforce organization:\n1. Have an Admin go to Settings > Integrations > Salesforce.\n2. Click 'Connect Salesforce' and authenticate with your Salesforce credentials (OAuth 2.0).\n3. Map your preferred Salesforce fields to the sidebar view.\n4. Click 'Save & Sync'.\n\nHere is our setup guide with a video walkthrough: `docs.ourdomain.com/integrations/salesforce`. Let us know if you'd like a guided walkthrough with one of our solution architects!\n\nBest regards,\nSolutions Support Team",
    "expected_facts": [
      "Native Salesforce CRM integration available in sidebar",
      "Displays Contact/Lead details, Open Opportunities, Deal Value, and Stage",
      "Settings > Integrations > Salesforce > Connect Salesforce (OAuth 2.0)",
      "Setup guide link provided"
    ],
    "prohibited_promises": [
      "Do not claim Salesforce requires custom API coding",
      "Do not promise unreleased features"
    ],
    "difficulty": "standard"
  },
  {
    "id": "EVAL-012",
    "category": "sla_escalations",
    "subject": "UNACCEPTABLE: Third outage this month. We are losing clients. What is our compensation?",
    "customer_email": "Your system went down again for 45 minutes today during peak European trading hours. This is the 3rd time in September. Our clients could not reach our trading desk. I want an immediate explanation, what measures you are implementing to prevent this, and what SLA credit/refund we are receiving. - Henrik Lindqvist, Head of Trading Infrastructure",
    "customer_sentiment": "frustrated",
    "intent": "Severe client escalation regarding recurring system downtime, demanding root cause, preventative measures, and financial SLA compensation",
    "reference_reply": "Dear Henrik,\n\nI understand completely why you are furious. Three service disruptions during peak trading hours is wholly unacceptable, and I sincerely apologize for the severe impact on your trading operations and your clients.\n\nI am handling this personally alongside our VP of Infrastructure and our Head of Enterprise Customer Success. Here is our immediate commitment and plan of action:\n\n1. **Root Cause & Architectural Mitigation**:\n   - Today's disruption was triggered by a cache cluster partition in our Frankfurt availability zone. Traffic failed to seamlessly route to our secondary Ireland cluster.\n   - Our SRE team has deployed automated cross-region active-active failover routing to ensure redundant fallback occurs within 10 seconds without human intervention.\n   - We are publishing a comprehensive Post-Incident Analysis (RCA) within 24 hours.\n\n2. **SLA Financial Credit Compensation**:\n   - Our enterprise SLA guarantees 99.9% uptime. Because our availability for September currently stands at 99.4%, you are entitled to a contractual service credit.\n   - We have automatically applied a **25% SLA credit** to your next invoice (#INV-9941), and our VP of Success will review further commercial accommodations.\n\n3. **Executive Review Meeting**:\n   - I would like to schedule a 20-minute review call tomorrow between your infrastructure team and our VP of Engineering to review the technical telemetry. Please let me know what time works best.\n\nSincerely,\nMarcus Sterling\nDirector of Enterprise Customer Operations",
    "expected_facts": [
      "Acknowledge gravity, frequency of disruptions, and apologize sincerely",
      "Technical root cause summary (Frankfurt cluster partition, active-active failover deployed)",
      "Post-Incident Review (RCA) commitment within 24 hours",
      "SLA contractual financial credit calculated and applied (e.g. 25% credit)",
      "Offer executive engineering briefing call"
    ],
    "prohibited_promises": [
      "Do not minimize the issue or make defensive excuses",
      "Do not refuse SLA compensation when contractual SLA was breached",
      "Do not pass the blame to upstream cloud providers without remediation"
    ],
    "difficulty": "adversarial"
  },
  {
    "id": "EVAL-013",
    "category": "product_how_to",
    "subject": "How to set up Out-of-Office auto-replies for the shared mailbox during holidays",
    "customer_email": "Our support desk will be closed for the upcoming Thanksgiving weekend (Thursday to Sunday). How do we configure an Out-of-Office auto-responder on our shared support@ email so customers know we will reply on Monday? Thanks! - Kelly Robinson",
    "customer_sentiment": "polite",
    "intent": "Configuring scheduled Out-of-Office holiday auto-reply on shared mailbox",
    "reference_reply": "Hi Kelly,\n\nHappy upcoming Thanksgiving! Setting up a holiday auto-responder for your shared mailbox is very straightforward.\n\nHere is how to configure it:\n1. Navigate to Settings > Shared Mailboxes and select your `support@` mailbox.\n2. Click the 'Auto-Responders & OOO' tab.\n3. Toggle **'Enable Scheduled Auto-Responder'** to ON.\n4. Set your active timeframe: Start: Thursday 00:00 to End: Sunday 23:59.\n5. Draft your message informing customers of your holiday hours and when normal responses resume on Monday.\n6. Under Advanced Options, ensure **'Send maximum 1 auto-reply per sender'** is selected (this prevents email looping with customer automated systems).\n7. Click 'Save and Schedule'.\n\nThe auto-responder will activate and deactivate strictly on schedule without requiring manual intervention on Monday morning. Enjoy your holiday weekend!\n\nBest regards,\nCustomer Support Team",
    "expected_facts": [
      "Settings > Shared Mailboxes > [Mailbox] > Auto-Responders & OOO",
      "Scheduled start and end timeframe configuration",
      "Loop prevention: 1 auto-reply per sender",
      "Auto-deactivates automatically on Monday"
    ],
    "prohibited_promises": [
      "Do not tell user to change personal Gmail OOO settings which affect personal emails",
      "Do not omit loop prevention advice"
    ],
    "difficulty": "standard"
  },
  {
    "id": "EVAL-014",
    "category": "product_how_to",
    "subject": "Using shared email tags vs Gmail labels - what is the difference?",
    "customer_email": "Hi, I noticed we have both regular Gmail labels and your platform's 'Shared Tags' in our sidebar. What is the difference between the two? If I apply a tag, will my teammate see it? - Timothy Chen",
    "customer_sentiment": "curious",
    "intent": "Clarify functional distinction between personal Gmail labels and shared mailbox tags",
    "reference_reply": "Hi Timothy,\n\nThat is a very common and important distinction to keep in mind!\n\nHere is how they differ:\n\n1. **Shared Tags (Our Platform)**:\n   - **Team-wide Visibility**: When you attach a Shared Tag (e.g., 'Billing', 'VIP', 'Bug') to a conversation, **every agent** in that shared mailbox instantly sees it in real time.\n   - **Automations & SLAs**: Shared tags can trigger automated routing rules, SLA tracking, and aggregate analytics reports.\n   - **Centralized**: Admins manage tag names and color palettes centrally.\n\n2. **Gmail Labels (Native Google)**:\n   - **Personal Only**: Native Gmail labels are private to your individual Google account. Teammates cannot see your personal Gmail labels unless they access your personal mailbox directly.\n   - **No Team Sync**: Applying a Gmail label does not update shared dashboards or team reports.\n\n**Recommendation**: For team collaboration, ticket categorization, and SLA tracking, always use **Shared Tags**. Keep Gmail labels for your own personal email sorting!\n\nBest regards,\nCustomer Support Team",
    "expected_facts": [
      "Shared Tags: visible to all agents in shared mailbox in real time",
      "Shared Tags integrate with automations, SLAs, and reports",
      "Gmail Labels: private to individual personal Google accounts",
      "Clear recommendation to use Shared Tags for collaborative customer support"
    ],
    "prohibited_promises": [
      "Do not claim Gmail labels sync across team members automatically",
      "Do not confuse shared tags with personal labels"
    ],
    "difficulty": "standard"
  },
  {
    "id": "EVAL-015",
    "category": "sla_escalations",
    "subject": "Threatening Chargeback: Cancel my account and refund immediately or I dispute with Amex",
    "customer_email": "I requested a cancellation 3 days ago and no one replied! If my account is not canceled right this second and the $450 charge reversed, I am filing a fraud dispute and chargeback with American Express today! - Richard Vance",
    "customer_sentiment": "frustrated",
    "intent": "De-escalate angry customer threatening Amex credit card chargeback and expedite cancellation & refund",
    "reference_reply": "Hi Richard,\n\nI apologize sincerely for the delay in our response to your cancellation request—I understand your frustration, and you will not need to file a dispute with American Express.\n\nI have taken immediate action on your account today:\n1. **Subscription Canceled**: Your subscription has been canceled immediately, and all future billing is disabled.\n2. **Full Refund Processed**: I have processed a full refund of $450.00 directly back to your American Express card (#ending in your card on file).\n3. **Confirmation & Reference**: Your refund transaction ID is #RF-39910. Depending on American Express processing times, the credit typically appears on your online statement within 1-3 business days.\n\nI have emailed your formal cancellation and refund receipt to this address. I truly apologize that your initial inquiry was delayed, and I appreciate your past business with us.\n\nBest regards,\nMarcus Sterling\nCustomer Support Operations Lead",
    "expected_facts": [
      "Immediate de-escalation: reassure customer dispute is unnecessary",
      "Confirm immediate cancellation of subscription",
      "Confirm full refund of $450 processed to Amex card",
      "Provide refund reference ID and timeline (1-3 business days)"
    ],
    "prohibited_promises": [
      "Do not argue with or threaten the customer about chargeback fees",
      "Do not delay cancellation or demand lengthy exit surveys"
    ],
    "difficulty": "adversarial"
  },
  {
    "id": "EVAL-016",
    "category": "billing_and_invoicing",
    "subject": "Can we pay by ACH / Bank Wire transfer instead of credit card?",
    "customer_email": "Hello, our corporate procurement policy does not allow recurring software charges over $5,000 on corporate credit cards. Can we pay for our 30-seat Enterprise annual contract via ACH / Wire Transfer against an invoice? - Monica Bellucci, Finance Director",
    "customer_sentiment": "neutral",
    "intent": "Inquiring about ACH / Wire transfer payment terms for annual Enterprise contract",
    "reference_reply": "Hi Monica,\n\nYes, absolutely! We support ACH and Wire Transfer payments for all annual Enterprise and Pro contracts exceeding $2,500.\n\nHere is our standard invoicing process:\n1. We issue a formal Net 30 invoice including our corporate banking coordinates (ACH routing, SWIFT/BIC, and IBAN) along with our W-9 tax form.\n2. Your procurement team can remit payment via ACH or domestic/international wire transfer.\n3. We can activate your 30-seat Enterprise workspace immediately upon contract signature so your team does not experience onboarding delays while accounting processes the payment.\n\nI have attached our standard vendor packet and W-9 form to this email. Could you please confirm your company's legal billing entity name and purchase order (PO) number if applicable so I can generate your Net 30 invoice?\n\nBest regards,\nBilling & Finance Operations",
    "expected_facts": [
      "ACH / Wire transfer supported for annual contracts over $2,500",
      "Standard Net 30 invoice terms with banking coordinates and W-9",
      "Immediate workspace activation upon contract execution",
      "Request billing entity details and PO number"
    ],
    "prohibited_promises": [
      "Do not force credit card on Enterprise annual contracts",
      "Do not offer Net 90 terms without executive approval"
    ],
    "difficulty": "standard"
  },
  {
    "id": "EVAL-017",
    "category": "technical_bugs",
    "subject": "Email threads showing HTML code artifacts and unparsed CSS",
    "customer_email": "Some incoming emails from customers using Outlook are rendering raw HTML code (like <div>, <p style=...>, and &nbsp;) instead of styled rich text in our shared mailbox view. It makes reading customer inquiries very difficult. Can you fix this? - Frank Castle",
    "customer_sentiment": "frustrated",
    "intent": "Shared inbox displaying unparsed HTML/CSS code artifacts for emails originating from Outlook",
    "reference_reply": "Hi Frank,\n\nThank you for alerting us to this, and I apologize for the readability issues this is causing your agents.\n\nThis behavior occurs when incoming emails contain nested MSO (Microsoft Outlook) conditional comment wrappers (`<!--[if mso]>`), which our sanitizer previously escaped as plaintext entities to prevent XSS.\n\nOur engineering team deployed an update to our email sanitization parser today (v3.18.2) to properly strip MSO conditionals while preserving valid HTML formatting.\n\nTo view the affected emails with clean formatting:\n1. Click the 'Reload Thread' button in the top right corner of any affected conversation, or hard-refresh your browser tab (Ctrl+F5 / Cmd+Shift+R).\n2. Any new incoming Outlook emails will now render clean, formatted rich text automatically.\n\nPlease reply if you still notice raw HTML tags in any new incoming threads!\n\nBest regards,\nTechnical Support Team",
    "expected_facts": [
      "Acknowledge Outlook MSO conditional wrapper parsing issue",
      "Explain fix deployed in email sanitizer (v3.18.2)",
      "Troubleshooting: click 'Reload Thread' or hard-refresh browser",
      "Confirm new emails render formatted text automatically"
    ],
    "prohibited_promises": [
      "Do not suggest customer disable HTML security sanitization",
      "Do not claim Outlook emails cannot be supported"
    ],
    "difficulty": "standard"
  },
  {
    "id": "EVAL-018",
    "category": "account_access",
    "subject": "How to restrict an agent from deleting customer conversations?",
    "customer_email": "We want our junior agents to answer and tag emails, but we want to prevent them from having permission to permanently delete customer conversations or shared mailboxes. How do we configure this role restriction? - Teresa Mendoza",
    "customer_sentiment": "neutral",
    "intent": "Configuring granular role permissions to prevent junior agents from deleting conversations or mailboxes",
    "reference_reply": "Hi Teresa,\n\nProtecting customer conversation records from accidental deletion is a great security best practice, and our role permissions are built to ensure this!\n\nBy default:\n- **Members** (standard agents) can resolve or close tickets, but **cannot permanently delete conversations** or modify shared mailbox configurations.\n- Only **Admins** and **Account Owners** have permission to permanently purge conversations or delete mailboxes.\n\nTo ensure your junior agents cannot delete records:\n1. Navigate to Settings > Team Management > Users.\n2. Ensure all junior agents are assigned the **'Member'** role (do not assign them Admin privileges).\n3. Under Settings > Security & Data Retention, verify that **'Restrict Ticket Deletion to Workspace Admins Only'** is toggled **ON**.\n4. (Optional) Toggle on 'Soft-Delete Trash Bin (30-day retention)' so any closed or trashed conversation can be easily restored by an Admin.\n\nThis completely prevents junior agents from purging any customer records. Let us know if you would like us to review your role settings!\n\nBest regards,\nCustomer Support Team",
    "expected_facts": [
      "Members cannot delete conversations by default; deletion restricted to Admins",
      "Assign junior agents the 'Member' role under Settings > Team Management",
      "Verify 'Restrict Ticket Deletion to Workspace Admins Only' toggle",
      "Mention Soft-Delete 30-day retention safety net"
    ],
    "prohibited_promises": [
      "Do not make junior agents Admins",
      "Do not tell customer permissions cannot be restricted"
    ],
    "difficulty": "standard"
  },
  {
    "id": "EVAL-019",
    "category": "feature_requests",
    "subject": "Can we auto-assign tickets based on language (Spanish vs English)?",
    "customer_email": "We have bilingual agents who handle our Spanish-speaking customers. Can your automation rules detect if an incoming email is written in Spanish and automatically route it to our Spanish support team? - Gabriela Alvarez",
    "customer_sentiment": "curious",
    "intent": "Language-based automated routing to route Spanish incoming emails to bilingual agents",
    "reference_reply": "Hi Gabriela,\n\nYes! Automated language detection and routing is fully supported using our **Smart Routing Rules**.\n\nHere is how you can set up language-based routing for your Spanish team:\n1. Navigate to Settings > Workflows & Automation > Create Rule.\n2. Name your rule: 'Spanish Inquiries Routing'.\n3. Under 'Conditions', select: **'Email Language equals Spanish (es)'**.\n4. (Optional) You can add a secondary condition like *'Body contains common Spanish keywords (hola, gracias, ayuda)'* if you want strict matching.\n5. Under 'Actions', select: **'Assign to Team'** > choose 'Spanish Support Team' (or select specific bilingual agents in a round-robin pool).\n6. (Optional) Add action: 'Add Tag: [Language: Spanish]'.\n7. Click 'Save and Activate'.\n\nOur system uses automatic NLP language detection on the incoming email body. As soon as a Spanish inquiry arrives, it will route directly to your Spanish-speaking agents within seconds! Here is our guide: `docs.ourdomain.com/automations/language-routing`.\n\nBest regards,\nCustomer Success Team",
    "expected_facts": [
      "Language detection supported in Smart Routing Rules",
      "Settings > Workflows & Automation > Condition: Email Language equals Spanish (es)",
      "Action: Assign to Team or round-robin bilingual agents",
      "Optional tagging for reporting",
      "Documentation link provided"
    ],
    "prohibited_promises": [
      "Do not claim language routing requires manual tagging",
      "Do not quote external translation API charges"
    ],
    "difficulty": "standard"
  },
  {
    "id": "EVAL-020",
    "category": "sla_escalations",
    "subject": "URGENT: Legal inquiry - We received a subpoena requiring historical email records",
    "customer_email": "CONFIDENTIAL: We have been served with a federal civil subpoena requiring all email communications between our company and 'Acme Corp' from Jan 1, 2024 to Dec 31, 2024. Does your system retain immutable audit logs and how do we perform a legal hold export? - Raymond Reddington, Chief Legal Officer",
    "customer_sentiment": "urgent",
    "intent": "Legal hold inquiry regarding immutable audit logs and compliance export for subpoena",
    "reference_reply": "Dear Raymond,\n\nWe acknowledge the legal confidentiality and urgency of your inquiry regarding federal subpoena compliance.\n\nOur enterprise architecture complies with SOC 2 Type II and ISO 27001 regulatory standards and includes comprehensive legal hold and litigation export capabilities:\n\n1. **Immutable Audit Logs**:\n   - All email deliveries, incoming messages, internal agent notes, assignment changes, and timestamp telemetry are recorded in append-only immutable audit storage.\n   - Historical records from the 2024 calendar year are fully intact and preserved.\n\n2. **Initiating Legal Hold & Audit Export**:\n   - Navigate to Settings > Security & Compliance > Legal Hold.\n   - Click 'Create Legal Hold' to freeze records associated with domain `@acmecorp.com` and prevent any automated retention purges.\n   - Click 'Generate Compliance Export', set the date range from `2024-01-01` to `2024-12-31`, and choose format (Encrypted ZIP containing RFC 822 `.eml` files and SHA-256 hash manifests for chain of custody).\n\n3. **Dedicated Compliance Officer Support**:\n   - I have assigned our Senior Data Protection Officer (reference #LEGAL-2026-904) to assist your legal team directly. If you require a sworn Affidavit of Custodian of Records, we will prepare one promptly.\n\nSincerely,\nLegal Compliance & Enterprise Security Support",
    "expected_facts": [
      "Acknowledge confidentiality and legal urgency of subpoena",
      "Confirm immutable audit logs and 2024 record preservation under SOC 2",
      "Steps: Settings > Security & Compliance > Legal Hold > Create Legal Hold",
      "Export format: Encrypted ZIP with RFC 822 .eml and SHA-256 chain of custody manifest",
      "Offer Affidavit of Custodian of Records and direct DPO assistance"
    ],
    "prohibited_promises": [
      "Never disclose subpoena details publicly",
      "Do not claim records cannot be retrieved or that chain of custody is not supported"
    ],
    "difficulty": "adversarial"
  }
]

def main():
    with open(EVAL_FILE, "w", encoding="utf-8") as f:
        json.dump(EVAL_TEST_CASES, f, indent=2, ensure_ascii=False)
    print(f"Successfully generated {len(EVAL_TEST_CASES)} evaluation test cases at {EVAL_FILE}")

if __name__ == "__main__":
    main()
