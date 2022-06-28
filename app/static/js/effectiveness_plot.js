// Parse the Data
var url = window.location.pathname
var splitURL = url.toString().split("/")
var view = splitURL.at(-2)
var cname = splitURL.at(-1)

fetch_url = `/get_token_effectiveness_data?${view}=${cname}`

fetch(fetch_url)
    .then(function(response) { return response.json(); })
    .then( function(data) {

    // set the dimensions and margins of the graph
    let plot_div = document.getElementById("effectivenessPlot")
    let w = plot_div.offsetWidth
    // let h = document.body.offsetHeight
    let h = data.length * 30

    const margin = {top: 30, right: 10, bottom: 30, left: 10},
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
    const x = d3.scaleLinear()
        .domain(d3.extent(data, d => d.value))
        .range([ 0, width]);
    svg_axis.append("g")
        .attr("transform", `translate(0, ${0})`)
        .call(d3.axisTop(x).ticks(5)).select(".domain").remove()

    // data = data.splice(0, 50)

    // Y axis
    const y = d3.scaleBand()
        .range([ 0, height ])
        .domain(data.map(function(d) { return d.group; }))
        .padding(1)

    const yScale = d3.scaleLinear()
        .domain([0,1])
        .range([0, height])
  

    svg.append("line")
        .style("stroke-dasharray", ("4, 4"))
        .attr("x1",x(1))
        .attr("y1",yScale(1))
        .attr("x2",x(1))
        .attr("y2",yScale(0))
        .style("stroke", "black")


    // Circles of variable
    svg.selectAll("mycircle")
        .data(data)
        .join("circle")
            .attr("cx", function(d) { return x(d.value); })
            .attr("cy", function(d) { return y(d.group); })
            .attr("r", "6")
            .style("fill", "#69b3a2")

    let yAxisGenerator = d3.axisRight(y)
    yAxisGenerator.tickSize(0)
    let YAxis = svg.append("g")
        .call(yAxisGenerator)

    YAxis.select(".domain").remove()
    YAxis.selectAll(".tick text")
            .attr("font-size","20")
            .attr("color","black")
})