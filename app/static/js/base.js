$(document).ready( function() {
	$('a.upvote').click(function() {
		var user_nickname = g_user_nickname;
		var sugg_id = $(this).parent().find(".sugg_id").html();
		$.post("/_upvote", {
			user_nickname: user_nickname,
			sugg_id: sugg_id
		});
	});
	$('a.delete').click(function() {
		var user_nickname = g_user_nickname;
		var sugg_id = $(this).parent().find(".sugg_id").html();
		$.post("/_delete_suggestion", {
			user_nickname: user_nickname,
			sugg_id: sugg_id
		});
	});
});
