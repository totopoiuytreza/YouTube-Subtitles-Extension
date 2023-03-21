(() => {
    let youtubeLeftControls, youtubePlayer;
    let currentVideo = null;
    

    chrome.runtime.onMessage.addListener((obj, sender, sendResponse) => {
        const { type, url, tabId } = obj;
        console.log("POTATO")

        if(type === 'NEW_URL') {
            currentVideo = url;
        }
    });
})();