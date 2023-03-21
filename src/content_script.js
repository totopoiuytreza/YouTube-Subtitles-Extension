(() => {
    let youtubeLeftControls, youtubePlayer;
    let currentVideo = null;
    

    chrome.runtime.onMessage.addListener((obj, sender, sendResponse) => {
        const { type, url, tabId } = obj;
        if(type === 'NEW_URL') {
            currentVideo = url;
            loadNewVideo();
        }
    });

    const loadNewVideo = () => {
        fetch('/transcribe', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                url: currentVideo
            })
        })
        .then(response => response.text())
        .then(text => {
            // Do something with the transcribed text
            console.log(text);
        })
        .catch(error => {
            console.error(error);
        });
    }
})();