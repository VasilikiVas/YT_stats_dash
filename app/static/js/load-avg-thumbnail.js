window.addEventListener('load', (event) => {
    var url = window.location.pathname
    var splitURL = url.toString().split("/")
    
    var view = splitURL.at(-2)
    var name = splitURL.at(-1)
    
    var fetch_url = `/get_thumbnail_average_img?${view}=` + name
    fetch(fetch_url)
        .then(function(response) { return response })
        .then((data) => {
            document.getElementById("avgThumbnail").setAttribute("src", data.url)
    })

    var fetch_url = `/get_most_repr_thumbnail?${view}=` + name
    fetch(fetch_url)
        .then(function(response) { return response })
        .then((data) => {
            document.getElementById("mostReprThumbnail").setAttribute("src", data.url)
    })

    var fetch_url = `/get_most_repr_title?${view}=` + name
    fetch(fetch_url)
        .then(function(response) { return response.json() })
        .then((data) => {
            document.getElementById("mostReprTitle").innerHTML = data.repr
    })
})