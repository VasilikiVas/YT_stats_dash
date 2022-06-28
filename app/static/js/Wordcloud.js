// Tokens should be given in such a format, where values are the counts of tokens (or tfidf values
var word2count = { 'Hello': 100, 'there': 100, 'Good': 30, 'morning':40, 'to':50, 'you':60,
'my': 10, 'what': 100, 'weather': 30, 'mood':40, 'four':50, 'eight':60,
'name': 10, 'about': 100, 'cloud': 30, 'one':40, 'fine':50, 'nine':60,
'is': 10, 'yours': 98, 'sun': 30, 'two':40, 'six':50, 'ten':60,
'100': 10, '20': 10, '5': 30, '8':40, 'fec':50, 'tgvrwveween':60,
'1': 10, '3': 10, '6': 30, '9':40, 'vevd':50, 'tewfceqen':60,
'2': 10, '4': 10, '7': 30, '64':40, 'sdewdeqix':50, 'ewdcw':60,
'danai': 100, 'the': 10, 'sea': 30, 'cecs':40, 'sevrefvween':50, 'fewfeqw':60};

var word2tfidf = { 'Hello': 1, 'there': 100, 'Good': 30, 'morning':40, 'to':50, 'you':60,
'my': 10, 'what': 100, 'weather': 30, 'mood':40, 'four':50, 'eight':60,
'name': 10, 'about': 100, 'cloud': 30, 'one':40, 'fine':50, 'nine':60,
'is': 10, 'yours': 98, 'sun': 30, 'two':40, 'six':50, 'ten':60,
'100': 10, '20': 10, '5': 30, '8':40, 'fec':50, 'tgvrwveween':60,
'1': 10, '3': 10, '6': 30, '9':40, 'vevd':50, 'tewfceqen':60,
'2': 10, '4': 10, '7': 30, '64':40, 'sdewdeqix':50, 'ewdcw':60,
'danai': 100, 'the': 10, 'sea': 30, 'cecs':40, 'sevrefvween':50, 'fewfeqw':60};

console.log("hello")
// import * as cloud from 'd3-cloud';

// Encapsulate the word cloud functionality
function wordCloud(selector) {

    //Construct the word cloud's SVG element
    var svg = d3.select(selector).append("svg")
        .attr("width", 700)
        .attr("height", 300)
        .append("g")
        .attr("class", "wordcloud")
        .attr("transform", "translate(350,150)");


    var color = d3.scale.linear()
        .domain([1, 50, 100])
        .range(["dodgerblue", "limegreen", "yellow"]);

    //Draw the word cloud
    function draw(words) {
        var cloud = svg.selectAll("g text")
                        .data(words, function(d) { return d.text; })

        //Entering words
        cloud.enter()
            .append("text")
            .style("font-family", "Impact")
            .style("fill", function(d, i) {return color(word2tfidf[d.text]);
            })
            .attr("text-anchor", "middle")
            .attr('font-size', 1)
            .text(function(d) { return d.text; });

        //Entering and existing words
        cloud
            .transition()
                .duration(600)
                .style("font-size", function(d) { return d.size + "px"; })
                .attr("transform", function(d) {
                    return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
                })
                .style("fill-opacity", 1);
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
                .size([600, 200])
                .words(words)
                // .padding(1)
                .rotate(function() { return ~~(Math.random() * 2) * 90; })
                .font("Impact")
                .fontSize(function(d) { return d.size*0.5; })
                .on("end", draw)
                .start();
        }
    }
}

function getWords(i) {
    return Object.keys(word2count)
            .map(function(key) {
                // return {text: d, size: 10 + Math.random() * 60};
                return {text: key, size: word2count[key] }; //TODO: we have to adjust the ratio
            })
}

//This method tells the word cloud to redraw with a new set of words.
function showNewWords(vis, i) {
    i = i || 0;

    // vis.update(getWords(i ++ % words.length))
    vis.update(getWords(i ++ % Object.keys(word2count).length))
    // vis.update(getWords(Object.keys(word2count).length))
}

//Create a new instance of the word cloud visualisation.
var myWordCloud = wordCloud('myWordCloud');
console.log("hello2")

showNewWords(myWordCloud);