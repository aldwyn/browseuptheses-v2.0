$(document).ready(function() {
	var fadeSpeed = 'fast';

	$('#jumbo-browse').click(function() {
		if ($('#jumbo-query').val() !== '') {
			$('#jumbotron').slideUp('slow');
			$('#main-query').val($('#jumbo-query').val());
			$('#for-trend').html($('#jumbo-query').val());
			$('#field-opt'+$('#jumbo-opt').val()).attr('selected', 'selected');
		};
	});

	$('#main-query')
		.focusin(function() { $('#query-response').slideDown(fadeSpeed); })
		.focusout(function() { $('#query-response').slideUp(fadeSpeed); })
		.keyup(function() { console.log($(this).val()); }
	);

	$('#jumbo-query')
		.focusin(function() { $('#jumbo-query-response').slideDown(fadeSpeed); })
		.focusout(function() { $('#jumbo-query-response').slideUp(fadeSpeed); })
		.keyup(function() { console.log($(this).val()); }
	);


});