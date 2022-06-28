// set the dimensions and margins of the graph
const margin = {top: 30, right: 30, bottom: 30, left: 10},
    width = 300 - margin.left - margin.right,
    height = screen.height*.7 - margin.top - margin.bottom;

// append the svg object to the body of the page
const svg = d3.select("#effectivenessPlot")
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", `translate(${margin.left}, ${margin.top})`);

// Parse the Data
var view = splitURL.at(-2)
var cname = splitURL.at(-1)

fetch_url = `/get_token_effectiveness_data?${view}=${cname}`
fetch(fetch_url)
    .then(function(response) { return response.json(); })
    .then( function(data) {
// console.log(data)

  // Add X axis
  const x = d3.scaleLinear()
    .domain(d3.extent(data, d => d.value))
    .range([ 0, width]);
  svg.append("g")
    .attr("transform", `translate(0, ${0})`)
    .call(d3.axisTop(x).ticks(5)).select(".domain").remove()

  // Y axis
  const y = d3.scaleBand()
    .range([ 0, height ])
    .domain(data.map(function(d) { return d.group; }))
    .padding(1);
  

  // Circles of variable
  svg.selectAll("mycircle")
    .data(data)
    .join("circle")
      .attr("cx", function(d) { return x(d.value); })
      .attr("cy", function(d) { return y(d.group); })
      .attr("r", "6")
      .style("fill", "#69b3a2")

    
  svg.append("g")
    .call(d3.axisRight(y).tickSize(0)).select(".domain").remove()
})