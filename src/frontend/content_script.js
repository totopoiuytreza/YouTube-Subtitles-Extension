(() => {
    let youtubeLeftControls, youtubePlayer;
    let currentVideo = null;
    let port;

    port = chrome.runtime.connect({name: "websocket"});
        port.onMessage.addListener((msg) => {
            console.log("RECEIVING")
            if (msg.type === 'transcribe') {
                console.log(msg.data.text);
            }
        });
        
    chrome.runtime.onMessage.addListener((msg) => {
        if (msg.type === 'NEW_URL') {
            currentVideo = msg.videoId;
            loadNewVideo();
        }
    });

    const loadNewVideo = () => {
        // Connect to the backend server using a named port
        
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
