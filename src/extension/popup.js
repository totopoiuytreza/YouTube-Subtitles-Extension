// Define a listener for the popup DOM content to be loaded
window.addEventListener("DOMContentLoaded", () => {

    // Get the input element from the popup
    const input = document.getElementById("lang-select");
  
    // Get the currently active tab
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      const activeTab = tabs[0];
  
      // Create a message to send to the background script containing the input value, the code editor value and the active tab ID
      const message = {
        type: "executeCode",
        inputValue: input.value,
        tabId: activeTab.id
      };
  
      // Send the message to the background script
      chrome.runtime.sendMessage(message);
  
    });
  });
  