console.log("AI Navigation Assistant loaded");

function getVisibleTools() {
  const elements = Array.from(
    document.querySelectorAll(
      "a, button, [role='menuitem'], [role='button'], li"
    )
  );

  return elements
    .map(el => ({
      text: el.innerText.trim(),
      element: el
    }))
    .filter(item => item.text.length > 0);
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  const userQuery = request.userQuery.toLowerCase();

  const tools = getVisibleTools();

  // If nothing is visible yet
  if (tools.length === 0) {
    sendResponse({
      reply: "I can’t see navigation tools yet. Please open the main menu and try again."
    });
    return;
  }

  // Try to match user intent to tool list
  const queryWords = userQuery.split(" ");

  let bestMatch = null;

  for (let tool of tools) {
    const toolText = tool.text.toLowerCase();
    for (let word of queryWords) {
      if (toolText.includes(word)) {
        bestMatch = tool;
        break;
      }
    }
    if (bestMatch) break;
  }

  // Respond
  if (bestMatch) {
    sendResponse({
      reply: `Click "${bestMatch.text}"`
    });
  } else {
    sendResponse({
      reply:
        "I can see these tools: " +
        tools.slice(0, 6).map(t => t.text).join(", ") +
        ". Please tell me which one you want."
    });
  }
});
