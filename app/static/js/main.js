var subfile;

async function GetSub(thread_id) {
    return new Promise(function (resolve) {
        var xhr = new XMLHttpRequest();
        var num_id = parseInt(thread_id, 10);
        console.log("in check", thread_id);
        xhr.open('GET', '/whisperai/sub/' + num_id, true);
        xhr.onreadystatechange = function () {
            if (xhr.readyState == XMLHttpRequest.DONE) {
                //subfile = JSON.parse(xhr.responseText);
                var subtitleBlob = new Blob([xhr.responseText], { type: 'text/vtt' });
                var subtitleURL = URL.createObjectURL(subtitleBlob);
                subfile = subtitleURL
                // Set the subtitle track's src attribute
                var subtitleTrack = document.getElementById('subtitleTrack');
                subtitleTrack.src = subtitleURL;
                resolve(subtitleURL)
            };
        };
        xhr.send();
        srt_button = document.getElementById("srt_download");
        srt_button.style.display = "block";
    });
}

async function CheckProgress(thread_id) {
    return new Promise(function (resolve) {
        var xhr = new XMLHttpRequest();
        var num_id = parseInt(thread_id, 10);
        console.log("in check", thread_id);
        xhr.open('GET', '/whisperai/progress/' + num_id, true);
        xhr.onreadystatechange = function () {
            if (xhr.readyState == XMLHttpRequest.DONE) {
                var output_data = JSON.parse(xhr.responseText)
                resolve(output_data);
            };
        };
        xhr.send();
    });
}


async function SendAndGetId(video_file) {
    return new Promise(function (resolve, reject) {
        var xhr = new XMLHttpRequest();

        xhr.open('POST', '/whisperai', true);
        xhr.onreadystatechange = function () {
            if (xhr.readyState == XMLHttpRequest.DONE) {
                console.log(xhr.responseText);
                resolve(xhr.responseText);
            };

        };
        //xhr.setRequestHeader("Content-Type", "multipart/form-data");

        // We create a FormData object and add the selected file
        const formData = new FormData();
        formData.append("file", video_file);
        // We send the request to the server with the send() method
        xhr.send(formData);
    });
}


// Example: Toggle waves when a button is clicked

document.getElementById("input").addEventListener("change", async function () {
    var waveContainer = document.getElementById("waveContainer");
    var thread_id = await SendAndGetId(this.files[0]);
    waveContainer.style.display = "flex";
    var media = URL.createObjectURL(this.files[0]);
    var video = document.getElementById("video");
    var output_show = document.getElementById("live_text");

    video.src = media;
    var intervalId = setInterval(async function () {
        var data = await CheckProgress(thread_id);
        output_show.innerText = data.output_text;
        console.log(data.status);
        if (data.status === true) {
            console.log("exit");
            var deum = await GetSub(thread_id);
            video.style.display = "block";
            video.play();
            waveContainer.style.display = "none";

            clearInterval(intervalId); // Stop the interval if the condition is met
        }
    }, 2 * 1000);

});

document.getElementById("srt_download").addEventListener("click", async function () {
    var link = document.createElement("a");
    link.download = "subs.vtt";
    console.log(subfile);
    link.href = subfile;
    link.click();
});
