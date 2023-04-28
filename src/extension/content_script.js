(() => {
    
    let youtubeLeftControls, youtubePlayer;
    let currentVideo = null;
    let language_to_transcribe = "english";
    let videoTranscripted = false;
    let currentInterval = null;
    let transcribeController = null;
    

    chrome.runtime.onMessage.addListener((msg) => {
        console.log("Connected to :", msg);
        if (msg.type == 'NEW_URL') {
            if(currentVideo != msg.videoId) {
                // Abort all previous requests
                console.log("Aborting previous requests")
                if (transcribeController != null){
                    transcribeController.abort();
                }
            }
            // Change previous video Id
            currentVideo = msg.videoId;

            // Reset transcription status
            videoTranscripted = false;

            // Start transcription
            console.log("Transcribing video: ", currentVideo)
            currentInterval = setInterval(checkTranscription, 5000);
            transcribeController = transcribing()
        }
    });
    
    const transcribing = () => {
        transcribeController = new AbortController();
        fetch('http://127.0.0.1:5000/transcribe', {
            method: 'POST',
            mode: 'cors',
            signal: transcribeController.signal,
            headers: {
                'Content-Type': 'application/json'
                },
            body: JSON.stringify({
                video_id: currentVideo,
                language : language_to_transcribe

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

        return transcribeController;
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
            clearInterval(currentInterval);
            videoTranscripted = false;
        }
    }

        // Define the content script
    chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
        if (message === "addContent") {
        // Find the element to inject content into
        const targetElement = document.querySelector("#content");
    
        // Create a new element with your custom content
        const newElement = document.createElement("div");
        newElement.innerHTML = "<h1>F*** YouTube!</h1><p>This is some edgy content added by your extension.</p><img src='https://i.imgur.com/TjFgTtN.gif' alt='edgy image' />";
    
        // Add the new element to the target element
        targetElement.appendChild(newElement);
        }
    });

    chrome.scripting.executeScript({
        target: {tabId: tabId},
        function: () => {
          // Create a button
          const button = document.createElement('button');
          button.textContent = 'My Button';
      
          // Add an event listener to the button
          button.addEventListener('click', () => {
            // Call the YouTube API
            const player = document.querySelector('.video-stream');
            player.pauseVideo();
          });
      
          // Add the button to the video player
          const container = document.querySelector('.ytp-right-controls');
          container.insertBefore(button, container.firstChild);
        }
      });
       
})();
