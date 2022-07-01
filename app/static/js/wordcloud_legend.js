var svgWidth = 9060,
    svgHeight = 500,
    x1 = 100,
    barWidth = 20,
    y1 = 100,
    barHeight = 300,
    numberHues =14;

var idGradient = "legendGradient";

var svgForLegendStuff = d3.select("#theBar").append("svg")
                            .attr("width", svgWidth)
                            .attr("height", svgHeight)
                            ;

svgForLegendStuff.append("g")
                    .append("defs")
                    .append("linearGradient")
                        .attr("id",idGradient)
                        .attr("x1","100%")
                        .attr("x2","100%")
                        .attr("y1","0%")
                        .attr("y2","100%"); 

svgForLegendStuff.append("rect")
                    .attr("fill","url(#" + idGradient + ")")
                    .attr("x",x1)
                    .attr("y",y1)
                    .attr("width",barWidth)
                    .attr("height",barHeight)
                    .attr("rx",0)
                    .attr("ry",0);

var textY = y1 + barHeight/2 + 15;
svgForLegendStuff.append("text")
                                .attr("class","legendText")
                                .attr("text-anchor", "middle")
                                .attr("x",x1 + 10)
                                .attr("y",textY)
                                .attr("dy",-170)
                                .text("max");

svgForLegendStuff.append("text")
                                .attr("class","legendText")
                                .attr("text-anchor", "middle")
                                .attr("x",x1 + 150)
                                .attr("y",textY)
                                .attr("dy",-180)
                                .attr('transform', 'rotate(270,250,250)')
                                .text("selectivity");

svgForLegendStuff.append("text")
                                .attr("class","legendText")
                                .attr("text-anchor", "left")
                                // .attr("x",x1 + barWidth + 15)
                                .attr("x",x1 - 8)
                                .attr("y",textY)
                                .attr("dy",+152)
                                .text("min");


var opacityStart = 100.0
var opacity,p;
var color = d3.scale.linear()
    .domain([1, 50, 100])
    .range(["yellow", "limegreen", "dodgerblue"])

var theData = [];
for (var i=1; i<100; i+=2) {
    opacity = opacityStart;
    p = 0.01 * i;
    theData.push({"rgb":color(i), "opacity":opacity, "percent":p});
    theData.push({"rgb":color(i), "opacity":opacity, "percent":p});       
}

var stops = d3.select('#' + idGradient).selectAll('stop')
                    .data(theData);
                    
    stops.enter().append('stop');
    stops.attr('offset',function(d) {
                            return d.percent;
                })
                .attr('stop-color',function(d) {
                            return d.rgb;
                })
                .attr('stop-opacity',function(d) {
                            return d.opacity;
                });