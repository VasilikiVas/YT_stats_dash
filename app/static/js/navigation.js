$(document).ready(function(){
    $('#thumbnailBtn').click(function(){
        window.location.href = window.location.pathname + "?" + "subview_mode=" + $(this).val()
    })

    $('#titleBtn').click(function(){
        window.location.href = window.location.pathname + "?" + "subview_mode=" + $(this).val()
    })
})

// Display all .cat_info with , seperator between thousands
function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function displayWithCommas(){
    var elements = document.querySelectorAll('.cat_info')
    elements.forEach(element => {
        console.log(element)
        var val = parseInt(element.getAttribute("value"))
        val = numberWithCommas(val)
        element.innerHTML = val
    })
}

// $(document).ready(function(){
//     $('#categories').change(function(){
//         var url = window.location.pathname
//         var splitURL = url.toString().split("/")
//         var view = splitURL.at(-2)
//         window.location.href = window.location.origin + '/' + view + '/' + $(this).val()

//         // update_URL('/category/' + $(this).val())
//     })
// })

// window.onload = function() {
//     var url = window.location.pathname
//     var splitURL = url.toString().split("/")
    
//     var view = splitURL.at(-2)
//     var name = splitURL.at(-1)
    
//     var fetch_url = `/get_thumbnail_average_img?${view}=` + name
//     fetch(fetch_url)
//         .then(function(response) { return response })
//         .then((data) => {
//             console.log(data)
//             document.getElementById("avgThumbnail").setAttribute("src", data.url)
//     })
// }

// function update_URL(url) {
//     window.history.pushState("", "", url);
//     updateEverything()
// }

// function updateEverything() {
//     updateDomColoursPlot()
// }

// window.addEventListener('pushState', function(ev) {
//     console.log('pushState!')
//     updateEverything()	
// })

// window.onpopstate = function (event) {
//     // do stuff here
//     updateEverything()
// 	console.log('pushState!');
// }