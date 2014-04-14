<div class="row">
	<div class="large-12 medium-12 small-12 columns">
		<fieldset>
			<legend>Basic Search</legend>
			<form action="search.php" method="GET" class="row collapse">
				<div class="small-2 columns">
					<select name="category">
						<option value="All" selected>All</option>
						<option value="Thesis">Thesis</option>
						<option value="Researcher">Researcher</option>
						<option value="Department">Department</option>
						<option value="Faculty">Faculty</option>
						<option value="Year">Year</option>
					</select>
				</div>
				<div class="small-8 columns">
					<input id="q" type="text" name="search" placeholder="Search for keywords or scopes" autofocus autocomplete="off" onkeyup="updateTypeAhead(q.value)"/>
					<div id="typeahead-data"></div>
				</div>
				<div class="small-2 columns">
					<input id="jumbo-browse" type="submit" class="postfix small button" value="Browse" />
				</div>
			</form>
		</fieldset>
	</div>
</div>
<script>
	function updateTypeAhead(q) {
		$('#typeahead-data div').remove();
		if (q !== '') {
			$('#typeahead-data').css('display', 'block');
			$.ajax({
				url: 'app/updateTypeAhead.php?q='+q,
				dataType: 'json',
				success: function(data) {
					for (var i = 0; i < data.vector.length; i++) {
						$('#typeahead-data').append('<div id="ta_data_'+i+'" onclick="transportValue(ta_data_'+i+'.innerHTML)">' +
							data.vector[i]['val'] + '</div>');
					}
				}
			});
		} else {
			$('#typeahead-data').css('display', 'none');
		}
	}

	function transportValue(ta_data) {
		$('#q').val(ta_data);
		$('#typeahead-data').css('display', 'none');
	}
</script>