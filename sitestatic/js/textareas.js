tinyMCE.init({
	// General options
	mode : "textareas",
	theme : "advanced",
	plugins : "pagebreak,style,advlink,iespell,inlinepopups,insertdatetime,preview,searchreplace,contextmenu,paste,fullscreen,noneditable,nonbreaking,xhtmlxtras,wordcount,advlist,autosave",
 
	// Theme options
	theme_advanced_buttons1 : "bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,formatselect,fullscreen,code",
	theme_advanced_buttons2 : "cut,copy,paste,pastetext,|,search,replace,|,bullist,numlist,|,outdent,indent,blockquote,|,undo,redo,|,link,unlink,cleanup,|,insertdate,inserttime,preview",
	theme_advanced_buttons3 : "",
 
	theme_advanced_toolbar_location : "top",
	theme_advanced_toolbar_align : "left",
	theme_advanced_statusbar_location : "bottom",
 
	// Example content CSS (should be your site CSS)
	//content_css : "/css/style.css",
 
	template_external_list_url : "lists/template_list.js",
	external_link_list_url : "lists/link_list.js",
	external_image_list_url : "lists/image_list.js",
	media_external_list_url : "lists/media_list.js",
 
	// Style formats
	style_formats : [
		{title : 'Bold text', inline : 'strong'},
		{title : 'Red text', inline : 'span', styles : {color : '#ff0000'}},
		{title : 'Help', inline : 'strong', classes : 'help'},
	],
 
	width: '700',
	height: '160'
 
});