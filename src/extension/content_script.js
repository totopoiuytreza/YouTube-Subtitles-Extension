(() => {
    
    let youtubeLeftControls, youtubePlayer;
    let currentVideo = null;
    let videoTranscripted = false;
    const transcribeController = new AbortController();
    const checkController = new AbortController();

    chrome.runtime.onMessage.addListener((msg) => {
        if (msg.type === 'NEW_URL' && msg.videoId !== currentVideo) {
            // Change previous video Id
            currentVideo = msg.videoId;

            // Abort all previous requests
            transcribeController.abort();
            checkController.abort();

            // Reset transcription status
            videoTranscripted = false;

            // Start transcription
            setInterval(checkTranscription, 5000);
            transcribing()
        }
        else if (msg.type === 'NOT_NEW_URL') {
            // Abort all previous requests
            transcribeController.abort();
            checkController.abort();

            // Reset transcription status
            videoTranscripted = false;
        }
    });
    
    const transcribing = () => {
        fetch('http://127.0.0.1:5000/transcribe', {
            method: 'POST',
            mode: 'cors',
            signal: transcribeController.signal,
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
                signal: checkController.signal,
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
