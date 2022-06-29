



function create_wordcloud() {
    
}
// http://127.0.0.1:5000/get_word_cloud_data?category=gaming
var url = window.location.pathname
var splitURL = url.toString().split("/")
var view = splitURL.at(-2)
var cname = splitURL.at(-1)

fetch_url = `/get_word_cloud_data?${view}=${cname}`

var div = document.getElementById("myWordCloud")

fetch(fetch_url)
    .then(function(response) { return response.json(); })
    .then( function(data) {

    // Encapsulate the word cloud functionality
    function wordCloud(selector) {


        //Construct the word cloud's SVG element
        var svg = d3.select(selector).append("svg")
            // .attr("width", 800)
            // .attr("height", 300)
            .attr("viewBox", [0,0, div.offsetWidth, 300])
            .append("g")
            .attr("class", "wordcloud")
            .attr("transform", "translate(460,160)");

        var word2color = data['color']
        var word2size = data['size']

        //Draw the word cloud
        function draw(words) {
            var cloud = svg.selectAll("g text")
                            .data(words, function(d) { 
                                return d.text; 
                            })

            var color = d3.scale.linear()
                .domain([0,50,100])
                .range(["dodgerblue", "limegreen", "yellow"]);


            //Entering words
            cloud.enter()
                .append("text")
                .style("font-family", "Impact")
                .style("fill", function(d, i) {
                    return color(word2color[d['text']]);
                })
                .attr("text-anchor", "middle")
                .attr('font-size', 1)
                .text(function(d) { 
                    return d['text']; });

            //Entering and existing words
            cloud
                .transition()
                    .duration(600)
                    .style("font-size", function(d) { 
                        return d.size+ "px"; 
                    })
                    .attr("transform", function(d) {
                        return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
                    })
                    .style("fill-opacity", 1);

            var x1 = -430,
            barWidth = 20,
            y1 = -130,
            barHeight = 250;
            
            var idGradient = "legendGradient";
                                        
            svg.append("g")
                .append("defs")
                .append("linearGradient")
                .attr("id",idGradient)
                .attr("x1","100%")
                .attr("x2","100%")
                .attr("y1","0%")
                .attr("y2","100%"); 

            svg.append("rect")
                .attr("fill","url(#" + idGradient + ")")
                .attr("x",x1)
                .attr("y",y1)
                .attr("width",barWidth)
                .attr("height",barHeight)
                .attr("rx",0)
                .attr("ry",0);
                
            var textY = y1 + barHeight/2 + 15;
                svg.append("text")
                    .attr("class","legendText")
                    .attr("text-anchor", "middle")
                    .attr("x",x1 + 10)
                    .attr("y",textY)
                    .attr("dy",-150)
                    .text(data.count_range[1]);
                
            svg.append("text")
                .attr("class","legendText")
                .attr("text-anchor", "middle")
                // .attr("x",x1 + 100)
                .attr("x",x1)
                .attr("y",textY)
                .attr("dy", 0)
                .attr('transform', 'translate( -450 , -440) rotate(270)')
                .text("word occurrences");
                
            svg.append("text")
                .attr("class","legendText")
                .attr("text-anchor", "left")
                // .attr("x",x1 + barWidth + 15)
                .attr("x",x1 +5)
                .attr("y",textY)
                .attr("dy",130)
                .text(data.count_range[0]);
                
                
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


    }


    //Use the module pattern to encapsulate the visualisation code. We'll
    // expose only the parts that need to be public.
    return {

        //Recompute the word cloud for a new set of words. This method will
        // asycnhronously call draw when the layout has been computed.
        //The outside world will need to call this function, so make it part
        // of the wordCloud return value.
        update: function(words) {
            d3.layout
                .cloud()
                .size([div.offsetWidth*.9, 300])
                .words(words)
                // .padding(1)
                .rotate(function() { return ~~(Math.random() * 2) * 90; })
                .font("Impact")
                .fontSize(function(d) { 
                    return word2size[d['text']]; 
                })
                .on("end", draw)
                .start();
        }
    }
}

function getWords(i) {
    return Object.keys(data['size'])
            .map(function(key) {
                return {text: key, size: data['size'][key] *60 }; //TODO: we have to adjust the ratio
            })
}

//This method tells the word cloud to redraw with a new set of words.
function showNewWords(vis, i) {
    i = i || 0;

    vis.update(getWords(i ++ % Object.keys(data['size']).length))
    // vis.update(getWords(Object.keys(word2count).length))
}

//Create a new instance of the word cloud visualisation.
var myWordCloud = wordCloud('#myWordCloud');

showNewWords(myWordCloud);
})

// document.getElementById("wordcloud_btn").on("click", showNewWords(myWordCloud))
