
// When a new tab is created, check if it is a youtube video page
chrome.tabs.onUpdadated.addListener((tabId, tab) => {
    if(tab.url && tab.url.includes('youtube.com/watch')) {
        // Send the current url to the content script
        chrome.tabs.sendMessage(tabId, {
            type : 'NEW_URL',
            url: tab.url
        })
    }
})