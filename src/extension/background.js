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
    else{
        chrome.tabs.sendMessage(tabId, {
            type : 'NOT_NEW_URL'
        })
    }
})


