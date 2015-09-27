(function($){
'use strict';

var g_timer;

$(function(){

    var get_clientname = function(){
        return 'localhost' + Math.floor($.now() / 1000);
    };
    var myname = get_clientname();;
    
    // date
    if( $("#id_dlDate").length ){
        $("#id_dlDate").datepicker({
          dateFormat: "yy-mm-dd"
        });
    }
    
    // time
    if( $('#id_dlHour').length && $('#id_dlMin').length ){
        if( $('#id_dlHour').val() < 0 ){
            $('#id_dlMin').attr('disabled', 'disabled').addClass('Disabled');
        }
        $('#id_dlHour').change(function(){
            if( $('#id_dlHour').val() < 0 ){
                $('#id_dlMin').attr('disabled', 'disabled').addClass('Disabled');
            }else{
                $('#id_dlMin').removeAttr('disabled').removeClass('Disabled');
            }
        });
    }

    // add a target
    if( $('#addTarget').length ){
        $('#addTarget').on('click', function(){
//            var cnt = $('#targets').find('input[type=text]').length;
            var newName = 'mail';
//            var newName = 'targets';
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
            var userMarkers = new Object();

            var addChat = function(data){
                var dateVal = new Date(data.created_at);
                var dateStr = dateVal.getFullYear() + '年' +
                    (dateVal.getMonth() + 1) + '月' +
                    dateVal.getDate() + '日 ' +
                    dateVal.getHours() + '時' +
                    dateVal.getMinutes() + '分';
                $('#chatView').prepend(
                    $('<li>').append(
                        $('<span>').addClass('Date').text(dateStr)
                    ).append(
                        $('<span>').addClass('Message').text(data.message)
                    )
                );
            };
            var addMessage = function(msg){
                $('#chatView').prepend(
                    $('<li>').append(
                        $('<span>').addClass('Message').text(msg)
                    )
                );
            }

            var setPosition = function(){
                navigator.geolocation.getCurrentPosition(function(ev){
                    var identifier = location.pathname.replace(/.*\/([\w]+)\/$/, '$1');
                    var data = {
                        'identifier': identifier,
                        'local_channel': myname,
                        'lat': ev.coords.latitude,
                        'lng': ev.coords.longitude
                    };
                    swampdragon.callRouter('get_markers', 'marker-list',
                                           data,
                                           function(context, data){
                                           });
                }, null);
            };

            var showMarkers = function(obj){
                var id = obj.local_channel;
                var location = new google.maps.LatLng(obj.lat, obj.lng);
                if( userMarkers[id] ){
                    var curPos = userMarkers[id].getPosition();
                    var meter = google.maps.geometry.spherical.computeDistanceBetween(location, curPos);
                    if( meter < 100 ){ return } // 近距離は除外
                    userMarkers[id].setMap(null);
                }

                userMarkers[id] = new google.maps.Marker({
                    draggable: false,
                    animation: google.maps.Animation.BOUNCE,
                    position: location,
                    icon: {
                        path: google.maps.SymbolPath.BACKWARD_CLOSED_ARROW,
                        scale: 5
                    },
                    map: g_map
                });
            };            
            
            // =======================
            // メインの処理
            // =======================
            swampdragon.ready(function(){
                isCon=true;
                var identifier = location.pathname.replace(/.*\/([\w]+)\/$/, '$1');
                
                swampdragon.subscribe('chat-list', 'ch-chat|' + myname,
                                      {'identifier': identifier},
                                      function(context, data){},
                                      function(context, data){}
                                     );

                swampdragon.subscribe('marker-list', 'ch-marker|' + myname,
                                      {'identifier': identifier},
                                      function(context, data){}
                                      function(context, data){}
                                     );                                
                
                swampdragon.getList('chat-list',
                                    {'identifier': identifier},
                                    function(response, data){
                                        for(var i=data.length; i > 0;){
                                            addChat(data[--i]);
                                        }
                                    });
            });

            // Push通知
            swampdragon.onChannelMessage(function(channels, obj){
                if( $.inArray('ch-chat|' + myname, channels) >= 0 ){
                    addChat(obj.data);
                }
                if( $.inArray('ch-marker|' + myname, channels) >= 0){
                    showMarkers(obj);
                }
            });

            swampdragon.close(function(){                
                //            console.log("close");
                isCon = false;
                addMessage("接続が切れました");
                clearInterval(g_timer);
                clearMarker();
                $('#postBtn').off('click');
                $('#postBtn').attr('disabled', 'disabled');
            });

            // 投稿ボタン
            $('#postBtn').on('click', $.proxy(function(){
                var id = $('.ChatView').data('id');
                var identifier = $('.ChatView').data('identifier');
                var msg = $('#chatMessage').val();            
                if( isCon ){
                    swampdragon.create('chat-list', {
                        'identifier': identifier,
                        'message': msg,
                    },function(context, data){
                        $('#chatMessage').val('');
                    },function(context, data){
                        addMessage("送信に失敗しました。再投稿してください");
                        console.log(data);
                    });
                }else{
                }
            }, this));

            if(navigator.geolocation){
                setPosition();
                g_timer = setInterval(setPosition, 10000);
            }                    
        } // $('.ChatView').length
    } // $('.Chat')
});
}(jQuery));
