#!/usr/bin/env python3
"""Generate a themed sample dataset for the omnimodal agent memory demo.

Default mode: 8 files around a single theme ("Acme Analytics pricing complaint").
Advanced mode (--advanced): 32 files across 5 distinct semantic themes, designed
to produce visible topic-based clusters in the t-SNE visualization.
"""

import argparse
import json
from pathlib import Path
from typing import TypedDict

DATA_DIR = Path("data")


# ---------------------------------------------------------------------------
# Theme definitions (advanced mode)
# ---------------------------------------------------------------------------
class ThemeFile(TypedDict):
    rel_path: str
    description: str
    content: str  # text content / slide text / speech text
    bg_color: str  # hex color for images/video


class Theme(TypedDict):
    name: str
    files: list[ThemeFile]


ADVANCED_THEMES: list[Theme] = [
    {
        "name": "onboarding",
        "files": [
            {
                "rel_path": "notes/onboarding_checklist.txt",
                "description": (
                    "Step-by-step onboarding checklist for Initech Corp "
                    "covering API setup, SSO, data import, and team invitations"
                ),
                "content": (
                    "Initech Corp — Onboarding Checklist\n"
                    "Date: 2025-03-18\n\n"
                    "1. Generate API keys in the admin console\n"
                    "2. Configure SSO/SAML with Initech's identity provider\n"
                    "3. Run initial data import (CSV + Salesforce connector)\n"
                    "4. Invite Initech's 12-person analytics team\n"
                    "5. Schedule 4-week training program with CSM\n"
                    "6. Set up Slack integration for alerts\n"
                    "7. Validate dashboard permissions per role\n"
                ),
                "bg_color": "#1b2d1b",
            },
            {
                "rel_path": "notes/kickoff_meeting.txt",
                "description": (
                    "Kickoff meeting notes with Initech Corp discussing "
                    "onboarding timeline, integration milestones, and training schedule"
                ),
                "content": (
                    "Kickoff Meeting — Initech Corp Onboarding\n"
                    "Date: 2025-03-20\n"
                    "Attendees: Lisa (CSM), Raj (Solutions), Tom (Initech CTO)\n\n"
                    "Agenda:\n"
                    "- Review 4-week onboarding timeline\n"
                    "- API integration milestones: week 1 sandbox, week 2 production\n"
                    "- SSO setup scheduled for Monday with Initech IT\n"
                    "- Data migration: 2.4M records from legacy warehouse\n"
                    "- Training: 3 live sessions + recorded walkthroughs\n"
                    "- Success criteria: 80% team adoption by week 4\n"
                ),
                "bg_color": "#1b2d1b",
            },
            {
                "rel_path": "images/onboarding_welcome.png",
                "description": (
                    "Welcome slide for Initech Corp onboarding showing "
                    "4-week timeline: API setup, SSO, data import, team training"
                ),
                "content": (
                    "WELCOME TO ACME ANALYTICS\n"
                    "Initech Corp Onboarding\n\n"
                    "Week 1: API Keys & Sandbox\n"
                    "Week 2: SSO & Production Setup\n"
                    "Week 3: Data Import & Migration\n"
                    "Week 4: Team Training & Go-Live"
                ),
                "bg_color": "#1b2d1b",
            },
            {
                "rel_path": "pdfs/onboarding_guide.pdf",
                "description": (
                    "Enterprise onboarding guide covering API key generation, "
                    "SSO configuration, data import procedures, and team setup"
                ),
                "content": (
                    "This guide walks new enterprise customers through the Acme "
                    "Analytics onboarding process. Step 1: Generate API keys from "
                    "the admin console under Settings > API. Step 2: Configure "
                    "SSO/SAML by uploading your IdP metadata XML. Step 3: Import "
                    "data using our CSV uploader or Salesforce/HubSpot connectors. "
                    "Step 4: Invite team members and assign roles (Admin, Analyst, "
                    "Viewer). Step 5: Complete the onboarding checklist and schedule "
                    "your first training session with your Customer Success Manager."
                ),
                "bg_color": "#1b2d1b",
            },
            {
                "rel_path": "audio/onboarding_call.mp3",
                "description": (
                    "Customer success manager scheduling onboarding sessions "
                    "with Initech Corp, discussing API setup and training timeline"
                ),
                "content": (
                    "Hi Tom, this is Lisa from Acme Analytics customer success. "
                    "I'm reaching out to schedule your onboarding sessions. We "
                    "have your API sandbox ready and I'd like to walk your team "
                    "through the setup process this Thursday. We'll cover API key "
                    "generation, SSO configuration, and the data import workflow. "
                    "After that, we'll schedule three training sessions over the "
                    "next two weeks. Looking forward to getting Initech up and "
                    "running smoothly."
                ),
                "bg_color": "#1b2d1b",
            },
            {
                "rel_path": "video/onboarding_walkthrough.mp4",
                "description": (
                    "4-step onboarding walkthrough: API key generation, SSO "
                    "setup, data import, and team invitation process"
                ),
                "content": (
                    "Onboarding Walkthrough\n\n"
                    "Step 1: Generate API Key\n"
                    "Step 2: Configure SSO/SAML\n"
                    "Step 3: Import Your Data\n"
                    "Step 4: Invite Your Team"
                ),
                "bg_color": "#1b2d1b",
            },
        ],
    },
    {
        "name": "security_incident",
        "files": [
            {
                "rel_path": "notes/security_incident_report.txt",
                "description": (
                    "Security incident report: 12 accounts accessed via "
                    "unpatched dependency, containment and remediation steps"
                ),
                "content": (
                    "SECURITY INCIDENT REPORT\n"
                    "Date: 2025-03-14\n"
                    "Severity: HIGH\n\n"
                    "Summary: Unauthorized access detected on 12 enterprise "
                    "accounts via an unpatched third-party dependency "
                    "(CVE-2025-1234). The vulnerability allowed session "
                    "hijacking through crafted API requests.\n\n"
                    "Timeline:\n"
                    "- 09:12 UTC: Anomalous API traffic detected\n"
                    "- 09:45 UTC: Security team alerted, investigation begun\n"
                    "- 10:30 UTC: Vulnerability identified, patch deployed\n"
                    "- 11:00 UTC: All affected sessions invalidated\n\n"
                    "Remediation: Dependency updated, all API tokens rotated, "
                    "affected customers notified.\n"
                ),
                "bg_color": "#2d1b1b",
            },
            {
                "rel_path": "notes/vulnerability_assessment.txt",
                "description": (
                    "Vulnerability assessment for CVE-2025-1234: severity HIGH, "
                    "48-hour remediation window, patch verification steps"
                ),
                "content": (
                    "Vulnerability Assessment — CVE-2025-1234\n"
                    "Date: 2025-03-15\n\n"
                    "CVE: CVE-2025-1234\n"
                    "Severity: HIGH (CVSS 8.1)\n"
                    "Component: auth-middleware v2.3.1\n"
                    "Fix: Upgrade to auth-middleware v2.3.2\n\n"
                    "Impact: Session hijacking via crafted Authorization header.\n"
                    "Affected systems: API gateway, customer portal.\n"
                    "Remediation window: 48 hours.\n\n"
                    "Verification steps:\n"
                    "1. Confirm dependency version >= 2.3.2\n"
                    "2. Run penetration test against auth endpoints\n"
                    "3. Verify no residual compromised sessions\n"
                    "4. Update security audit log\n"
                ),
                "bg_color": "#2d1b1b",
            },
            {
                "rel_path": "images/security_audit_dashboard.png",
                "description": (
                    "Security audit dashboard showing 1 critical vulnerability, "
                    "3 high severity issues, 89% systems patched"
                ),
                "content": (
                    "SECURITY AUDIT DASHBOARD\n\n"
                    "Critical: 1  |  High: 3  |  Medium: 7\n"
                    "Systems Patched: 89%\n"
                    "Last Scan: 2025-03-15 14:00 UTC\n\n"
                    "Action Required:\n"
                    "Patch auth-middleware on 4 nodes"
                ),
                "bg_color": "#2d1b1b",
            },
            {
                "rel_path": "pdfs/incident_response_plan.pdf",
                "description": (
                    "Formal incident response plan covering detection, "
                    "containment, eradication, recovery, and post-mortem procedures"
                ),
                "content": (
                    "Acme Analytics Incident Response Plan. Phase 1 Detection: "
                    "Automated monitoring triggers alerts on anomalous API traffic "
                    "patterns and failed authentication attempts. Phase 2 "
                    "Containment: Isolate affected systems, revoke compromised "
                    "tokens, enable enhanced logging. Phase 3 Eradication: Patch "
                    "vulnerable dependencies, rotate all credentials, update "
                    "firewall rules. Phase 4 Recovery: Restore normal operations, "
                    "verify system integrity, re-enable customer access. Phase 5 "
                    "Post-Mortem: Document timeline, root cause analysis, update "
                    "runbooks, schedule follow-up review."
                ),
                "bg_color": "#2d1b1b",
            },
            {
                "rel_path": "audio/security_briefing.mp3",
                "description": (
                    "Urgent security briefing on unauthorized access incident, "
                    "CVE-2025-1234 exploitation, and immediate response actions"
                ),
                "content": (
                    "Team, this is an urgent security briefing. At nine twelve "
                    "UTC today we detected unauthorized access to twelve enterprise "
                    "accounts. The attack exploited CVE twenty twenty-five twelve "
                    "thirty-four in our authentication middleware. We've already "
                    "deployed the patch, rotated all affected API tokens, and "
                    "invalidated compromised sessions. All affected customers have "
                    "been notified. We need everyone to verify their services are "
                    "running the patched version by end of day."
                ),
                "bg_color": "#2d1b1b",
            },
            {
                "rel_path": "video/security_patch_demo.mp4",
                "description": (
                    "Security patch deployment demo showing vulnerability scan, "
                    "patch application, verification, and audit completion"
                ),
                "content": (
                    "Security Patch Deployment\n\n"
                    "1. Vulnerability Scan: COMPLETE\n"
                    "2. Patch Applied: v2.3.2\n"
                    "3. Verification: PASSED\n"
                    "4. Audit Updated: DONE"
                ),
                "bg_color": "#2d1b1b",
            },
        ],
    },
    {
        "name": "product_launch",
        "files": [
            {
                "rel_path": "notes/product_launch_plan.txt",
                "description": (
                    "Insights AI product launch plan: beta April 15, "
                    "GA May 1, marketing timeline and feature highlights"
                ),
                "content": (
                    "Insights AI — Launch Plan\n"
                    "Date: 2025-03-16\n\n"
                    "Timeline:\n"
                    "- April 1: Internal dogfood release\n"
                    "- April 15: Closed beta (50 customers)\n"
                    "- April 25: Public beta\n"
                    "- May 1: General Availability\n\n"
                    "Key features:\n"
                    "- Natural language query interface\n"
                    "- AI-powered anomaly detection\n"
                    "- Automated insight generation\n"
                    "- Custom report scheduling\n\n"
                    "Marketing: Blog post, demo video, webinar series.\n"
                ),
                "bg_color": "#1b1b2d",
            },
            {
                "rel_path": "notes/beta_feedback_summary.txt",
                "description": (
                    "Beta feedback summary for Insights AI: 85% positive, "
                    "top feature requests and usability improvements"
                ),
                "content": (
                    "Insights AI — Beta Feedback Summary\n"
                    "Date: 2025-04-20\n"
                    "Respondents: 42 / 50 beta users\n\n"
                    "Overall satisfaction: 85% positive\n"
                    "NPS: 62\n\n"
                    "Top feature requests:\n"
                    "1. Export insights to PDF (18 votes)\n"
                    "2. Slack notifications for anomalies (15 votes)\n"
                    "3. Custom dashboards (12 votes)\n"
                    "4. API access for programmatic queries (9 votes)\n\n"
                    "Common feedback: 'The natural language interface is "
                    "intuitive but sometimes slow for complex queries.'\n"
                ),
                "bg_color": "#1b1b2d",
            },
            {
                "rel_path": "images/launch_announcement.png",
                "description": (
                    "Insights AI launch announcement slide: introducing "
                    "AI-powered analytics with natural language queries"
                ),
                "content": (
                    "INTRODUCING INSIGHTS AI\n"
                    "AI-Powered Analytics\n\n"
                    "Natural Language Queries\n"
                    "Anomaly Detection\n"
                    "Automated Insights\n\n"
                    "Beta: April 15 | GA: May 1"
                ),
                "bg_color": "#1b1b2d",
            },
            {
                "rel_path": "pdfs/insights_ai_whitepaper.pdf",
                "description": (
                    "Insights AI technical whitepaper covering LLM architecture, "
                    "retrieval-augmented generation, and analytics pipeline"
                ),
                "content": (
                    "Insights AI Technical Whitepaper. Insights AI combines "
                    "large language models with retrieval-augmented generation "
                    "to deliver intelligent analytics. The architecture uses a "
                    "fine-tuned LLM connected to the customer's data warehouse "
                    "via a semantic retrieval layer. Queries are parsed into "
                    "structured analytics operations, executed against the data, "
                    "and results are presented in natural language with supporting "
                    "visualizations. The system achieves 94% accuracy on benchmark "
                    "analytics queries while maintaining sub-second response times "
                    "for standard operations."
                ),
                "bg_color": "#1b1b2d",
            },
            {
                "rel_path": "audio/product_demo_narration.mp3",
                "description": (
                    "Narrated demo of Insights AI showing natural language "
                    "query, AI processing, and automated insight generation"
                ),
                "content": (
                    "Welcome to the Insights AI demo. Watch as I type a natural "
                    "language query: show me revenue trends for the last quarter. "
                    "The AI processes your request, queries the data warehouse, "
                    "and generates a visual report with key insights highlighted. "
                    "Notice how it automatically detected the fifteen percent "
                    "revenue dip in February and flagged it as an anomaly. You "
                    "can drill down into any insight by clicking on it or asking "
                    "a follow-up question."
                ),
                "bg_color": "#1b1b2d",
            },
            {
                "rel_path": "video/insights_ai_demo.mp4",
                "description": (
                    "Live demo of Insights AI: user query, AI processing, "
                    "and result visualization with anomaly detection"
                ),
                "content": (
                    "Insights AI — Live Demo\n\n"
                    "Query: Revenue trends Q1\n"
                    "Processing: Analyzing data...\n"
                    "Result: 3 insights found\n"
                    "Anomaly: Feb revenue -15%"
                ),
                "bg_color": "#1b1b2d",
            },
        ],
    },
    {
        "name": "hiring_culture",
        "files": [
            {
                "rel_path": "notes/hiring_plan_q2.txt",
                "description": (
                    "Q2 hiring plan: 6 open roles, $1.2M budget, "
                    "remote-first policy, diversity hiring targets"
                ),
                "content": (
                    "Q2 2025 Hiring Plan\n"
                    "Date: 2025-03-17\n"
                    "Budget: $1.2M\n\n"
                    "Open roles:\n"
                    "1. Senior Backend Engineer (Remote)\n"
                    "2. ML Engineer — Insights AI team (Remote)\n"
                    "3. Product Designer (Hybrid — SF)\n"
                    "4. DevOps Engineer (Remote)\n"
                    "5. Customer Success Manager (Remote)\n"
                    "6. Technical Writer (Remote)\n\n"
                    "Targets: 40% underrepresented candidates in pipeline.\n"
                    "Offer acceptance goal: 80%.\n"
                    "Policy: Remote-first, async communication, quarterly "
                    "on-sites.\n"
                ),
                "bg_color": "#2d2d1b",
            },
            {
                "rel_path": "notes/team_retrospective.txt",
                "description": (
                    "Sprint retrospective notes: burnout concerns, on-call "
                    "rotation improvements, team morale and process changes"
                ),
                "content": (
                    "Team Retrospective — Sprint 24\n"
                    "Date: 2025-03-14\n"
                    "Facilitator: Maya (Engineering Manager)\n\n"
                    "What went well:\n"
                    "- Shipped Insights AI beta on time\n"
                    "- New hire onboarding process improved\n"
                    "- Cross-team collaboration on security incident\n\n"
                    "Concerns:\n"
                    "- Burnout risk: 3 engineers flagged high workload\n"
                    "- On-call rotation needs rebalancing (2 people overloaded)\n"
                    "- Meeting fatigue — too many syncs\n\n"
                    "Actions:\n"
                    "- Redistribute on-call shifts next sprint\n"
                    "- Implement no-meeting Wednesdays\n"
                    "- Manager 1:1s to check in on burnout\n"
                ),
                "bg_color": "#2d2d1b",
            },
            {
                "rel_path": "images/team_growth_chart.png",
                "description": (
                    "Team growth chart showing headcount 28 to 45, "
                    "78% offer acceptance rate, hiring pipeline metrics"
                ),
                "content": (
                    "TEAM GROWTH — 2025\n\n"
                    "Headcount: 28 -> 45 (target)\n"
                    "Offer Acceptance: 78%\n"
                    "Open Roles: 6\n\n"
                    "Pipeline: 142 candidates\n"
                    "Diversity: 38% URG in pipeline"
                ),
                "bg_color": "#2d2d1b",
            },
            {
                "rel_path": "pdfs/employee_handbook.pdf",
                "description": (
                    "Employee handbook covering remote-first policy, equity "
                    "compensation, diversity principles, and benefits"
                ),
                "content": (
                    "Acme Analytics Employee Handbook. Our company operates on "
                    "a remote-first model with quarterly on-site gatherings. All "
                    "full-time employees receive equity compensation as part of "
                    "their package. We are committed to building a diverse and "
                    "inclusive workplace with a target of 40% underrepresented "
                    "groups in our hiring pipeline. Benefits include unlimited "
                    "PTO, home office stipend, learning budget, and mental health "
                    "support. Our core values: transparency, ownership, empathy, "
                    "and continuous learning."
                ),
                "bg_color": "#2d2d1b",
            },
            {
                "rel_path": "audio/culture_interview.mp3",
                "description": (
                    "Engineering manager interview discussing company culture, "
                    "remote work perks, team dynamics, and hiring philosophy"
                ),
                "content": (
                    "So what makes Acme Analytics special as a workplace? I'd "
                    "say it's the combination of remote-first flexibility with "
                    "genuine team connection. We do quarterly on-sites where the "
                    "whole engineering team gets together, and those are really "
                    "valuable for building relationships. We also invest heavily "
                    "in our hiring process to ensure culture fit and diversity. "
                    "Every engineer gets a learning budget and dedicated time for "
                    "professional development. The on-call rotation is fair and "
                    "we actively monitor for burnout."
                ),
                "bg_color": "#2d2d1b",
            },
            {
                "rel_path": "video/office_tour.mp4",
                "description": (
                    "Virtual office tour showcasing engineering hub, "
                    "collaboration spaces, and 'we're hiring' message"
                ),
                "content": (
                    "Virtual Office Tour\n\n"
                    "Engineering Hub: 28 engineers\n"
                    "Remote-First Culture\n"
                    "Quarterly On-Sites\n\n"
                    "We're Hiring! 6 Open Roles"
                ),
                "bg_color": "#2d2d1b",
            },
        ],
    },
]


# ---------------------------------------------------------------------------
# Generic themed file creators
# ---------------------------------------------------------------------------
def _create_themed_text(rel_path: str, content: str) -> None:
    """Create a plain text file at DATA_DIR / rel_path."""
    path = DATA_DIR / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def _create_themed_image(
    rel_path: str, slide_text: str, bg_color: str = "#1a1a2e"
) -> None:
    """Create a PNG slide image with multiline text."""
    from PIL import Image, ImageDraw, ImageFont

    path = DATA_DIR / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)

    img = Image.new("RGB", (800, 450), bg_color)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("Arial", 28)
    except OSError:
        font = ImageFont.load_default()
    draw.multiline_text((40, 40), slide_text, fill="white", font=font, spacing=12)
    img.save(path)


def _create_themed_pdf(rel_path: str, title: str, body: str) -> None:
    """Create a single-page PDF with a title and body text."""
    from fpdf import FPDF

    path = DATA_DIR / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 12, title, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_font("Helvetica", "", 12)
    pdf.multi_cell(0, 7, body)
    pdf.output(str(path))


def _create_themed_audio(rel_path: str, speech_text: str) -> None:
    """Create an MP3 file from text using gTTS."""
    from gtts import gTTS

    path = DATA_DIR / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)

    tts = gTTS(text=speech_text, lang="en")
    tts.save(str(path))


def _create_themed_video(
    rel_path: str, lines: list[str], bg_color: str = "#0f0f23"
) -> None:
    """Create a short MP4 with a text reveal animation."""
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont

    path = DATA_DIR / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)

    try:
        font = ImageFont.truetype("Arial", 26)
    except OSError:
        font = ImageFont.load_default()

    frames: list[np.ndarray] = []
    total_frames = 60
    for frame_idx in range(total_frames):
        img = Image.new("RGB", (800, 448), bg_color)
        draw = ImageDraw.Draw(img)
        visible_lines = int(len(lines) * min(frame_idx / (total_frames * 0.7), 1.0))
        for i, line in enumerate(lines[: visible_lines + 1]):
            draw.text((40, 40 + i * 40), line, fill="white", font=font)
        frames.append(np.array(img))

    import imageio.v3 as iio

    iio.imwrite(str(path), np.stack(frames), fps=30)


# ---------------------------------------------------------------------------
# Text notes (default mode)
# ---------------------------------------------------------------------------
def create_text_files() -> None:
    notes_dir = DATA_DIR / "notes"
    notes_dir.mkdir(parents=True, exist_ok=True)

    (notes_dir / "customer_complaint.txt").write_text(
        "Subject: Pricing complaint from Globex Corp\n"
        "Date: 2025-03-10\n\n"
        "Globex Corp (our largest enterprise customer) reached out to complain\n"
        "about the 40% price increase on the Analytics Pro plan. They say the\n"
        "new pricing was communicated too late and doesn't reflect the value\n"
        "they receive. They are evaluating competitor offerings and may churn\n"
        "if we don't offer a discount or grandfather their current rate.\n"
    )

    (notes_dir / "meeting_notes.txt").write_text(
        "Meeting Notes — Pricing Review (2025-03-12)\n"
        "Attendees: Sarah (PM), James (Sales), Priya (Finance)\n\n"
        "Key decisions:\n"
        "1. Offer Globex a 12-month rate lock at the old price.\n"
        "2. Introduce a new 'Enterprise Legacy' tier for long-term customers.\n"
        "3. Publish a pricing FAQ on the help center by end of week.\n"
        "4. Schedule a call with Globex's VP of Engineering for Thursday.\n"
    )

    (notes_dir / "product_roadmap.txt").write_text(
        "Acme Analytics — Q2 2025 Roadmap\n\n"
        "Planned features:\n"
        "- Real-time dashboard alerts (P0)\n"
        "- Custom report builder (P1)\n"
        "- SSO / SAML integration (P1)\n"
        "- Multimodal data ingestion API (P2)\n"
        "- Mobile companion app (P2)\n\n"
        "Goal: reduce churn by 15% through feature differentiation.\n"
    )
    print(f"  Created {len(list(notes_dir.iterdir()))} text files in {notes_dir}")


# ---------------------------------------------------------------------------
# Images (PNG via Pillow) — default mode
# ---------------------------------------------------------------------------
def create_images() -> None:
    from PIL import Image, ImageDraw, ImageFont

    images_dir = DATA_DIR / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    def _draw_slide(text: str, filename: str, bg: str = "#1a1a2e") -> None:
        img = Image.new("RGB", (800, 450), bg)
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("Arial", 28)
        except OSError:
            font = ImageFont.load_default()
        draw.multiline_text((40, 40), text, fill="white", font=font, spacing=12)
        img.save(images_dir / filename)

    _draw_slide(
        "ACME ANALYTICS\nPricing Update — March 2025\n\n"
        "Analytics Pro: $99/mo  ->  $139/mo (+40%)\n"
        "Enterprise:    $249/mo ->  $349/mo (+40%)\n\n"
        "Effective April 1, 2025",
        "pricing_slide.png",
    )

    _draw_slide(
        "SUPPORT TICKET #4281\n\n"
        "Customer: Globex Corp\nStatus: ESCALATED\n\n"
        '"We were not informed about the price\n'
        " change until the invoice arrived.\n"
        ' This is unacceptable."',
        "support_ticket_screenshot.png",
        bg="#2d1b1b",
    )
    print(f"  Created {len(list(images_dir.iterdir()))} images in {images_dir}")


# ---------------------------------------------------------------------------
# PDF (via fpdf2) — default mode
# ---------------------------------------------------------------------------
def create_pdfs() -> None:
    from fpdf import FPDF

    pdfs_dir = DATA_DIR / "pdfs"
    pdfs_dir.mkdir(parents=True, exist_ok=True)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(
        0,
        12,
        "Acme Analytics - Pricing Policy Update",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.ln(4)
    pdf.set_font("Helvetica", "", 12)
    body = (
        "Effective April 1, 2025, Acme Analytics will adjust pricing across all "
        "subscription tiers. The Analytics Pro plan increases from $99/month to "
        "$139/month. The Enterprise plan increases from $249/month to $349/month.\n\n"
        "Rationale: infrastructure costs have risen 35% year-over-year due to "
        "increased compute requirements for real-time analytics processing. The "
        "new pricing reflects the true cost of delivering enterprise-grade uptime "
        "and performance guarantees.\n\n"
        "Existing customers on annual contracts will retain their current rate "
        "until renewal. Monthly subscribers will see the new rate on their next "
        "billing cycle.\n\n"
        "For questions, contact billing@acme-analytics.example.com."
    )
    pdf.multi_cell(0, 7, body)
    pdf.output(str(pdfs_dir / "pricing_policy.pdf"))
    print(f"  Created 1 PDF in {pdfs_dir}")


# ---------------------------------------------------------------------------
# Audio (MP3 via gTTS) — default mode
# ---------------------------------------------------------------------------
def create_audio() -> None:
    from gtts import gTTS

    audio_dir = DATA_DIR / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)

    text = (
        "Hi, this is David from Globex Corp. I'm calling about our Acme Analytics "
        "subscription. We just received an invoice showing a forty percent increase. "
        "Nobody told us about this in advance. We've been a customer for three years "
        "and this feels like a bait-and-switch. Please have someone from your team "
        "call me back today to discuss options, "
        "or we will start evaluating alternatives."
    )
    tts = gTTS(text=text, lang="en")
    tts.save(str(audio_dir / "customer_call.mp3"))
    print(f"  Created 1 audio file in {audio_dir}")


# ---------------------------------------------------------------------------
# Video (MP4 via imageio) — default mode
# ---------------------------------------------------------------------------
def create_video() -> None:
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont

    video_dir = DATA_DIR / "video"
    video_dir.mkdir(parents=True, exist_ok=True)

    frames: list[np.ndarray] = []
    lines = [
        "Acme Analytics — Dashboard Demo",
        "",
        "Revenue: $1.2M  (+18% YoY)",
        "Active Users: 14,200",
        "Churn Rate: 4.7%  (target < 3%)",
        "",
        "Alert: 3 enterprise accounts",
        "flagged for churn risk.",
    ]

    try:
        font = ImageFont.truetype("Arial", 26)
    except OSError:
        font = ImageFont.load_default()

    # Generate 60 frames (2 seconds at 30 fps) with a simple reveal animation
    total_frames = 60
    for frame_idx in range(total_frames):
        img = Image.new("RGB", (800, 448), "#0f0f23")
        draw = ImageDraw.Draw(img)
        visible_lines = int(len(lines) * min(frame_idx / (total_frames * 0.7), 1.0))
        for i, line in enumerate(lines[: visible_lines + 1]):
            draw.text((40, 40 + i * 40), line, fill="white", font=font)
        frames.append(np.array(img))

    import imageio.v3 as iio

    output_path = str(video_dir / "dashboard_demo.mp4")
    iio.imwrite(output_path, np.stack(frames), fps=30)
    print(f"  Created 1 video file in {video_dir}")


# ---------------------------------------------------------------------------
# Manifest
# ---------------------------------------------------------------------------
def _get_base_manifest() -> dict[str, str]:
    """Return the manifest entries for the default 8-file dataset."""
    return {
        "notes/customer_complaint.txt": (
            "Customer complaint from Globex Corp about a 40% price increase, "
            "mentions potential churn"
        ),
        "notes/meeting_notes.txt": (
            "Internal meeting notes from the pricing review discussing rate "
            "locks and an Enterprise Legacy tier"
        ),
        "notes/product_roadmap.txt": (
            "Q2 2025 product roadmap with planned features and a goal to "
            "reduce churn by 15%"
        ),
        "images/pricing_slide.png": (
            "Slide showing pricing update: Analytics Pro $99 to $139, "
            "Enterprise $249 to $349, both +40%"
        ),
        "images/support_ticket_screenshot.png": (
            "Escalated support ticket #4281 from Globex Corp complaining "
            "about surprise price change"
        ),
        "pdfs/pricing_policy.pdf": (
            "Official pricing policy detailing the April 2025 price increase "
            "and rationale"
        ),
        "audio/customer_call.mp3": (
            "Voice recording of David from Globex Corp calling about the "
            "40% invoice increase"
        ),
        "video/dashboard_demo.mp4": (
            "Dashboard demo showing Revenue $1.2M, Active Users 14,200, "
            "Churn Rate 4.7% (target < 3%), 3 accounts flagged for churn risk"
        ),
    }


def create_manifest() -> None:
    """Write the default manifest (8 entries)."""
    manifest = _get_base_manifest()
    manifest_path = Path("manifest.json")
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"  Created {manifest_path}")


# ---------------------------------------------------------------------------
# Advanced mode: generate themed files across 4 extra themes
# ---------------------------------------------------------------------------
def create_advanced_files() -> dict[str, str]:
    """Generate all themed files and return their manifest entries."""
    manifest_entries: dict[str, str] = {}
    total = 0

    for theme in ADVANCED_THEMES:
        theme_name = theme["name"]
        print(f"\n  [{theme_name}]")

        for tf in theme["files"]:
            rel_path = tf["rel_path"]
            content = tf["content"]
            bg_color = tf["bg_color"]

            if rel_path.startswith("notes/"):
                _create_themed_text(rel_path, content)

            elif rel_path.startswith("images/"):
                _create_themed_image(rel_path, content, bg_color)

            elif rel_path.startswith("pdfs/"):
                # Extract title from first line of content
                title = content.split(".")[0]
                _create_themed_pdf(rel_path, title, content)

            elif rel_path.startswith("audio/"):
                _create_themed_audio(rel_path, content)

            elif rel_path.startswith("video/"):
                video_lines = content.split("\n")
                _create_themed_video(rel_path, video_lines, bg_color)

            manifest_entries[rel_path] = tf["description"]
            total += 1
            print(f"    {rel_path}")

    print(f"\n  Created {total} themed files across {len(ADVANCED_THEMES)} themes")
    return manifest_entries


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate sample dataset for the omnimodal agent memory demo."
    )
    parser.add_argument(
        "--advanced",
        action="store_true",
        help=(
            "Generate 32 files across 5 semantic themes (instead of 8) "
            "for richer t-SNE clustering."
        ),
    )
    args = parser.parse_args()

    print("Generating sample dataset...\n")

    print("[1/6] Text notes")
    create_text_files()

    print("[2/6] Images")
    create_images()

    print("[3/6] PDFs")
    create_pdfs()

    print("[4/6] Audio")
    create_audio()

    print("[5/6] Video")
    create_video()

    if args.advanced:
        print("\n[+] Advanced mode: generating themed files...")
        advanced_entries = create_advanced_files()

        print("\n[6/6] Manifest (merged)")
        manifest = _get_base_manifest()
        manifest.update(advanced_entries)
        manifest_path = Path("manifest.json")
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
        print(f"  Created {manifest_path} ({len(manifest)} entries)")
    else:
        print("[6/6] Manifest")
        create_manifest()

    print(f"\nDone! Sample data is in ./{DATA_DIR}/")


if __name__ == "__main__":
    main()
