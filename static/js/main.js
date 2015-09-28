(function($){
'use strict';

$(function(){
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
});
}(jQuery));
