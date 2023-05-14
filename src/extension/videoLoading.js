fetch('/get_video_id', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      'video_url': 'https://www.youtube.com/watch?v=YOUR_VIDEO_ID'
    })
  })
  .then(response => response.json())
  .then(data => {
    var videoId = data.video_id;
    var iframeUrl = "https://www.youtube.com/embed/" + videoId + "?cc_load_policy=1";
  
    var iframe = document.createElement("iframe");
    iframe.setAttribute("src", iframeUrl);
    iframe.setAttribute("width", "560");
    iframe.setAttribute("height", "315");
    iframe.setAttribute("frameborder", "0");
    iframe.setAttribute("allowfullscreen", "true");
  
    document.getElementById("player").appendChild(iframe);
  })
  .catch(error => console.error(error));