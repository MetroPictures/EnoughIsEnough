$(document).ready(function() {
	var buttons = {
		'1' : 3, 
		'2' : 15,
		'3' : 16,
		'4' : 6, 
		'10' : 12, 
		'mute' : 13,
		'$' : 14, 
		'SP' : 10, 
		'EU' : 11, 
		',' : 5, 
		'cmd' : 9, 
		'ctrl' : 8, 
		'inf' : 7,
		'pause' : 4
	};

	var hup = "hang_up";
	var pup = "pick_up";

	$("#mp_receiver")
		.html(pup)
		.click(function() {
			if($(this).html() == hup) {
				next_state = pup;
			} else if($(this).html() == pup) {
				next_state = hup;
			}

			$.ajax({
				url : $(this).html(),
				context : this
			}).done(function(json) {
				console.info(json);				
				$(this).html(next_state);
			});
		});
	
	var button_keys = Object.keys(buttons);
	for(var i=0; i<button_keys.length; i++) {
		var html = "<p class=\"num\">" + button_keys[i] + "</p>";
		var tr = $(document.createElement('tr'));
		var td = $(document.createElement('td'));
		var a = $(document.createElement('a'))
			.html(html)
			.click(function() {
				var mapping = $($(this).find('.num')[0]).html();
				$.ajax({
					url : "mapping/" + buttons[mapping]
				}).done(function(json) {
					console.info(json);
				});
			});

		$(td).append(a);
		$(tr).append(td);
		$("#mp_main").append(tr);
	}
});