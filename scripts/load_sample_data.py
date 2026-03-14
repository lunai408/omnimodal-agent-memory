#!/usr/bin/env python3
"""Generate a themed sample dataset for the omnimodal agent memory demo.

Theme: "Acme Analytics" — a fictional B2B SaaS company dealing with a
pricing complaint from a key customer.

Creates files in data/{notes,images,pdfs,audio,video}/.
"""

from pathlib import Path

DATA_DIR = Path("data")


# ---------------------------------------------------------------------------
# Text notes
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
# Images (PNG via Pillow)
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
# PDF (via fpdf2)
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
# Audio (MP3 via gTTS)
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
# Video (MP4 via imageio)
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
        img = Image.new("RGB", (800, 450), "#0f0f23")
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
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    print("Generating sample dataset...\n")

    print("[1/5] Text notes")
    create_text_files()

    print("[2/5] Images")
    create_images()

    print("[3/5] PDFs")
    create_pdfs()

    print("[4/5] Audio")
    create_audio()

    print("[5/5] Video")
    create_video()

    print(f"\nDone! Sample data is in ./{DATA_DIR}/")


if __name__ == "__main__":
    main()
