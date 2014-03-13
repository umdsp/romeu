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
							alertText += 'ID ................' + ': ' + value.id.toString()+'\n';
							alertText += 'Name ..............' + ': ' + value.g_name+' '+value.m_name+' '+value.f_name+'\n';
							alertText += 'Birthday ..........' + ': ' + value.b_date+'\n';
							alertText += 'Birthday Location .' + ': ' + value.b_loc+'\n';
							alertText += '--------------------------------------------------------' + '\n';
						}
					alert(alertText)
				}
            });
		});
		$("#id_org_name").blur(function (data) {
			var jsonObject= {
					"org_name":$( "#id_org_name" ).val()
				};
			$.get("/ajax/creators/org_name/", {jobj: JSON.stringify(jsonObject)}, function(data) {
				if (data.length > 0) {
					var alertText = 'Already in database\n\n'
					for (var key in data )
						if (data.hasOwnProperty(key)) {
							var value = data[key];
							alertText += 'ID ................' + ': ' + value.id.toString()+'\n';
							alertText += 'Name ..............' + ': ' + value.org_name+'\n';
							alertText += '--------------------------------------------------------' + '\n';
						}
					alert(alertText)
				}
            });				
		});
		$("#id_name_en").blur(function (data) {
			var jsonObject= {
					"city":$( "#id_name_en" ).val(),
					"country":$( "#id_country_1" ).val()
				};
			$.get("/ajax/cities/", {jobj: JSON.stringify(jsonObject)}, function(data) {
				if (data.length > 0) {
					var alertText = 'Already in database\n\n'
					for (var key in data )
						if (data.hasOwnProperty(key)) {
							var value = data[key];
							alertText += 'ID ................' + ': ' + value.id.toString()+'\n';
							alertText += 'City ..............' + ': ' + value.city+'\n';
							alertText += 'Sate ..............' + ': ' + value.state+'\n';
							alertText += 'Country............' + ': ' + value.country+'\n';
							alertText += '--------------------------------------------------------' + '\n';
						}
					alert(alertText)
				}
            });				
		});
		
		$("#id_name_es").blur(function (data) {
			var jsonObject= {
					"city":$( "#id_name_en" ).val(),
					"country":$( "#id_country_1" ).val()
				};
			$.get("/ajax/cities/", {jobj: JSON.stringify(jsonObject)}, function(data) {
				if (data.length > 0) {
					var alertText = 'Already in database\n\n'
					for (var key in data )
						if (data.hasOwnProperty(key)) {
							var value = data[key];
							alertText += 'ID ................' + ': ' + value.id.toString()+'\n';
							alertText += 'City ..............' + ': ' + value.city+'\n';
							alertText += 'Sate ..............' + ': ' + value.state+'\n';
							alertText += 'Country............' + ': ' + value.country+'\n';
							alertText += '--------------------------------------------------------' + '\n';
						}
					alert(alertText)
				}
            });				
		});			

		$("#id_city_0").blur(function (data) {
			var jsonObject= {
					"title_en":$( "#id_title_en" ).val(),
					"title_es":$( "#id_title_es" ).val(),
					"city":$( "#id_city_1" ).val(),
					"country":$( "#id_country_1" ).val()
				};
			$.get("/ajax/locations/", {jobj: JSON.stringify(jsonObject)}, function(data) {
				if (data.length > 0) {
					var alertText = 'Already in database\n\n'
					for (var key in data )
						if (data.hasOwnProperty(key)) {
							var value = data[key];
							alertText += 'ID ................' + ': ' + value.id.toString()+'\n';
							alertText += 'Title..............' + ': ' + value.location+'\n';
							alertText += 'Country............' + ': ' + value.country+'\n';
							alertText += 'City ..............' + ': ' + value.city+'\n';
							alertText += '--------------------------------------------------------' + '\n';
						}
					alert(alertText)
				}
            });	
		});
		
		$("#id_title_en").blur(function (data) {
			var jsonObject= {
					"title_en":$( "#id_title_en" ).val(),
					"title_es":$( "#id_title_es" ).val()
				};
			$.get("/ajax/festivals/", {jobj: JSON.stringify(jsonObject)}, function(data) {
				if (data.length > 0) {
					var alertText = 'Already in database\n\n'
					for (var key in data )
						if (data.hasOwnProperty(key)) {
							var value = data[key];
							alertText += 'ID ................' + ': ' + value.id.toString()+'\n';
							alertText += 'Festival...........' + ': ' + value.festival+'\n';
							alertText += '--------------------------------------------------------' + '\n';
						}
					alert(alertText)
				}
            });				
		});
		
		$("#id_title_es").blur(function (data) {
			var jsonObject= {
					"title_es":$( "#id_title_es" ).val(),
					"title_en":$( "#id_title_en" ).val()
				};
			$.get("/ajax/festivals/", {jobj: JSON.stringify(jsonObject)}, function(data) {
				if (data.length > 0) {
					var alertText = 'Already in database\n\n'
					for (var key in data )
						if (data.hasOwnProperty(key)) {
							var value = data[key];
							alertText += 'ID ................' + ': ' + value.id.toString()+'\n';
							alertText += 'Festival...........' + ': ' + value.festival+'\n';
							alertText += '--------------------------------------------------------' + '\n';
						}
					alert(alertText)
				}
            });				
		});
		
		
    });
})(django.jQuery);
