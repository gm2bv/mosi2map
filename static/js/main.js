(function($){
'use strict';

var g_timer;

$(function(){
    // date
    if( $("#deadlineYMD").length ){
        $("#deadlineYMD").datepicker({
          dateFormat: "yy-mm-dd"
        });
    }
    
    // time
    if( $('#hour').length && $('#min').length ){
        if( $('#hour').val() < 0 ){
            $('#min').attr('disabled', 'disabled').addClass('Disabled');
        }
        $('#hour').change(function(){
            if( $('#hour').val() < 0 ){
                $('#min').attr('disabled', 'disabled').addClass('Disabled');
            }else{
                $('#min').removeAttr('disabled').removeClass('Disabled');
            }
        });
    }

    // add a target
    if( $('#addTarget').length ){
        $('#addTarget').on('click', function(){
//            var cnt = $('#targets').find('input[type=text]').length;
            var newName = 'targets';
            var delBtn = $('<button>').addClass('DelMail').html("<span class='typcn typcn-delete'></span>");
            var newTarget = $('<li>').append($('<input>').attr({type:'email',name:newName})).append(delBtn);
            $('#targets').find('li.Ctrl').before(newTarget);
            delBtn.on('click', function(ev){
                newTarget.remove();
                return false;
            });
            return false;
        });
    }
    if( $('#targets').length ){
        $('#targets').find('.DelMail').each(function(i, elm){
            $(this).on('click', function(ev){
                var mailLI = $(this).parent('li');
                mailLI.remove();
            });
        });
    }

    var addMessage = function(msg){
        var elm = $('<li>');
        var elm_msg = $('<span>').addClass('Message').text(msg);
        elm.append(elm_msg);
        $('#chatView').prepend(elm);
    }
    var pushComes = function(event){
        console.log("[PUSH] comes!!");
        var dat = JSON.parse(event.data);
        if(dat.msg){
            console.log("   msg: " + dat.msg);
            var elm = $('<li>');
            var elm_date = $('<span>').addClass('Date').text(dat.date);
            var elm_msg = $('<span>').addClass('Message').text(dat.msg);
            elm.append(elm_date).append(elm_msg);
            $('#chatView').prepend(elm);

            $('#chatMessage').val('');
        }else if( dat.lat && dat.lng ){
            var gPos = new google.maps.LatLng(dat.lat, dat.lng);
            var id = dat.connection;
            addMarker(id, gPos);
        }
    };

    if( $('.Chat').length ){
        if( $('.MobileTabMenu').css('display') !== 'none' ){
            // for Mobile
            $('.Gmap').before($('.ChatView .ChatPostForm'));

            var target = $('.MobileTabMenu').data('target');
            $('.'+target).hide();
            $('.MobileTabMenu').find('li').each(function(i, obj){
                var menu = $(this).find('a');
                var page = menu.data('page');
                if(i == 0){
                    $('#' + page).show();
                    menu.addClass('Selected');
                }
                menu.on('click', function(ev){
                    $('.'+target).hide();
                    $('.MobileTabMenu').find('li a').removeClass('Selected');
                    
                    $('#' + page).show();
                    menu.addClass('Selected');
                });
            });
        }

        if( $('.ChatView').length
          && !$('.ChatView').hasClass('Close') ){

            var url = $('.ChatView').data('url');
            var isCon = false;
            var ws = new WebSocket(url);
            ws.onmessage = pushComes;
            ws.onopen    = function(event){
                //            console.log("open");
                isCon=true;
            };
            ws.onclose = function(event){
                //            console.log("close");
                isCon = false;
                addMessage("接続が切れました");
                clearInterval(g_timer);
                clearMarker();
            };

            $('#postBtn').on('click', $.proxy(function(){
                var identifier = $('.ChatView').data('identifier');
                var msg = $('#chatMessage').val();            
                if( isCon ){
                    console.log("[MSG] " + msg);
                    ws.send(JSON.stringify({identifier: identifier, msg: msg}));
                }else{
                }
            }, this));

            var montior = function(event){
                ws.send(JSON.stringify({lat: event.coords.latitude, lng: event.coords.longitude}));
            };

            var getPosition = function(){
                navigator.geolocation.getCurrentPosition(function(ev){
                    ws.send(JSON.stringify({lat: ev.coords.latitude, lng: ev.coords.longitude}));
                }, null);
            }
            
            if(navigator.geolocation){
                getPosition();
                g_timer = setInterval(getPosition, 10000);
            }        
        }
    }
});
}(jQuery));
