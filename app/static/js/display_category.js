window.addEventListener('load', (event) => {
    displayChannels();
    // displayVideos();
})

var num_channels_display = 10;
var num_videos_display = 10

function removeAllChildNodes(parent) {
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }
}

function increaseDisplayedChannels(){
    num_channels_display += 10;
    displayChannels();
};

function displayChannels(){

    var channelsDisplay = document.getElementById("channel_display_list");

    // Remove all children so as to not have duplicate channels displayed
    removeAllChildNodes(channelsDisplay)

    // Get the amount of channels to display
    channels_to_display = channels.slice(0,num_channels_display);
    for (let i=0; i<channels_to_display.length;i++){
        var channel = channels[i];

        var channel_item = document.createElement("li");
        channel_item.className = "nav-item";

        var channel_link = document.createElement("a");
        channel_link.className = "nav-link";
        channel_link.setAttribute("href", `/channel/${channel.name}`);
        channel_link.style.cssText = "width: 100% !important";

        var channel_name = document.createElement("span")
        channel_name.innerHTML = `${channel.name}`

        var channel_img = document.createElement("img")
        channel_link.className = "channel_logo";
        channel_img.setAttribute("src", `${channel.logo_url}`);
        channel_img.style.cssText = "width: 40px;";

        channel_link.appendChild(channel_img);
        channel_link.appendChild(channel_name);
        channel_item.appendChild(channel_link);
        channelsDisplay.appendChild(channel_item);

    };
    var load_more_button = document.createElement("button");
    load_more_button.innerText = "Load more...";
    load_more_button.setAttribute("id", "load_more_channels_button");
    load_more_button.setAttribute("onclick", "increaseDisplayedChannels()");

    channelsDisplay.appendChild(load_more_button);    
};


function increaseDisplayedVideos(){
    num_videos_display += 10;
    displayVideos();
};

function displayVideos(){

    var videosDisplay = document.getElementById("video_display_list");

    // Remove all children so as to not have duplicate channels displayed
    removeAllChildNodes(videosDisplay)

    // Get the amount of channels to display
    videos_to_display = videos.slice(0,num_videos_display);
    for (let i=0; i<videos_to_display.length;i++){
        // <a href="/video/{{ vid.id }}"><img src="https://i.ytimg.com/vi/{{ vid.id }}/default.jpg" class="video_list_thumb"></a>
        var vid = videos[i];

        var video_link = document.createElement("a");
        video_link.setAttribute("href", `/video/${vid.id}`);
        video_link.style.cssText = "";

        var video_img = document.createElement("img")
        video_img.className = "video_list_thumb";
        video_img.setAttribute("src", `https://i.ytimg.com/vi/${vid.id}/default.jpg`);
        video_img.style.cssText = "";

        videosDisplay.appendChild(video_img);
        videosDisplay.appendChild(video_link);

    };
    var load_more_button = document.createElement("button");
    load_more_button.innerText = "Load more...";
    load_more_button.setAttribute("id", "load_more_vids_button");
    load_more_button.setAttribute("onclick", "increaseDisplayedVideos()");

    videosDisplay.appendChild(load_more_button);    
};