$(document).ready(function(){
    var commentDeleteForm = $(".deleteCommentForm");
    commentDeleteForm.submit(function(event){
        event.preventDefault();
        var thisForm = $(this);
        var action = thisForm.attr("action");
        var method = thisForm.attr("method");
        var formData = thisForm.serialize();

        $.ajax({
            url: action,
            method: method,
            data: formData,
            success: function(data){
                event.target.parentNode.parentNode.parentNode.remove();
                if (data["result"]){
                    $("#"+data["result"]).remove();
                    }
            },
            error: function(errorData){
                console.log("Error");
                console.log(errorData);
            }
        })
    })
    }



    )