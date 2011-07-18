
/* requires RelatedObjects.js */

function didAddPopup(win,newId,newRepr) {
    var name = windowname_to_id(win.name);
    $("#"+name).trigger('didAddPopup',[html_unescape(newId),html_unescape(newRepr)]);
    win.close();
}

autocompleteselectmultiplevalues = new Array();

function setup_autocompleteselect(useid,url) {
    //alert(useid+' '+url);
    $("#"+useid+"_text").autocomplete(url, {
        width: 320,
        formatItem: function(row) { return row[2]; },
        formatResult: function(row) { return row[1]; },
        dataType: "text"
    });
    $("#"+useid+"_text").result(function(event, data) {
        prev = $("#"+useid+"").val();
        if(prev) {
            $("#"+useid+"").val( '' );
            $( "#"+useid+"_on_deck" ).children().fadeOut(1.0).remove();
        }
        $("#"+useid+"").val(data[0]);
        $("#"+useid+"_text").val("");
        addKiller = function(repr,id) {
            kill = "<span class='iconic' id='kill_"+useid+"'>X</span>   ";
            if(repr){
                $( "#"+useid+"_on_deck" ).empty();
                $( "#"+useid+"_on_deck" ).append( "<div>" + kill + repr + "</div>");
            } else {
                $( "#"+useid+"_on_deck > div" ).prepend(kill);
            }
            $("#kill_"+useid+"").click(function() { return function(){
                $("#"+useid+"").val( '' );
                $( "#"+useid+"_on_deck" ).children().fadeOut(1.0).remove();
                $("#"+useid+"_on_deck").trigger("killed");
            } }() );
        }
        addKiller(data[1],data[0]);
        $("#"+useid+"_on_deck").trigger("added");
    });
    if($("#"+useid+"").val()) { // add X for initial value if any
        addKiller = function(repr,id) {
            kill = "<span class='iconic' id='kill_"+useid+"'>X</span>   ";
            if(repr){
                $( "#"+useid+"_on_deck" ).empty();
                $( "#"+useid+"_on_deck" ).append( "<div>" + kill + repr + "</div>");
            } else {
                $( "#"+useid+"_on_deck > div" ).prepend(kill);
            }
            $("#kill_"+useid+"").click(function() { return function(){
                $("#"+useid+"").val( '' );
                $( "#"+useid+"_on_deck" ).children().fadeOut(1.0).remove();
                $("#"+useid+"_on_deck").trigger("killed");
            } }() );
        }
        addKiller(null,$("#"+useid+"").val());
    }
    $("#"+useid+"").bind('didAddPopup',function(event,id,repr) {
        data = Array();
        data[0] = id;
        data[1] = repr;
        prev = $("#"+useid+"").val();
        if(prev) {
            $("#"+useid+"").val( '' );
            $( "#"+useid+"_on_deck" ).children().fadeOut(1.0).remove();
        }
        $("#"+useid+"").val(data[0]);
        $("#"+useid+"_text").val("");
        addKiller = function(repr,id) {
            kill = "<span class='iconic' id='kill_"+useid+"'>X</span>   ";
            if(repr){
                $( "#"+useid+"_on_deck" ).empty();
                $( "#"+useid+"_on_deck" ).append( "<div>" + kill + repr + "</div>");
            } else {
                $( "#"+useid+"_on_deck > div" ).prepend(kill);
            }
            $("#kill_"+useid+"").click(function() { return function(){
                $("#"+useid+"").val( '' );
                $( "#"+useid+"_on_deck" ).children().fadeOut(1.0).remove();
                $("#"+useid+"_on_deck").trigger("killed");
            } }() );
        }
        addKiller(data[1],data[0]);
        $("#"+useid+"_on_deck").trigger("added");
    });
}

function setup_autocompleteselectmultiple(useid,url){
    currentRepr = autocompleteselectmultiplevalues[useid];
    $("#"+useid+"_text").autocomplete(url, {
        width: 320,
        multiple: true,
        multipleSeparator: " ",
        scroll: true,
        scrollHeight:  300,
        formatItem: function(row) { return row[2]; },
        formatResult: function(row) { return row[1]; },
        dataType: "text"
    });

    $("#"+useid+"_text").result(function(event, data)
        {
            id = data[0];
            if( $("#"+useid+"").val().indexOf( "|"+id+"|" ) == -1) {
                if($("#"+useid+"").val() == '') {
                        $("#"+useid+"").val('|');
                }
                $("#"+useid+"").val( $("#"+useid+"").val() + id + "|");
                function addKiller_(repr,id) {
                    killer_id = "kill_"+useid+"" + id
                    kill = "<span class='iconic' id='"+killer_id+"'>X</span>    ";
                    $( "#"+useid+"_on_deck" ).append("<div id='"+useid+"_on_deck_" + id +"'>" + kill + repr + " </div>");
                    $("#"+killer_id).click(function(frozen_id) { return function(){
                        $("#"+useid+"").val( $("#"+useid+"").val().replace( "|" + frozen_id + "|", "|" ) );
                        $("#"+useid+"_on_deck_" + frozen_id).fadeOut().remove();
                        $("#"+useid+"_on_deck").trigger("killed");
                    }}(id) );
                }
                addKiller_(data[1],id);
                $("#"+useid+"_text").val('');
                $("#"+useid+"_on_deck").trigger("added");
            }
        }
    );

    $.each(currentRepr,function(i,its){
        repr = its[0];
        id = its[1]
        killer_id = "kill_"+useid+"" + id
        kill = "<span class='iconic' id='"+killer_id+"'>X</span>        ";
        $( "#"+useid+"_on_deck" ).append("<div id='"+useid+"_on_deck_" + id +"'>" + kill + repr + " </div>");
        $("#"+killer_id).click(function(frozen_id) { return function(){
            $("#"+useid+"").val( $("#"+useid+"").val().replace( "|" + frozen_id + "|", "|" ) );
            $("#"+useid+"_on_deck_" + frozen_id).fadeOut().remove();
            $("#"+useid+"_on_deck").trigger("killed");
        }}(id) );
    });
    $("#"+useid+"").bind('didAddPopup',function(event,id,repr) {
            data = Array();
            data[0] = id;
            data[1] = repr;
            id = data[0];
            if( $("#"+useid+"").val().indexOf( "|"+id+"|" ) == -1) {
                if($("#"+useid+"").val() == '') {
                        $("#"+useid+"").val('|');
                }
                $("#"+useid+"").val( $("#"+useid+"").val() + id + "|");
                function addKiller_(repr,id) {
                    killer_id = "kill_"+useid+"" + id
                    kill = "<span class='iconic' id='"+killer_id+"'>X</span>    ";
                    $( "#"+useid+"_on_deck" ).append("<div id='"+useid+"_on_deck_" + id +"'>" + kill + repr + " </div>");
                    $("#"+killer_id).click(function(frozen_id) { return function(){
                        $("#"+useid+"").val( $("#"+useid+"").val().replace( "|" + frozen_id + "|", "|" ) );
                        $("#"+useid+"_on_deck_" + frozen_id).fadeOut().remove();
                        $("#"+useid+"_on_deck").trigger("killed");
                    }}(id) );
                }
                addKiller_(data[1],id);
                $("#"+useid+"_text").val('');
                $("#"+useid+"_on_deck").trigger("added");
            }
    });
}
