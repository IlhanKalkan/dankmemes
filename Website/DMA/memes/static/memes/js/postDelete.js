$(document).ready(function() {
    
    // post deletion
    $(".postdeletebtn").on('click', function(event){
        event.preventDefault();
        var id = $(event.currentTarget).attr("id");
        console.log( "post deletion initiated." );
        console.log(id);
        // ask for confirmation
        if (confirm("Are you sure you want to delete your post?")){
            // if confirmed, delete post
            console.log("permission OKAY for deleting post number " + id );
            window.location.replace("/post_delete/" + id);
            console.log("post deleted.");
        } else {
            console.log("post deletion cancelled.");
        }
    });

});