// Url to the input data
var url = "https://raw.githubusercontent.com/VasilikiVas/Thesis/main/std_test.json?token=GHSAT0AAAAAABUW463HYD5JZSFEIEB6LEPEYVY3ZTQ"
// Colors to differentiate riders with and without doping allegations
var colors = ["#27ae60"]

// The attributes of the riders corresponding to the above colors
var legendKeys = ["Video"]

// Create an invisible div for the tooltip
const tooltip = d3.select("body")
                  .append("div")
                  .attr("id", "tooltip")
                  .style("visibility", "hidden")

// 1. Load the data from external source
d3.json(url).then(function(dataset) {
   mean = dataset.mean
   data = dataset.datapoints
   //data = dataset

    // 2. Append svg-object for the bar chart to a div in your webpage
    // (here we use a div with id=container)
    var width = 700;
    var height = 270;
    var margin = {left: 90, top: 80, bottom: 50, right: 20};
    var axisOffset = 10   // How for the axes are moved away from each other

    const svg = d3.select("#container")
                  .append("svg")
                  .attr("id", "svg")
                  .attr("width", width)
                  .attr("height", height)

    // 3. Define scales to translate domains of the data to the range of the svg
    var xMin = d3.min(data, (d) => d["std"]);
    var xMax = d3.max(data, (d) => d["std"]);

    var yMin = d3.min(data, (d) => d["Video views"]);
    var yMax = d3.max(data, (d) => d["Video views"]);

    var xScale = d3.scaleLinear()
                   .domain([xMin, xMax])
                   .range([margin.left + axisOffset, width- margin.right])

    var yScale = d3.scaleLinear()
                   .domain([yMin, yMax])
                   .range([height- margin.bottom - axisOffset, margin.top])

    // 4. Draw and transform/translate horizontal and vertical axes
    var xAxis = d3.axisBottom().scale(xScale).tickFormat(d3.format(".3f"))
    var yAxis = d3.axisLeft().scale(yScale).tickFormat(d3.format("d"))

    svg.append("g")
       .attr("transform", "translate(0, "+ (height - margin.bottom) + ")")
       .attr("id", "x-axis")
       .call(xAxis)

    svg.append("g")
       .attr("transform", "translate("+ (margin.left)+", 0)")
       .attr("id", "y-axis")
       .call(yAxis)

    svg.append("line")
       .style("stroke-dasharray", ("4, 4"))
       .attr("x1",xScale(mean))
       .attr("y1",yScale(yMax - 0.5))
       .attr("x2",xScale(mean))
       .attr("y2",yScale(yMin))
       .style("stroke", "black")

    // 5. Draw individual scatter points and define mouse events for the tooltip
    svg.selectAll("scatterPoints")
       .data(data)
       .enter()
       .append("circle")
       .attr("cx", (d) => xScale(d["std"]))
       .attr("cy", (d) => yScale(d["Video views"]))
       .attr("r", 5)
       .attr("fill", colors[0])
       .attr("class", "dot")
       .attr("data-xvalue", (d) => d["std"])
       .attr("data-yvalue", (d) => d["Video views"])
       .on("mouseover", function(d){
         info = d.toElement.__data__
           tooltip.style("visibility", "visible")
                  .style("left", event.pageX+10+"px")
                  .style("top", event.pageY-80+"px")
                  .attr("data-std", info["std"])
                  .html("Video name: "+info["Video_name"]+"<br><br>"+"STD: "+info["std"]+"<br><br>"+"Number of views: "+ info["Video views"]+"<br><br>"+"Channel name: "+info["Channel"])
       })
       .on("mousemove", function(){
           tooltip.style("left", event.pageX+10+"px")
       })
       .on("mouseout", function(){
           tooltip.style("visibility", "hidden")
       })

     // 6. Finalize chart by adding title, axes labels and legend
     svg.append("text")
        .attr("x", margin.left + (width - margin.left - margin.right) / 2)
        .attr("y", height - margin.bottom / 5)
        .attr("class", "label")
        .text("std");

     svg.append("text")
         .attr("y", margin.left/2)
         .attr("x", -height/2)
         .attr("transform", "rotate(-90)")
         .attr("class", "label")
         .text("Views");

     svg.selectAll("legendSymbols")
        .data(legendKeys)
        .enter()
        .append("circle")
        .attr("cx", width - margin.right - 75)
        .attr("cy", (d, i) => 150 + i * 25)
        .attr("r", 5)
        .attr("fill", (d, i) => colors[i])

     svg.selectAll("legendTexts")
        .data(legendKeys)
        .enter()
        .append("text")
        .text((d) => d)
        .attr("x", width - margin.right - 75 + 10)
        .attr("y", (d, i) => 150 + i * 25 + 5)
        .attr("class", "textbox")

     svg.append("text")
        .attr("x", xScale(mean))
        .attr("y", yScale(yMax+0.5))
        .attr("class", "label")
        .text("mean");

     const legend = svg.append("rect")
                       .attr("x", width - margin.right - 85)
                       .attr("y", 150-5-10)
                       .attr("rx", 5)
                       .attr("ry", 5)
                       .attr("width", 63)
                       .attr("height", 30)
                       .attr("id", "legend")
}) 