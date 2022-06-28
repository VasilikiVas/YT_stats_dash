// Colors to differentiate riders with and without doping allegations
var colors = ["#27ae60"]

// Create an invisible div for the tooltip
const tooltip = d3.select("body")
                  .append("div")
                  .attr("id", "tooltip")
                  .style("visibility", "hidden")

// function to format tooltip data
const formatter =  d3.format(',d')

function create_std_plot(subview){
   // 1. Load the data from external source
   var url = window.location.pathname
   var splitURL = url.toString().split("/")

   var view = splitURL.at(-2)
   var cname = splitURL.at(-1)
   var fetch_url
   var std_plot_id

   if (subview == "thumbnail"){
      fetch_url = `/get_thumbnail_std_plot_data?${view}=` + cname
      std_plot_id = '#thumbnail_std_plot'
   } else {
      fetch_url = `/get_title_std_plot_data?${view}=` + cname
      std_plot_id = '#title_std_plot'
   }

   fetch(fetch_url)
         .then(function(response) { return response.json(); })
         .then((dataset) => {
            
            mean = dataset.mean
            data = dataset.datapoints

            // 2. Append svg-object for the bar chart to a div in your webpage
            var width = 1100;
            var height = 400;
            var margin = {left: 90, top: 10, bottom: 50, right: 20};
            var axisOffset = 10   // How for the axes are moved away from each other
            
            // const zoom = d3.zoom()
            //    .on('zoom', (event) => {
            //    svg.attr('transform', event.transform);
            //    })
            //    .scaleExtent([1, 40]);
            
            const svg = d3.select(std_plot_id)
                           .append("svg")
                           .attr("id", "svg")
                           .attr("viewBox", [0, 0, width, height])

            // 3. Define scales to translate domains of the data to the range of the svg
            var xMin = d3.min(data, (d) => d["x"]);
            var xMax = d3.max(data, (d) => d["x"]);

            var yMin = d3.min(data, (d) => d["y"]);
            var yMax = d3.max(data, (d) => d["y"]);

            var xScale = d3.scaleLinear()
                           .domain([xMin, xMax])
                           .range([margin.left + axisOffset, width- margin.right])

            var yScale = d3.scaleLinear()
                           .domain([yMin, yMax])
                           .range([height- margin.bottom - axisOffset, margin.top])

            // 4. Draw and transform/translate horizontal and vertical axes
            var xAxis = d3.axisBottom().scale(xScale).tickFormat(d3.format(".3f"))
            var yAxis = d3.axisLeft().scale(yScale)

            svg.append("g")
               .attr("transform", "translate(0, "+ (height - margin.bottom) + ")")
               .attr("id", "x-axis")
               .call(xAxis)

            svg.append("g")
               .attr("transform", "translate("+ (margin.left)+", 0)")
               .attr("id", "y-axis")
               .call(yAxis)

            // 5. Draw individual scatter points and define mouse events for the tooltip
            svg.selectAll("scatterPoints")
               .data(data)
               .enter()
               .append("circle")
               .style("opacity", 0.6)
               .attr("cx", (d) => xScale(d["x"]))
               .attr("cy", (d) => yScale(d["y"]))
               .attr("r", 5)
               .attr("fill", colors[0])
               .attr("class", "dot")
               .attr("data-xvalue", (d) => d["x"])
               .attr("data-yvalue", (d) => d["y"])
               .on("click", function(d) {
                  let url = `/channel/${d.target.__data__.channel_id}`
                  window.location.href = url
               })
               .on("mouseover", function(d){
                  info = d.toElement.__data__
                  tooltip.style("visibility", "visible")
                           .style("left", event.pageX+10+"px")
                           .style("top", event.pageY-80+"px")
                           .attr("data-std", info["x"])
                           .html(`
                  <div>
                     <a class="channel_entry nav-link">
                           <img src="${info["logo_url"]}" class="channel_logo">
                           <span class="ml-1 h5 font-weight-bold text-gray-800">${info["name"]}</span>
                     </a>
                     <table>
                           <tr>
                              <td>std: </td>
                              <td class="h5 mb-0 font-weight-bold text-gray-800">${info["x"]}</td>
                           </tr>
                           <tr>
                              <td>avg views: </td>
                              <td class="h5 mb-0 font-weight-bold text-gray-800">${formatter(info["y"])}</td>
                           </tr>
                     </table>
                  </div>`)
               })
               .on("mousemove", function(){
                  tooltip.style("left", event.pageX+10+"px")
               })
               .on("mouseout", function(){
                  tooltip.style("visibility", "hidden")
               })

            svg.append("line")
               .style("stroke-dasharray", ("4, 4"))
               .attr("x1",xScale(mean))
               .attr("y1",yScale(yMax - 0.5))
               .attr("x2",xScale(mean))
               .attr("y2",yScale(yMin))
               .style("stroke", "black")

            // 6. Finalize chart by adding title, axes labels and legend
            svg.append("text")
               .attr("x", margin.left + (width - margin.left - margin.right) / 2)
               .attr("y", height - margin.bottom / 5)
               .attr("class", "label")
               .text("std");

            svg.append("text")
                  .attr("y", margin.left/2-20)
                  .attr("x", -height/2)
                  .attr("transform", "rotate(-90)")
                  .attr("class", "label")
                  .text("Views");

            svg.append("text")
               .attr("x", xScale(mean))
               .attr("y", yScale(yMax+0.5))
               .attr("class", "label")
               .text("mean");
            })
}

create_std_plot(subview_mode)

