// Tokens should be given in such a format, where values are the counts of tokens (or tfidf values
// var word2count = { 'Hello': 100, 'there': 100, 'Good': 30, 'morning':40, 'to':50, 'you':60,
// 'my': 10, 'what': 100, 'weather': 30, 'mood':40, 'four':50, 'eight':60,
// 'name': 10, 'about': 100, 'cloud': 30, 'one':40, 'fine':50, 'nine':60,
// 'is': 10, 'yours': 98, 'sun': 30, 'two':40, 'six':50, 'ten':60,
// '100': 10, '20': 10, '5': 30, '8':40, 'fec':50, 'tgvrwveween':60,
// '1': 10, '3': 10, '6': 30, '9':40, 'vevd':50, 'tewfceqen':60,
// '2': 10, '4': 10, '7': 30, '64':40, 'sdewdeqix':50, 'ewdcw':60,
// 'danai': 100, 'the': 10, 'sea': 30, 'cecs':40, 'sevrefvween':50, 'fewfeqw':60};

// var word2tfidf = { 'Hello': 1, 'there': 100, 'Good': 30, 'morning':40, 'to':50, 'you':60,
// 'my': 10, 'what': 100, 'weather': 30, 'mood':40, 'four':50, 'eight':60,
// 'name': 10, 'about': 100, 'cloud': 30, 'one':40, 'fine':50, 'nine':60,
// 'is': 10, 'yours': 98, 'sun': 30, 'two':40, 'six':50, 'ten':60,
// '100': 10, '20': 10, '5': 30, '8':40, 'fec':50, 'tgvrwveween':60,
// '1': 10, '3': 10, '6': 30, '9':40, 'vevd':50, 'tewfceqen':60,
// '2': 10, '4': 10, '7': 30, '64':40, 'sdewdeqix':50, 'ewdcw':60,
// 'danai': 100, 'the': 10, 'sea': 30, 'cecs':40, 'sevrefvween':50, 'fewfeqw':60};

// http://127.0.0.1:5000/get_word_cloud_data?category=gaming
var url = window.location.pathname
var splitURL = url.toString().split("/")
var view = splitURL.at(-2)
var cname = splitURL.at(-1)

// fetch_url = `/get_${subview_mode}_effectiveness_data?${view}=${cname}`
fetch_url = `/get_word_cloud_data?${view}=${cname}`

fetch(fetch_url)
    .then(function(response) { return response.json(); })
    .then( function(data) {


    // Encapsulate the word cloud functionality
    function wordCloud(selector) {

        //Construct the word cloud's SVG element
        var svg = d3.select(selector).append("svg")
            // .attr("width", 800)
            // .attr("height", 300)
            .attr("viewBox", [0,0, 800, 300])
            .append("g")
            .attr("class", "wordcloud")
            .attr("transform", "translate(440,160)");

        var word2tfidf = data['tfidf']
        var word2count = data['counts']

        //Draw the word cloud
        function draw(words) {
            var cloud = svg.selectAll("g text")
                            .data(words, function(d) { 
                                return d.text; 
                            })

            var color = d3.scale.linear()
                .domain([1, 50, 100])
                .range(["dodgerblue", "limegreen", "yellow"]);


            //Entering words
            cloud.enter()
                .append("text")
                .style("font-family", "Impact")
                .style("fill", function(d, i) {
                    return color(word2tfidf[d['text']]/300);
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
                    .text("max");
                
            svg.append("text")
                .attr("class","legendText")
                .attr("text-anchor", "middle")
                .attr("x",x1 + 100)
                .attr("y",textY)
                .attr("dy", 0)
                .attr('transform', 'rotate(270,250,250)')
                .text("specificity");
                
            svg.append("text")
                .attr("class","legendText")
                .attr("text-anchor", "left")
                // .attr("x",x1 + barWidth + 15)
                .attr("x",x1 -2)
                .attr("y",textY)
                .attr("dy",130)
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
                .size([1000, 300])
                .words(words)
                // .padding(1)
                .rotate(function() { return ~~(Math.random() * 2) * 90; })
                .font("Impact")
                .fontSize(function(d) { 
                    return word2count[d['text']]/100; 
                })
                .on("end", draw)
                .start();
        }
    }
}

function getWords(i) {
    return Object.keys(data['counts'])
            .map(function(key) {
                return {text: key, size: data['counts'][key] *60 }; //TODO: we have to adjust the ratio
            })
}

//This method tells the word cloud to redraw with a new set of words.
function showNewWords(vis, i) {
    i = i || 0;

    vis.update(getWords(i ++ % Object.keys(data['counts']).length))
    // vis.update(getWords(Object.keys(word2count).length))
}

//Create a new instance of the word cloud visualisation.
var myWordCloud = wordCloud('#myWordCloud');

showNewWords(myWordCloud);
})