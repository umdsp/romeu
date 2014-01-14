(function($) {
    $(document).ready(function() {
        $("#id_family_name").blur(function (data) {
			var jsonObject= {
					"g_name":$( "#id_given_name" ).val(),
					"m_name":$( "#id_middle_name" ).val(), 
					"f_name":$( "#id_family_name" ).val()
				};
			$.get("/ajax/creators/", {jobj: JSON.stringify(jsonObject)}, function(data) {
				if (data.length > 0) {
					var alertText = 'Already in database\n\n'
					for (var key in data )
						if (data.hasOwnProperty(key)) {
							var value = data[key];
							alertText += 'ID ................' + ': ' + value.id+'\n';
							alertText += 'Name ..............' + ': ' + value.g_name+' '+value.m_name+' '+value.f_name+'\n';
							alertText += 'Birthday ..........' + ': ' + value.b_date+'\n';
							alertText += 'Birthday Location .' + ': ' + value.b_loc+'\n';
							alertText += '--------------------------------------------------------' + '\n';
						}
					alert(alertText)
				}
            });
		});
		$("#id_org_name").change(function (data) {
			var jsonObject= {
					"org_name":$( "#id_org_name" ).val()
				};
			$.get("/ajax/creators/org_name/", {jobj: JSON.stringify(jsonObject)}, function(data) {
				if (data.length > 0) {
					var alertText = 'Already in database\n\n'
					for (var key in data )
						if (data.hasOwnProperty(key)) {
							var value = data[key];
							alertText += 'ID ................' + ': ' + value.id+'\n';
							alertText += 'Name ..............' + ': ' + value.org_name+'\n';
							alertText += '--------------------------------------------------------' + '\n';
						}
					alert(alertText)
				}
            });				
		});
    });
})(django.jQuery);
