window.onload = function(){
    displayChannels();
};

var num_channels_display = 5;

function removeAllChildNodes(parent) {
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }
}

function increaseDisplayedChannels(){
    num_channels_display += 5;
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
    load_more_button.setAttribute("id", "load_more_button");
    load_more_button.setAttribute("onclick", "increaseDisplayedChannels()");
    channelsDisplay.appendChild(load_more_button);    
};

// document.getElementById("load_more_button").onclick = increaseDisplayedChannels;