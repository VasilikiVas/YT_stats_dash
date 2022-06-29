function construct_tooltip_video(info, incl_dev=false) {
    if (incl_dev) {
        deviation = `
           <tr>
              <td>deviation: </td>
              <td class="h5 mb-0 font-weight-bold text-gray-800">${info["deviation"].toFixed(3)}</td>
           </tr>
        `
    } else {deviation = '' }
   return `
   <div id="video_tooltip">

      <div class="vid_entry">
         <img class="thumbnail" src="${info["thumbnail_url"]}">
         <span class="ml-1 video_title">${info["title"]}</span>
      </div>
      <table>
            ${deviation}
            <tr>
               <td>views: </td>
               <td class="h5 mb-0 font-weight-bold text-gray-800">${formatter(info["views"])}</td>
            </tr>
            <tr>
               <td>channel: </td>
               <td class="h5 mb-0 font-weight-bold text-gray-800">${info["channel"]}</td>
            </tr>
      </table>
   </div>`
}

function construct_tooltip_channel(info, incl_std=false) {
   if (incl_std) {
      std = `
         <tr>
            <td>std: </td>
            <td class="h5 mb-0 font-weight-bold text-gray-800">${info["std"].toFixed(3)}</td>
         </tr>
      `
   } else { std = '' }
   return `
   <div>
      <a class="channel_entry nav-link">
            <img src="${info["logo_url"]}" class="channel_logo">
            <span class="ml-1 h5 font-weight-bold text-gray-800">${info["name"]}</span>
      </a>
      <table>
            ${std}
            <tr>
               <td>subs: </td>
               <td class="h5 mb-0 font-weight-bold text-gray-800">${formatter(info["subs"])}</td>
            </tr>
            <tr>
               <td>avg views: </td>
               <td class="h5 mb-0 font-weight-bold text-gray-800">${formatter(info["avg_views"])}</td>
            </tr>
      </table>
   </div>`
}

function construct_effectiveness_tooltip(d, subview_mode, view, cname) {
   let url = `/get_${subview_mode}_tooltip_data?${view}=${cname}&group=${d.group}`
   fetch(url)
       .then(function(response) { return response.json() })
       .then( function(vids) {
           div = document.getElementById("tooltip_vids")
           vids.forEach((vid)=>{
               html = `
                   <li class="vid_entry">
                       <img class="thumbnail" src="https://i.ytimg.com/vi/${vid.id}/hqdefault.jpg">
                       <span class="ml-1">
                           <table>
                               <tr><td class="video_title">${vid.title}</td></tr>
                               <tr><td class="video_info_small">views: ${formatter(vid.views)}</td></tr>
                               <tr><td class="video_info_small">channel: ${vid.channel}</td></tr>
                           </table>
                       </span>
                   </li>
               `
               div.innerHTML += html
           })
   })
   let html = `
       <table>
           <tr>
               <td>count: </td>
               <td class="h5 mb-0 font-weight-bold text-gray-800 cat_info">
                   ${formatter(d.count)}
               </td>
           </tr>
           <tr>
               <td>avg views: </td>
               <td class="h5 mb-0 font-weight-bold text-gray-800 cat_info">
                   ${formatter(d.avg_views)}
               </td>
           </tr>
           <tr>
               <td>effectiveness: </td>
               <td class="h5 mb-0 font-weight-bold text-gray-800 cat_info">
                   ${d.value.toFixed(3)}
               </td>
           </tr>
       </table>
       <ul id="tooltip_vids" class="tooltip_vids"></ul>
   `
   return html
}