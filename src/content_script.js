(() => {
    let youtubeLeftControls, youtubePlayer;
    let currentVideo = null;
    

    chrome.runtime.onMessage.addListener((obj, sender, sendResponse) => {
        const { type, videoId, tabId } = obj;
        if(type === 'NEW_URL') {
            currentVideo = videoId;
            loadNewVideo();
        }
    });

    const loadNewVideo = () => {
        fetch('http://127.0.0.1:5000/transcribe', {
            method: 'POST',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                video_id: currentVideo
            })
        })
        .then(response => response.text())
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            console.error(error);
        });
    }
})();