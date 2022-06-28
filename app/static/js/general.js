// Display all .cat_info with , seperator between thousands
function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function displayWithCommas(){
    var elements = document.querySelectorAll('.cat_info')
    elements.forEach(element => {
        var val = parseInt(element.getAttribute("value"))
        val = numberWithCommas(val)
        element.innerHTML = val
    })
}

displayWithCommas()