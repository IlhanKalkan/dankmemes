$(document).ready(function() {

    // comment posting
    $(".comment-form").on('submit', function(event){
        event.preventDefault();
        console.log( "comment submit received" );
        create_comment();
    });

    // reply posting
    $(".reply-form").on('submit', function(event){
        event.preventDefault();
        console.log( "reply submit received." );
        create_reply();
    });

    // AJAX for posting
    function create_comment() {
        console.log("create comment is working!"); // sanity check
        focus = $(':focus');
        val = focus.val(); // save input value
        id  = focus.attr('id');
        focus.val(''); // remove value from input
        console.log( id ); // for testing purposes
        console.log( val ); // retrieves input text through focused element

        $.ajax({
            url : "/create_comment/", // the endpoint
            type : "POST", // http method
            data : { comment_content : val,
                     comment_parentpost : id }, // data sent with the post request

            // handle a successful response
            success : function(json) {
                console.log(json); // log the returned json to the console
                divid = "#jsonUpdateComment" + id;
                console.log(" the found post id is " + divid); // another sanity check
                
                // fill in div
                $(divid).prepend("<li class='replycontainer blue lighten-5'><div class='comment childinline'>" + 
                    "<a class='italic b twelvepx inline colorblue' href='/u/" + json.creatorId + "'>" + json.creator + ": </a>" +
                    "<p>" + json.text + "</p>" +
                    "<div class='text-align-right inline'><p class='date inline eightpx gray'> " + json.pub_date +
                    "</p></div>" +
                    "</div></li> ");
                console.log("success"); // yet another sanity check
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                var res = "#result" + id;
                $(res).html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    };

    function create_reply() {
        console.log("create reply is working!"); // sanity check
        focus = $(':focus');
        val = focus.val(); // save the input value
        focus.val(''); // remove the value from the input
        id = focus.attr('id');
        console.log( id ); // for testing purposes
        console.log( val ); // retrieves input text through focused element
        $.ajax({
            url : "/create_reply/", // the endpoint
            type : "POST", // http method
            data : { reply_content :val,
                     reply_parentcomment : id }, // data sent with the post request

            // handle a successful response
            success : function(json) {
                console.log(json); // log the returned json to the console
                divid = "#jsonUpdateReply" + id;
                console.log(" the found post id is " + divid); // another sanity check
                
                // fill in div
                $(divid).prepend("<li class='replycontainer moreleftmargin grey lighten-4'><div class='reply childinline'>" + 
                    "<a class='italic b twelvepx inline colorblue' href='/u/" + json.creatorId + "'>" + json.creator + ": </a>" +
                    "<p>" + json.text + "</p>" +
                    "</div></li> ");
                console.log("success"); // yet another sanity check
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                var res = "#result" + id;
                $(res).html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    };

    $(function() {


        // This function gets cookie with a given name
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        var csrftoken = getCookie('csrftoken');

        /*
        The functions below will create a header with csrftoken
        */

        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        function sameOrigin(url) {
            // test that a given url is a same-origin URL
            // url could be relative or scheme relative or absolute
            var host = document.location.host; // host + port
            var protocol = document.location.protocol;
            var sr_origin = '//' + host;
            var origin = protocol + sr_origin;
            // Allow absolute or scheme relative URLs to same origin
            return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
                (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
                // or any other URL that isn't scheme relative or absolute i.e relative.
                !(/^(\/\/|http:|https:).*/.test(url));
        }

        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                    // Send the token to same-origin, relative URLs only.
                    // Send the token only if the method warrants CSRF protection
                    // Using the CSRFToken value acquired earlier
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });

    });

});