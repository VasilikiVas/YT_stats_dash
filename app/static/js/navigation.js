    $(document).ready(function(){
        $('#categories').change(function(){
            var url = window.location.pathname
            var splitURL = url.toString().split("/")
            var view = splitURL.at(-2)
            window.location.href = window.location.origin + '/' + view + '/' + $(this).val()

            // update_URL('/category/' + $(this).val())
        })
    })


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