
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

    if (!min_count) {
        min_count = 1000
        if (subview_mode == "thumbnail") { min_count /= 10 }
        if (view == "channel") { min_count = 2 }
    }

    fetch_url = `/get_${subview_mode}_effectiveness_data?${view}=${cname}&min_count=${min_count}`
    fetch(fetch_url)
        .then(function(response) { return response.json(); })
        .then( function(data) {

        // console.log(data)

        // set the dimensions and margins of the graph
        let plot_div = document.querySelector("#effectivenessPlot .simplebar-content")
        let w = plot_div.offsetWidth
        // let h = document.body.offsetHeight
        let h = data.length * 30 + 50

        const margin = {top: 30, right: 10, bottom: 30, left: 10},
            width = w - margin.left - margin.right,
            height = h - margin.top - margin.bottom;

        // append the svg object to the body of the page
        const svg_axis = d3.select("#effectivenessPlotAxis")
            .append("svg")
                .attr("viewBox", [0, 0,  width + margin.left + margin.right, 1.1*margin.top])
            .append("g")
                .attr("transform", `translate(${margin.left}, ${margin.top})`);

        document.querySelector("#effectivenessPlotAxis svg g").innerHTML += `
        <defs>
            <marker
                id="arrow"
                markerUnits="strokeWidth"
                markerWidth="12"
                markerHeight="12"
                viewBox="0 0 12 12"
                refX="6"
                refY="6"
                orient="auto">
                <path d="M2,2 L10,6 L2,10 L6,6 L2,2" style="fill: #000;"></path>
            </marker>
        </defs>
        `

        const svg = d3.select("#effectivenessPlot .simplebar-content")
        .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.bottom)
        .append("g")
            .attr("transform", `translate(${margin.left}, ${0})`);

        // Add X axis
        const x = d3.scale.linear()
            .domain(d3.extent(data, d => d.value))
            .range([ 0, width])

        // X axis arrow
        var line = svg_axis.append("line")
            .attr("x1", width + margin.left)
            .attr("y1", margin.top - 1.16*margin.bottom)  
            .attr("x2", margin.left+margin.right)
            .attr("y2", margin.top - 1.16*margin.bottom)  
            .attr("stroke","black")  
            .attr("stroke-width",1)  
            .attr("marker-end","url(#arrow)");
        
        var efect_text = svg_axis.append("text")
            .attr("x", (margin.left + width/3))
            .attr("y",  margin.top - 1.24*margin.bottom)
            .attr("class", "label")
            .text("less effective")

        // Y axis
        const y = d3.scale.ordinal()
            .rangeBands([ 0, height ])
            .domain(data.map(function(d) { return d.group; }))

        // // yScale for vertical line
        // const yScale = d3.scale.linear()
        //     .domain([0,1])
        //     .range([0, height])
    
        // svg.append("line")
        //     .style("stroke-dasharray", ("4, 4"))
        //     .attr("x1",x(1))
        //     .attr("y1",yScale(1))
        //     .attr("x2",x(1))
        //     .attr("y2",yScale(0))
        //     .style("stroke", "black")

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

        // Circles of variable
        svg.selectAll("mycircle")
            .data(data)
            // .join("circle")
            .enter().append("circle")
                .attr("cx", function(d) { return x(d.value); })
                .attr("cy", function(d) { return y(d.group)+15; })
                .attr("r", "6")
                .style("fill", "#69b3a2")
                .style("opacity", ".7")
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

    function resizeEffPlot() {
        // Set effectiveness plot to the same height as left
        let eff_col = document.getElementById("eff_col")
        let center_col = document.getElementById("center_content_col")

        eff_col.style.height = `${center_col.offsetHeight-20}px`
    }

    resizeEffPlot()

    setTimeout(resizeEffPlot, 500)
}

let checkExistEffectiveness = setInterval(function() {
    if (document.querySelector("#effectivenessPlot .simplebar-content")) {
        // console.log("Simplebar for effectiveness loaded!");
        clearInterval(checkExistEffectiveness);
        create_effectiveness_plot(null)
    }
}, 10); // check every 10ms
