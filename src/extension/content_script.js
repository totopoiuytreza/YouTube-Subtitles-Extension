(() => {
    
    let youtubeLeftControls, youtubePlayer;
    let currentVideo = null;
    let videoTranscripted = false;

    chrome.runtime.onMessage.addListener((msg) => {
        if (msg.type === 'NEW_URL') {
            currentVideo = msg.videoId;
            let videoTranscripted = false;
            setInterval(checkTranscription, 5000);
            transcribing()
            
        }
    });

    const transcribing = () => {
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
            videoTranscripted = true;
            console.log(data);
        })
        .catch(error => {
            console.error(error);
        });
    }

    const checkTranscription = () => {
        if (!videoTranscripted) {
            fetch('http://127.0.0.1:5000/check_transcription',  {
                method: 'GET',
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.text())
            .then(data => {
                console.log(data);
            })
            .catch(error => {
                console.error(error);
            });
        }
        else {
            clearInterval(checkTranscription);
        }
    }


})();
