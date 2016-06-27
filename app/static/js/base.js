$(document).ready( function() {
    $('a.minimize').click(function() {
        $(this).parent().replaceWith("This isn't done yet...");
    });
	$('a.upvote').click(function() {
		var user_nickname = g_user_nickname;
		var sugg_id = $(this).parent().find(".sugg_id").html();
		var score = parseInt($(this).parent().find(".score").html());
		score += 1;
		$(this).parent().find(".score").text( score );
		$.post("/_upvote", {
			user_nickname: user_nickname,
			sugg_id: sugg_id
		});
	});
	$('a.delete').click(function() {
		var user_nickname = g_user_nickname;
		var sugg_id = $(this).parent().find(".sugg_id").html();
		$(this).parent().hide();
		$.post("/_delete_suggestion", {
			user_nickname: user_nickname,
			sugg_id: sugg_id
		});
	});
    $('a.reply').click(function() {
        $(document).find("div.reply_div").hide();
        var form = "<div class='comment reply_div' id='reply_form'><form id='reply_form' class='reply_form' action=''> \
                    <h2>Reply Here:</h2> \
                    <input type='text' name='reply_text' id='reply_text' class='form-control reply_text' placeholder='Words go here'> \
                    <input type='submit' value='Submit' class='postreply btn btn-lg btn-primary btn-block'></input> \
                    </form></div>"
        $(form).insertAfter( $(this) );
        $(document).find("#reply_text").focus();
    });
    $(document).on('submit', '.reply_form', function() {
        var text = $(document).find("#reply_text").val();
        var parent_id = $(document).find("#reply_form").parent().find(".comment_id").html();
        var user_nickname = $(document).find("#reply_form").parent().find(".comment_nickname").html();
        var suggestion_id = $(document).find(".sugg_id").html();
        var data = {};
        data.text = text;
        data.parent_id = parent_id;
        data.user_nickname = user_nickname;
        data.suggestion_id = suggestion_id;
        $.ajax({
            type: "POST",
            url: "/reply",
            data: JSON.stringify(data),
            contentType: 'application/json; charset=utf-8',
            dataType: "json",
            success: function(result) {
                location.reload();
            },
            error: function(error) {
                alert("Something broke");
            }
        });
        console.log(data.text);
        return false;
    });
});
