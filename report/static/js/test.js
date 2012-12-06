$(function(){
	//loadTestResults('reflash=false');

	$('#id_reflash').click(function(e){
		e.preventDefault();
		var  selected_team = $('#id_teams a.btn-primary');
		if (selected_team === null || selected_team.length == 0){
			showAlert("", 'Warring!', 'You have not selected any Team yet!');
			return;
		}
		updateTestResults(selected_team[0].text);
	});

	$('#id_team_warrior').click(function(e){changeTeam(e, this);});
	$('#id_team_wizard').click(function(e){changeTeam(e, this);});
	$('#id_team_hunter').click(function(e){changeTeam(e, this);});
	$('#id_team_caissa').click(function(e){changeTeam(e, this);});

	$('#id_total').parent().click(function(){$('ul.unstyled li').show();});
	$('#id_red').parent().click(function(){filterResult('error');});
	$('#id_gray').parent().click(function(){filterResult('warring');});
	$('#id_green').parent().click(function(){filterResult('success');});

	function filterResult(flag){
		$('ul.unstyled li').hide();
		$('ul.unstyled li.'+flag).show();
	}
});

var TestGetter = {}

function showAlert (type, title, msg) {
	var alt = $('#id_alert');
	
	$('#id_title').text(title);
	$('#id_msg').text(msg);
	alt.addClass(type).show().fadeOut(10000);
}

function changeTeam(event, btn){
	event.preventDefault();
	loadTestResults('reflash=false&team='+$(btn).text()); 
	selectedTeam(btn);
}

function selectedTeam(btn){
	selecteBtn = $(btn);
	selecteBtn.parent().children().removeClass('btn-primary');
	selecteBtn.addClass('btn-primary');
}

function updateTestResults(team){
	loadTestResults('reflash=true&team='+team)
}

function loadTestResults(params){
	$('#id_loading').show();
	$('#id_reflash').hide();

	var request_url = '/test-results' + '?' + params;
	var template = '<li class="{{if green}}success{{/if}} {{if gray}}warring{{/if}} {{if red}}error{{/if}}">'
		+ '<a target="_blank" href="${latest_hostory}">${$item.removePrefix(url)}</a></li>';
	$.getJSON(request_url, function(data){
		var tests = data.tests;
		var actual_on = data.actual_on;
		$('#id_total').text(tests.length);
		$('#id_red').text(Counter.red(tests));
		$('#id_gray').text(Counter.gray(tests));
		$('#id_green').text(Counter.green(tests));
		$('#id_loading').hide();
		$('#id_reflash').show();

		$('#id_results').html(
			$.tmpl(template, tests, {
				removePrefix: function(value){
					return value.split('/')[3];
				}
			})

		);

		// format actual on date
		d = new Date(actual_on);
		d_str = d.getFullYear().toString() + '-'
			+ d.getMonth().toString() + '-'
			+ d.getDate().toString() + ' '
			+ d.getMinutes().toString() + ':'
			+ d.getSeconds().toString();
		$('#id_actual_on').text(d_str);
	});
}

var Counter = {
	red: function(data){
		var res = $.grep(data, function(el){
			return el.red;
		});
		return res.length;
	},
	green: function(data){
		var res = $.grep(data, function(el){
			return el.green;
		});
		return res.length;
	},
	gray: function(data){
		var res = $.grep(data, function(el){
			return el.gray;
		});
		return res.length;
	}
}