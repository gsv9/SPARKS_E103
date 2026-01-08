const chatMessages = document.getElementById("chatMessages");
const chatInput = document.getElementById("chatInput");

let pendingRedirectUrl = null;

function addMessage(text, sender) {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${sender}`;
    messageDiv.textContent = text;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function sendMessage(message) {
    try {
        const response = await fetch("http://127.0.0.1:81/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message })
        });

        const data = await response.json();

        addMessage(data.text, "assistant");

        // Backend explicitly tells when to redirect
        if (data.redirect_url) {
            pendingRedirectUrl = data.redirect_url;
        }
    } catch (err) {
        console.error(err);
        addMessage("Backend not responding.", "assistant");
    }
}

function handleUserInput() {
    const message = chatInput.value.trim();
    if (!message) return;

    addMessage(message, "user");
    chatInput.value = "";

    // Redirect only after backend sends redirect_url
    if (
        pendingRedirectUrl &&
        ["yes", "open"].includes(message.toLowerCase())
    ) {
        window.open(pendingRedirectUrl, "_blank");
        pendingRedirectUrl = null;
        return;
    }

    sendMessage(message);
}

chatInput.addEventListener("keypress", event => {
    if (event.key === "Enter") {
        handleUserInput();
    }
});
// Focus input field on page load
chatInput.focus();
// Initial system message on page load
addMessage("System ready. Awaiting command.", "assistant");