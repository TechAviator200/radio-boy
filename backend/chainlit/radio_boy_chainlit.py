import chainlit as cl

# Your animation served from /public
VIDEO_URL = "/public/animation.mp4"


def build_card_html(history):
    """
    Build the Apple Music-style Radio Boy card as raw HTML.
    `history` is a list of (speaker, text) tuples.
    """
    # Build the conversation text
    if not history:
        convo_text = "Type a vibe below and I'll riff back inside this card."
    else:
        lines = []
        for speaker, text in history:
            label = "You" if speaker == "user" else "Radio Boy"
            lines.append(f"{label}: {text}")
        convo_text = "<br><br>".join(lines)

    card_html = f"""
    <div style="
        background:#1c1c1e;
        border-radius:24px;
        overflow:hidden;
        border:1px solid #3a3a3c;
        box-shadow:0 20px 40px rgba(0,0,0,0.45);
        width:100%;
        max-width:420px;
        margin:16px auto;
        color:#fff;
        font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
    ">
        <!-- Header animation -->
        <div style="width:100%;aspect-ratio:1/1;background:#000;">
            <video
                src="{VIDEO_URL}"
                autoplay
                loop
                muted
                playsinline
                style="width:100%;height:100%;object-fit:cover;display:block;"
            ></video>
        </div>

        <!-- Text + convo -->
        <div style="padding:20px;">
            <div style="font-size:22px;font-weight:700;margin-bottom:4px;color:#ffffff;">
                Radio Boy
            </div>
            <div style="font-size:14px;color:#ff2d55;margin-bottom:14px;">
                I hear a vibe – let's build it out.
            </div>

            <div style="font-size:15px;line-height:1.6;color:#d1d1d6;">
                {convo_text}
            </div>
        </div>
    </div>
    """
    return card_html


@cl.on_chat_start
async def start():
    """Runs once when the chat opens."""
    cl.user_session.set("history", [])
    html = build_card_html([])
    await cl.Message(content=html).send()


@cl.on_message
async def main(message: cl.Message):
    """Runs every time you send a message."""
    text = message.content.strip()

    # Get prior convo
    history = cl.user_session.get("history", [])

    # Add user line
    history.append(("user", text))

    # Simple Radio Boy reply for now
    rb_reply = f"I hear a vibe like: {text} – want it smoother or more turn-up?"
    history.append(("radio", rb_reply))

    # Save updated convo
    cl.user_session.set("history", history)

    # Rebuild the card with full convo inside
    card_html = build_card_html(history)
    await cl.Message(content=card_html).send()
