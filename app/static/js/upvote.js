<script type=text/javascript>
	$(function() {
		$('a#upvote').bind('click', function() {
			$.getJSON('/_upvote', {
				user_nickname: "{{ sugg.user_nickname}}",
				sugg_id: "{{ sugg.id }}"
			}, function(data) {
				$("#score").html("{{ sugg.score + 1 }}");
			});
			return false;
		});
	});
</script>
