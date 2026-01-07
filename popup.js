document.getElementById("ask").addEventListener("click", () => {
  const query = document.getElementById("query").value;

  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    chrome.tabs.sendMessage(
      tabs[0].id,
      { userQuery: query },
      (response) => {
        document.getElementById("response").innerText = response.reply;
      }
    );
  });
});
