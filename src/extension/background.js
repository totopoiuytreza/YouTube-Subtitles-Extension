chrome.tabs.onUpdated.addListener((tabId, tab) => {
    if(tab.url && tab.url.includes('youtube.com/watch')) {
        const queryParameters = tab.url.split("?")[1];
        const urlParameters = new URLSearchParams(queryParameters);
        // Send the current url to the content script
        chrome.tabs.sendMessage(tabId, {
            type : 'NEW_URL',
            videoId: urlParameters.get('v'),
        })
    }
})


import WebSocket from 'ws';
const ws = new WebSocket('ws://127.0.0.1:5000');

ws.addEventListener('open', (event) => {
    console.log('WebSocket connection opened');
  });
  
ws.addEventListener('message', (event) => {
    const data = JSON.parse(event.data);
    if (data.type === 'transcribe') {
      console.log('Received transcribe event from server:', data.text);
    } else {
      console.log('Received message from server:', data.text);
    }
  });

