var app_graph = {

    feedname: "",

    // Include required javascript libraries
    include: [
        "static/flot/jquery.flot.min.js",
        "static/flot/jquery.flot.time.min.js",
        "static/flot/jquery.flot.selection.min.js",
        "static/vis.helper.js",
        "static/flot/date.format.js"
    ],

    // App start function
    init: function()
    {
        var placeholder = $('#placeholder');
        
        $("#zoomout").click(function () {view.zoomout(); app_graph.draw();});
        $("#zoomin").click(function () {view.zoomin(); app_graph.draw();});
        $('#right').click(function () {view.panright(); app_graph.draw();});
        $('#left').click(function () {view.panleft(); app_graph.draw();});
        $('.time').click(function () {view.timewindow($(this).attr("time")); app_graph.draw();});
        
        placeholder.bind("plotselected", function (event, ranges)
        {
            view.start = ranges.xaxis.from;
            view.end = ranges.xaxis.to;
            app_graph.draw();
        });
    },

    show: function() 
    {
        req = (window.location.hash).substring(1).split("/");
        app_graph.feedname = req[1]+"/"+req[2];
        console.log(app_graph.feedname);

        var meta = {};

        $.ajax({                                      
            url: path+"api/"+app_graph.feedname+"/meta",
            dataType: 'json',
            async: false,                      
            success: function(data_in) { meta = data_in; } 
        });

        // var feedid = urlParams.feedid;

        var top_offset = 0;
        var placeholder_bound = $('#placeholder_bound');
        var placeholder = $('#placeholder');

        var width = placeholder_bound.width();
        var height = width * 0.5;

        placeholder.width(width);
        placeholder_bound.height(height);
        placeholder.height(height-top_offset);

        view.start = meta.start_time*1000;
        view.end = (meta.start_time + (meta.npoints * meta.interval))*1000;

        $("#vis-title").html(app_graph.feedname);
        app_graph.draw();

        /*
        $(window).resize(function(){
            var width = placeholder_bound.width();
            var height = width * 0.5;

            placeholder.width(width);
            placeholder_bound.height(height);
            placeholder.height(height-top_offset);

            options.xaxis.min = view.start;
            options.xaxis.max = view.end;
            $.plot(placeholder, [{data:data,color: plotColour}], options);
        });
        */
    },
    
    hide: function() 
    {
    
    },
    
    draw: function ()
    {
        var dp = 1;
        var units = "C";
        var fill = false;
        var plotColour = 0;
        
        var options = {
            lines: { fill: fill },
            xaxis: { mode: "time", timezone: "browser", min: view.start, max: view.end},
            //yaxis: { min: 0 },
            grid: {hoverable: true, clickable: true},
            selection: { mode: "x" }
        }
        
        var data = [];
        
        var npoints = 800;
        interval = Math.round(((view.end - view.start)/npoints)/1000);
        
        $.ajax({                                      
            url: path+"api/"+app_graph.feedname+"/data",                         
            data: "start="+view.start+"&end="+view.end+"&interval="+interval,
            dataType: 'json',
            async: false,                      
            success: function(data_in) { data = data_in; }
        });
        
        options.xaxis.min = view.start;
        options.xaxis.max = view.end;
        $.plot($('#placeholder'), [{data:data,color: plotColour}], options);
    }
}
