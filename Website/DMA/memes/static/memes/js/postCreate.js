$(document).ready(function() {
    
    // post creation page
    document.getElementById ("postCreateBtn").addEventListener ("click", disable, false);

    function disable() {
        $(this).attr('disabled', 'disabled');
    };

});