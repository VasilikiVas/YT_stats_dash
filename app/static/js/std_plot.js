// function to format tooltip data
const formatter =  d3.format(',d')

function construct_std_tooltip(info) {
   return `
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
   </div>`
}

function create_std_plot(subview){

   // Colors to differentiate riders with and without doping allegations
   var color = "#27ae60"

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
            var margin = { top: 10, right: 20, bottom: 50, left: 90 },
               outerWidth = 800,
               outerHeight = 300,
               width = outerWidth - margin.left - margin.right,
               height = outerHeight - margin.top - margin.bottom;
            
            var x = d3.scale.linear()
               .range([0, width]).nice();

            var y = d3.scale.linear()
               .range([height, 0]).nice();
            

            // 3. Define scales to translate domains of the data to the range of the svg
            var xMin = d3.min(data, function(d) { return d["x"];})
            var xMax = d3.max(data, function(d) { return d["x"];})

            var yMin = d3.min(data, function(d) { return d["y"];})
            var yMax = d3.max(data, function(d) { return d["y"];})

            x.domain([xMin, xMax]);
            y.domain([yMin, yMax]);

            // 4. Draw and transform/translate horizontal and vertical axes
            var xAxis = d3.svg.axis()
               .scale(x)
               .orient("bottom")
               .tickSize(-height);

            var yAxis = d3.svg.axis()
               .scale(y)
               .orient("left")
               .tickSize(-width);

            var tip = d3.tip()
               .attr("class", "d3-tip")
               .offset([-10, 0])
               .html(function(d) {
                  return construct_std_tooltip(d)})

            var zoomBeh = d3.behavior.zoom()
               .x(x)
               .y(y)
               .scaleExtent([0, 500])
               .on("zoom", zoom);

            var svg = d3.select(std_plot_id)
               .append("svg")
                 .attr("viewBox", [0, 0, outerWidth, outerHeight])
               .append("g")
                 .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
                 .call(zoomBeh);

            svg.call(tip);

            svg.append("rect")
               .attr("width", width)
               .attr("height", height);

            svg.append("g")
               .classed("x axis", true)
               .attr("transform", "translate(0," + height + ")")
               .call(xAxis)
             .append("text")
               .classed("label", true)
               .attr("x", width)
               .attr("y", margin.bottom - 10)
               .style("text-anchor", "end")
               .text("std");

            svg.append("g")
               .classed("y axis", true)
               .call(yAxis)
             .append("text")
               .classed("label", true)
               .attr("transform", "rotate(-90)")
               .attr("y", -margin.left)
               .attr("dy", ".71em")
               .style("text-anchor", "end")
               .text("Views");

            var objects = svg.append("svg")
               .classed("objects", true)
               .attr("width", width)
               .attr("height", height);
         
            objects.append("svg:line")
               .classed("axisLine hAxisLine", true)
               .attr("x1", 0)
               .attr("y1", 0)
               .attr("x2", width)
               .attr("y2", 0)
               .attr("transform", "translate(0," + height + ")")
         
            objects.append("svg:line")
               .classed("axisLine vAxisLine", true)
               .attr("x1", 0)
               .attr("y1", 0)
               .attr("x2", 0)
               .attr("y2", height);

            svg.append("line")
               .style("stroke-dasharray", ("4, 4"))
               .attr("x1",x(mean))
               .attr("y1",y(yMax - 0.5))
               .attr("x2",x(mean))
               .attr("y2",y(yMin))
               .style("stroke", "black")

            objects.selectAll(".dot")
               .data(data)
               .enter().append("circle")
               .classed("dot", true)
               .attr("r", 4)
               .attr("transform", transform)
               .style("fill", color)
               .on("click", function(d) {
                  let url = `/channel/${d.target.__data__.name_id}`
                  window.location.href = url
               })
               .on("mouseover", tip.show)
               .on("mouseout", tip.hide);

            d3.select("input").on("click", change);

            function change() {
               xMax = d3.max(data, function(d) { return d["x"]; });
               xMin = d3.min(data, function(d) { return d["x"]; });
           
               zoomBeh.x(x.domain([xMin, xMax])).y(y.domain([yMin, yMax]));
           
               var svg = d3.select(std_plot_id).transition();
           
               svg.select(".x.axis").duration(750).call(xAxis).select(".label").text('std');
           
               objects.selectAll(".dot").transition().duration(1000).attr("transform", transform);
             }

             function zoom() {
               svg.select(".x.axis").call(xAxis);
               svg.select(".y.axis").call(yAxis);
           
               svg.selectAll(".dot")
                   .attr("transform", transform);
             }
           
             function transform(d) {
               return "translate(" + x(d['x']) + "," + y(d['y']) + ")";
             }
           })
}

//             svg.append("g")
//                .attr("transform", "translate(0, "+ (height - margin.bottom) + ")")
//                .attr("id", "x-axis")
//                .call(xAxis)

//             svg.append("g")
//                .attr("transform", "translate("+ (margin.left)+", 0)")
//                .attr("id", "y-axis")
//                .call(yAxis)

//             // 5. Draw individual scatter points and define mouse events for the tooltip
//             svg.selectAll("scatterPoints")
//                .data(data)
//                .enter()
//                .append("circle")
//                .style("opacity", 0.6)
//                .attr("cx", (d) => xScale(d["x"]))
//                .attr("cy", (d) => yScale(d["y"]))
//                .attr("r", 5)
//                .attr("fill", colors[0])
//                .attr("class", "dot")
//                .attr("data-xvalue", (d) => d["x"])
//                .attr("data-yvalue", (d) => d["y"])
//                .on("click", function(d) {
//                   let url = `/channel/${d.target.__data__.channel_id}`
//                   window.location.href = url
//                })
//                .on("mouseover", function(d){
//                   info = d.toElement.__data__
//                   tooltip.style("visibility", "visible")
//                            .style("left", event.pageX+10+"px")
//                            .style("top", event.pageY-80+"px")
//                            .attr("data-std", info["x"])
//                            .html(`
//                   <div>
//                      <a +class="channel_entry nav-link">
//                            <img src="${info["logo_url"]}" class="channel_logo">
//                            <span class="ml-1 h5 font-weight-bold text-gray-800">${info["name"]}</span>
//                      </a>
//                      <table>
//                            <tr>
//                               <td>std: </td>
//                               <td class="h5 mb-0 font-weight-bold text-gray-800">${info["x"]}</td>
//                            </tr>
//                            <tr>
//                               <td>avg views: </td>
//                               <td class="h5 mb-0 font-weight-bold text-gray-800">${formatter(info["y"])}</td>
//                            </tr>
//                      </table>
//                   </div>`)
//                })
//                .on("mousemove", function(){
//                   tooltip.style("left", event.pageX+10+"px")
//                })
//                .on("mouseout", function(){
//                   tooltip.style("visibility", "hidden")
//                })

//             // 6. Finalize chart by adding title, axes labels and legend
//             svg.append("text")
//                .attr("x", margin.left + (width - margin.left - margin.right) / 2)
//                .attr("y", height - margin.bottom / 5)
//                .attr("class", "label")
//                .text("std");

//             svg.append("text")
//                   .attr("y", margin.left/2-20)
//                   .attr("x", -height/2)
//                   .attr("transform", "rotate(-90)")
//                   .attr("class", "label")
//                   .text("Views");

//             svg.append("text")
//                .attr("x", xScale(mean))
//                .attr("y", yScale(yMax+0.5))
//                .attr("class", "label")
//                .text("mean");
//             })
// }

create_std_plot(subview_mode)