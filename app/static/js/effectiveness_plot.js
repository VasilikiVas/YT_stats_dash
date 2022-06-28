
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
                        <span class="ml-1">${vid.title}</span>
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

function create_effectiveness_plot(min_count) {
    // Colors to differentiate riders with and without doping allegations
    var colors = ["#27ae60"]

    // Create an invisible div for the tooltip
    const tooltip = d3.select("body")
                     .append("div")
                     .attr("id", "tooltip")
                     .style("visibility", "hidden")
                     .style("width", "400px")

    // Parse the Data
    var url = window.location.pathname
    var splitURL = url.toString().split("/")
    var view = splitURL.at(-2)
    var cname = splitURL.at(-1)

    fetch_url = `/get_${subview_mode}_effectiveness_data?${view}=${cname}&min_count=${min_count}`
    fetch(fetch_url)
        .then(function(response) { return response.json(); })
        .then( function(data) {

        console.log(data)

        // set the dimensions and margins of the graph
        let plot_div = document.querySelector("#effectivenessPlot .simplebar-content")
        let w = plot_div.offsetWidth
        // let h = document.body.offsetHeight
        let h = data.length * 30

        const margin = {top: 30, right: 10, bottom: 30, left: 5},
            width = w - margin.left - margin.right,
            height = h - margin.top - margin.bottom;

        // append the svg object to the body of the page
        const svg_axis = d3.select("#effectivenessPlotAxis")
            .append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", margin.top)
            .append("g")
                .attr("transform", `translate(${margin.left}, ${margin.top})`);
        const svg = d3.select("#effectivenessPlot .simplebar-content")
        .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.bottom)
        .append("g")
            .attr("transform", `translate(${margin.left}, ${0})`);

        // Add X axis
        // const x = d3.scaleLinear()
        const x = d3.scale.linear()
            .domain(d3.extent(data, d => d.value))
            .range([ 0, width])
        let xAxisGenerator = d3.svg.axis()
            .scale(x.copy())
            .orient("top")
            // .ticks(5)
        let xAxis = svg_axis.append("g")
            .attr("transform", `translate(0, ${0})`)
            // .call(d3.axisTop(x).ticks(5)).select(".domain").remove()
            .call(xAxisGenerator)

        // Y axis
        // const y = d3.scaleBand()
        const y = d3.scale.ordinal()
            // .range([ 0, height ])
            .rangeBands([ 0, height ])
            .domain(data.map(function(d) { return d.group; }))
            // .padding(1)

        // const yScale = d3.scale.linear()
        const yScale = d3.scale.linear()
            .domain([0,1])
            .range([0, height])
    

        svg.append("line")
            .style("stroke-dasharray", ("4, 4"))
            .attr("x1",x(1))
            .attr("y1",yScale(1))
            .attr("x2",x(1))
            .attr("y2",yScale(0))
            .style("stroke", "black")


        // let yAxisGenerator = d3.axisRight(y)
        let yAxisGenerator = d3.svg.axis()
            .scale(y)
            .orient("right")
        // yAxisGenerator.tickSize(0)
        let yAxis = svg.append("g")
            .call(yAxisGenerator)
            // .attr("transform", `translate(0, -15)`);

        yAxis.select(".domain").remove()
        yAxis.selectAll(".tick text")
            .attr("font-size","20")
            .attr("color","black")

        xAxis.select(".domain").remove()
        xAxis.selectAll(".tick text")
            .attr("font-size","10")
            .attr("color","black")  

        // Circles of variable
        svg.selectAll("mycircle")
            .data(data)
            // .join("circle")
            .enter().append("circle")
                .attr("cx", function(d) { return x(d.value); })
                .attr("cy", function(d) { return y(d.group)+15; })
                .attr("r", "6")
                .style("fill", "#69b3a2")
                .style("opacity", ".5")
                .on("mouseover", function(d){
                    // info = d.toElement.__data__
                    info = d
                    tooltip.style("visibility", "visible")
                            .style("right", window.innerWidth-event.pageX+10+"px")
                            .style("top", event.pageY+"px")
                            .attr("data-std", info["x"])
                            .html(construct_effectiveness_tooltip(
                                    info,
                                    subview_mode, view, cname
                                ))
                })
                .on("mousemove", function(){
                    tooltip.style("right", window.innerWidth-event.pageX+10+"px")
                })
                .on("mouseout", function(){
                    tooltip.style("visibility", "hidden")
                })
              
    })
}

let checkExist = setInterval(function() {
    if (document.querySelector("#effectivenessPlot .simplebar-content")) {
        console.log("Simplebar for effectiveness loaded!");
        clearInterval(checkExist);
    create_effectiveness_plot(100)
    }
}, 10); // check every 10ms
