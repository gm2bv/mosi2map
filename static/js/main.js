(function($){
'use strict';

$(function(){
    // date
    if( $("#id_dlDate").length ){
        $("#id_dlDate").datepicker({
          dateFormat: "yy-mm-dd"
        });
    }
    
    // add a target
    if( $('#addTarget').length ){
        $('#addTarget').on('click', function(){
            var newName = 'mail';
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

    var checkInputForm = function(){

        var date = $("#id_dlDate").val();
        var hour = $("#id_dlHour").val();
        var min = $("#id_dlMin").val();
        var deadline = date + " " + hour + ":" + min;
        var term = $("#id_terms").val();
        $("#id_terms").find('option').each(function(){
            if( $(this).val() != term ){
                return true;
            }
            var str = $(this).text();
            if( $(this).attr('value') > 0 ){
                deadline += " 〜 " + str;
            }else{
                deadline += str;
            }
            $("#confirmForm").find("dt.Deadline.Confirm + dd").text(deadline);
            return false;
        });

        
        $("#confirmForm").find("dt.Targets.Confirm + dd ul.Targets").children().remove();
        $("#targets").find("input[type=email]").each(function(){
            var mail = $(this).val();
            $("#confirmForm").find("dt.Targets.Confirm + dd ul.Targets").append(
                $("<li>").text(mail)
            );
        });

        var message = $("#id_message").val();
        message = message.replace(/\n/g, '<br>');
        message = message.replace(/^\s/g, '');
        $("#confirmForm").find("dt.Message.Confirm + dd").html(message);

        return true;
    };

    // 確認ボタン
    $("#confirmBtn").on('click', function(){
        if( checkInputForm() ){
            $("#inputForm").hide();
            $("#confirmForm").show();
        }
        return false;
    });
    // キャンセルボタン
    $("#cancelBtn").on('click', function(){
        $("#inputForm").show();
        $("#confirmForm").hide();
        return false;
    });
});
}(jQuery));
