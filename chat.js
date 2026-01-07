// Get DOM elements
const chatMessages = document.getElementById('chatMessages');
const chatInput = document.getElementById('chatInput');

// Store pending redirect URL
let pendingRedirectUrl = null;

// BACKEND URL (Flask running on port 81)
const BACKEND_URL = "http://127.0.0.1:81/chat";

/**
 * Adds a message to the chat window
 * @param {string} text - The message text
 * @param {string} sender - Either 'user' or 'assistant'
 */
function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    messageDiv.textContent = text;
    chatMessages.appendChild(messageDiv);

    // Auto-scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

/**
 * Sends user message to backend
 * @param {string} message - The user's message
 */
async function sendMessage(message) {
    try {
        const response = await fetch(BACKEND_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // Display assistant's response
        addMessage(data.text, 'assistant');

        // Store redirect URL if present
        if (data.redirect_url) {
            pendingRedirectUrl = data.redirect_url;
        }

    } catch (error) {
        console.error('Error sending message:', error);
        addMessage('Sorry, there was an error processing your message.', 'assistant');
    }
}

/**
 * Checks if user message is a confirmation for redirect
 * @param {string} message - The user's message
 * @returns {boolean} - True if message is a redirect confirmation
 */
function isRedirectConfirmation(message) {
    const lowerMessage = message.toLowerCase().trim();
    return (
        lowerMessage === 'yes' ||
        lowerMessage === 'open' ||
        lowerMessage === 'go ahead'
    );
}

/**
 * Opens the pending redirect URL in a new tab
 */
function handleRedirect() {
    if (pendingRedirectUrl) {
        window.open(pendingRedirectUrl, '_blank');
        pendingRedirectUrl = null;
        addMessage('Opening the page now. Let me know if you need anything else.', 'assistant');
    }
}

/**
 * Handles user input submission
 */
function handleUserInput() {
    const message = chatInput.value.trim();

    // Don't process empty messages
    if (!message) return;

    // Add user message to chat
    addMessage(message, 'user');

    // Clear input field
    chatInput.value = '';

    // Check if this is a redirect confirmation
    if (pendingRedirectUrl && isRedirectConfirmation(message)) {
        handleRedirect();
    } else {
        // Send message to backend
        sendMessage(message);
    }
}

// Event listener for Enter key press
chatInput.addEventListener('keypress', (event) => {
    if (event.key === 'Enter') {
        event.preventDefault();
        handleUserInput();
    }
});

// Initial system message
addMessage('System ready. Awaiting command.', 'assistant');

// Focus input field on page load
chatInput.focus();
