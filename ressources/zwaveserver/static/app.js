var app = {

    include: {},

    load: function(appname) 
    {
        // We load here the html of the app into an dedicated element for that app
        // when an app is loaded its html remains in the dom even when viewing another app
        // an app is just hidden and shown depending on the visibility settings.
        
        // we check here if the app has been loaded to the dom, if not we load it
        
        var appdom = $("#app_"+appname);
        
        if (appdom.length) return true;
        
    
        var html = "";
        $.ajax({url: "static/apps/"+appname+"/"+appname+".html", async: false, cache: false, success: function(data) {html = data;} });
        
        $("#content").append('<div class="apps" id="app_'+appname+'" style="display:none"></div>');
        $("#app_"+appname).html(html);

        $.ajax({
            url: "static/apps/"+appname+"/"+appname+".js",
            dataType: 'script',
            async: false
        });
        
        // ----------------------------------------------------------
        // Included javascript loader
        // ----------------------------------------------------------
        var include = window["app_"+appname].include;
        for (i in include) {
            var file = include[i];
            if (app.include[file]==undefined)
            {
                app.include[file] = true;
                $.ajax({
                    url: file,
                    dataType: 'script',
                    async: false
                });
            }
        }
        
        window["app_"+appname].init();
        
        return true;
    },
    
    show: function(appname)
    {
        $(".apps").hide();
        $("#app_"+appname).show();
        if (window["app_"+appname]!=undefined) window["app_"+appname].show();
    },
    
    hide: function(appname)
    {
        $("#app_"+appname).hide();
        if (window["app_"+appname]!=undefined) window["app_"+appname].hide();
    }
};
