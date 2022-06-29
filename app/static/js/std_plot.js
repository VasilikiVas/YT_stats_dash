// function to format tooltip data
const formatter =  d3.format(',d')

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
            
            var mean = dataset.mean
            var data = dataset.datapoints

            var margin = { top: 10, right: 20, bottom: 50, left: 120 },
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


            x.domain([xMin-0.03, xMax+0.03]);
            // y.domain([yMin, yMax]);
            y.domain([0, yMax*1.05]);
            // console.log(yMin);

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
                  if (view == "category") {
                     return construct_tooltip_channel({std:d.x, avg_views:d.y, name:d.name, subs:d.subs, logo_url:d.logo_url},
                        incl_std = true)
                  } else if (view == "channel") {
                     return construct_tooltip_video({deviation:d.x, views:d.y, title:d.title, channel:d.channel, thumbnail_url:d.thumbnail},
                        incl_dev = true)
                  }})

            var zoomBeh = d3.behavior.zoom()
               .x(x)
               .y(y)
               .scaleExtent([0, 500])
               .on("zoom", zoom);

            // 2. Append svg-object to div
            var svg = d3.select(std_plot_id)
               .append("svg")
                 .attr("viewBox", [0, 0, outerWidth, outerHeight])
               .append("g")
                 .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
                 .call(zoomBeh);

            svg.call(tip);

            svg.append("rect")
               .attr("width", width)
               .attr("height", height)
            
            svg.append("g")
               .style("font-size","15px")
               .classed("x axis", true)
               .attr("transform", "translate(0," + height + ")")
               .call(xAxis)
             .append("text")
               .attr("x", (width - margin.left- margin.right) / 2)
               .attr("y",  margin.bottom - 10)
               .attr("class", "label")
               .text(function(d) {
                  if (view == "category") {
                     return "Standard Deviation"
                  } else if (view == "channel"){
                     return "Deviation"
                  }})

            svg.append("g")
               .style("font-size","15px")
               .classed("y axis", true)
               .call(yAxis)
             .append("text")
               .attr("y", -0.9*margin.left)
               .attr("x", -(height)/2)
               .attr("transform", "rotate(-90)")
               .attr("class", "label")
               .text("Views")    

            svg.append("text")
               .attr("class", "meanLabel")
               .attr("y", y(yMax+0.5))
               .text("mean")
               .attr("transform", "translate("+ (parseFloat(x(mean))-20).toString() +",0)")

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

            objects.append("svg:line")
               .attr("class", "medianLine vMedianLine")
               .attr("y1",y(yMax - 0.5))
               .attr("y2",y(yMin))
               .style("stroke", "black")
               .style("stroke-dasharray", ("4, 4"))
               .attr("transform", "translate("+ x(mean) +",0)")
            
            if (view == "channel"){
               objects.selectAll(".dot")
                  .data(data)
                  .enter()
                  .append("svg:image")
                     .classed("dot", true)
                     .attr("xlink:href", function(d) {
                        // console.log(d.thumbnail)
                        return d.thumbnail})
                     .attr("height", "40")
                     .attr("transform", transform)
                  .on("mouseover", tip.show)
                  .on("mouseout", tip.hide)
                  
            } else if (view=="category"){
               objects.selectAll(".dot")
                  .data(data)
                  .enter()
                  .append("circle")
                     .classed("dot", true)
                     .attr("r", 6)
                     .attr("transform", transform)
                     .style("fill", color)
                  .on("click", function(d) {
                           let url = `/channel/${d.name_id}`
                           window.location.href = url
                     })
                  .on("mouseover", tip.show)
                  .on("mouseout", tip.hide)
            }

             function zoom() {
               svg.select(".x.axis").call(xAxis);
               svg.select(".y.axis").call(yAxis);
               svg.select(".meanLabel").attr("transform", "translate("+ (parseFloat(x(mean))-20).toString() +",0)") 

               objects.select(".vMedianLine").attr("transform", "translate("+x(mean)+",0)");
           
               svg.selectAll(".dot")
                   .attr("transform", transform);
             }
            
             function transform(d) {
               // console.log("translate(" + x(d['x']) + "," + y(d['y']) + ")");
               return "translate(" + x(d['x']) + "," + y(d['y']) + ")";
             }
           })
}

create_std_plot(subview_mode)