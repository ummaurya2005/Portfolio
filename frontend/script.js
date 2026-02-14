function toggleChat() {
    const chat = document.getElementById("chatContainer");
    chat.style.display = chat.style.display === "flex" ? "none" : "flex";
}

async function sendMessage() {
    const inputField = document.getElementById("message");
    const chatBox = document.getElementById("chat-box");

    const message = inputField.value.trim();
    if (!message) return;

    // User Bubble
    chatBox.innerHTML += `
        <div style="text-align:right; margin-bottom:8px;">
            <span style="background:#00ffb3; color:black; padding:6px 10px; border-radius:10px; display:inline-block;">
                ${message}
            </span>
        </div>
    `;

    inputField.value = "";

    const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: message })
    });

    const data = await response.json();

    // Bot Bubble
    chatBox.innerHTML += `
        <div style="text-align:left; margin-bottom:8px;">
            <span style="background:#1f2937; padding:6px 10px; border-radius:10px; display:inline-block;">
                ${data.reply}
            </span>
        </div>
    `;

    chatBox.scrollTop = chatBox.scrollHeight;
}
