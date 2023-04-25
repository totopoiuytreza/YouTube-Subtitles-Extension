(() => {
    
    let youtubeLeftControls, youtubePlayer;
    let currentVideo = null;
    
    chrome.runtime.onMessage.addListener((msg) => {
        if (msg.type === 'NEW_URL') {
            currentVideo = msg.videoId;
            loadNewVideo();
        }
    });
    var socket = io.connect('http://127.0.0.1:5000');

    socket.on('connect', function() {
        console.log('connected');
    });

    socket.on('transcribe', function(msg) {
        console.log(msg.text);
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
