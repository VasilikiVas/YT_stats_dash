function search_channels(){
    var input = document.getElementById("channel_searchbar");
    var input_str = input.value.toLowerCase();
    selected_channels = []

    // var display_counter = 0;

    for (let i=0; i<channels.length; i++){
        var channel = channels[i];
        // if (channel.name.substring(0, input_str.length) == input_str){
        //     selected_channels.push(channel);
        // }
        for (part of channel.name.split('-')) {
            if (part.substring(0, input_str.length) == input_str){
                selected_channels.push(channel);
                break
            }
        }
    };
    // Display the first selected N channels 
    var search_channels_to_display = selected_channels.slice(0,num_channels_display);
    displayChannels(search_channels_to_display);
};