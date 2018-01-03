graphwidth = Math.min($('#graph-container').width(), 600);
$('#graph').width(graphwidth);
$('#graph').height(graphwidth);
			
var svg = d3.select("svg"),
	width = graphwidth,
	height = graphwidth,
	radiofuera = 32*width/64,
	radionivelbajo = 27*width/64,
	radionivelmedio = 20*width/64,
	radionivelalto = 13*width/64,
	radiocircentro = 6*width/64,
	posiciontextopart = radionivelbajo + (radiofuera-radionivelbajo)/3,
	radiodiputado = 12,
	lealtadajuste = 0,
	partidos = [],
	partidosplacing = [],
	coloresfranjas = ["#CCC", "#DDD", "#EEE"];

var nivelpartidos, 
	nivelbajo, 
	nivelmedio, 
	nivealto, 
	ciculocentro,
	separadores,
	michelle,
	textpath,
	nombrespartidos,
	diputados, 
	diputadoscirculos;

var display = 'sinasistencia',
	selectedbtn = 1;

d3.json("../public/data/diputados.laealtad.json", function(error, graph) {
	if (error) throw error;
	
	diputados = graph.diputados;
	partidos = graph.partidos;
	for (var i=0; i<partidos.length; i++) {
		partidosplacing[i] = 1;
	}
	
	nivelpartidos = svg.append("g")
		.append("circle")
		.attr("r", radiofuera)
		.attr("cx", width/2)
		.attr("cy", height/2)
		.attr("fill", "#3F607D")
		.attr("stroke", "#FFF")
		.attr("stroke-width", 1);
	
	nivelbajo = svg.append("g")
		.append("circle")
		.attr("r", radionivelbajo)
		.attr("cx", width/2)
		.attr("cy", height/2)
		.attr("fill", coloresfranjas[0])
		.attr("stroke", "#FFF")
		.attr("stroke-width", 2);
	
	nivelmedio = svg.append("g")
		.append("circle")
		.attr("r", radionivelmedio)
		.attr("cx", width/2)
		.attr("cy", height/2)
		.attr("fill", coloresfranjas[1]);
	
	nivealto = svg.append("g")
		.append("circle")
		.attr("r", radionivelalto)
		.attr("cx", width/2)
		.attr("cy", height/2)
		.attr("fill", coloresfranjas[2]);
	
	ciculocentro = svg.append("g")
		.append("circle")
		.attr("r", radiocircentro)
		.attr("cx", width/2)
		.attr("cy", height/2)
		.attr("fill", "#FFF");
	
	separadores = svg.append("g")
  		.selectAll(".separadores")
  		.data(partidos)
		.enter()
		.append("line")
		.attr("x1", width/2)
		.attr("y1", height/2)
		.attr("x2", width/2)
		.attr("y2", 0 + radiocircentro)
		.attr("stroke-width", 5)
		.attr("stroke", "#fff")
		.attr("transform",function(d,i) { return "rotate(" + 360*i/8 + ", " + width/2 + "," + height/2 + ") translate(0," + -1*radiocircentro + ")"; });
	
	michelle = svg.append("g")
		.append("svg:image")
		.attr("xlink:href",  "./public/images/michelle.jpg")
		.attr("height", radiocircentro*1.2)
        .attr("width", radiocircentro*1.2)
		.attr("x", width/2 - 1.2*radiocircentro/2)
        .attr("y", height/2 - 1.2*radiocircentro/2);
	
	textpath = svg.append("path")
		.attr("id", "textpath")
		.attr("d", "M " + width/2 + ", " + height/2 + " m -" + posiciontextopart + ", 0 a " + posiciontextopart + "," + posiciontextopart + " 0 1,1 " + 2*posiciontextopart + ",0 a " + posiciontextopart + "," + posiciontextopart + " 0 1,1 -" + 2*posiciontextopart + ",0")
		.style("fill", "none");
	nombrespartidos = svg.append("text")
  		.selectAll(".nombrespartidoscirc")
  		.data(partidos)
		.enter()
	   	.append("textPath")
		.attr("xlink:href", "#textpath") 
		.style("text-anchor","middle") 
		.style("fill","#FFF") 
		.attr("startOffset", function(d,i) {return (100/8)/2 + 100*i/8 + "%"; })		
		.text(function (d,i) { return d; })
		.attr("class","nombrespartidos");
	
	
	diputadoscirculos = svg.append("g")
		.selectAll("diputados")
		.data(diputados)
		.enter().append("g")
		.attr("class", "diputados")
		.attr("transform",function(d,i) { 
			var partidoindex = partidos.indexOf(d.comite_parlamentario);
			var lealtad = Math.max(0, (d.lealtad - lealtadajuste)/(1 - lealtadajuste))
			var mov = partidosplacing[partidoindex]*(Math.random(0,1))*(360/8)/4;
			var rotate = "rotate(" + ((360/8)/2 - 90 + mov + 360*partidoindex/8) + ", " + width/2 + "," + height/2 + ")";
			var translate = "translate(0,-" + (radiocircentro + (1-lealtad)*(radionivelbajo - radiocircentro)) + ")"
			partidosplacing[partidoindex] = partidosplacing[partidoindex]*-1
			return rotate + " " + translate; 
		})
		.on("mouseover", function(d) {
			
			var selection = d3.select("#tooltip")
				.style("left", (d3.event.pageX) + "px")
				.style("top", (d3.event.pageY) + "px")
				.style("background-color", "#FFF")
				.classed("hidden", false);						
		  
			selection.select("#tooltip-image")
				.attr("src", "https://www.camara.cl/img.aspx?prmid=g" + d.prmid);
								  
			selection.select("#tooltip-nombre")
				.html(d.nombre)
			
			selection.select("#tooltip-partido")
				.html(d.comite_parlamentario)
									
			selection.select("#value")
				.html("Votos a Favor: " + d.favor + "<br>" + "Votos en Contra: " + d.contra + "<br>" + "Abstenciones: " + d.abstencion + "<br>" + "Inasistencias: " + d.ausencia);	
		})
	  	.on("mouseout", function(d){
			d3.select("#tooltip").classed("hidden", true);
		});
		
	 
	 
	diputadoscirculos.append("circle")
		.attr("class", "diputado-circulo")
		.attr("r", radiodiputado)
		.attr("stroke", "#FFF")
		.attr("fill", "#53A0B8")
		.attr("cx", width/2 - radiodiputado/2)
		.attr("cy", height/2 + radiodiputado/2)
	
	diputadoscirculos.append("svg:image")
		.attr("class", "diputado-imagen")
		.attr("xlink:href",  function(d) { return "https://www.camara.cl/img.aspx?prmid=chs" + d.prmid; })
		.attr("height", radiodiputado)
        .attr("width", radiodiputado)
		.attr("x", width/2 - 10)
        .attr("y", height/2);				
});

function mostrarLealtadSinAsistencia() {
	display = 'sinasistencia';
	
	diputadoscirculos.transition().duration(750).attr("transform",function(d,i) { 
		var partidoindex = partidos.indexOf(d.comite_parlamentario);
		var lealtad = Math.max(0, (d.lealtad - lealtadajuste)/(1 - lealtadajuste))
		var mov = partidosplacing[partidoindex]*(Math.random(0,1))*(360/8)/4;
		var rotate = "rotate(" + ((360/8)/2 - 90 + mov + 360*partidoindex/8) + ", " + width/2 + "," + height/2 + ")";
		var translate = "translate(0,-" + (radiocircentro + (1-lealtad)*(radionivelbajo - radiocircentro)) + ")"
		partidosplacing[partidoindex] = partidosplacing[partidoindex]*-1
		return rotate + " " + translate; 
	});
}

function mostrarLealtadConAsistencia() {
	display = 'conasistencia';
	
	diputadoscirculos.transition().duration(750).attr("transform",function(d,i) { 
		var partidoindex = partidos.indexOf(d.comite_parlamentario);
		var lealtad = Math.max(0, (d.lealtad_con_asistencia - lealtadajuste)/(1 - lealtadajuste))
		var mov = partidosplacing[partidoindex]*(Math.random(0,1))*(360/8)/4;
		var rotate = "rotate(" + ((360/8)/2 - 90 + mov + 360*partidoindex/8) + ", " + width/2 + "," + height/2 + ")";
		var translate = "translate(0,-" + (radiocircentro + (1-lealtad)*(radionivelbajo - radiocircentro)) + ")"
		partidosplacing[partidoindex] = partidosplacing[partidoindex]*-1
		return rotate + " " + translate; 
	});
}

function mostrarLealtadSoloReprobados() {
	display = 'soloreprobados';
	
	diputadoscirculos.transition().duration(750).attr("transform",function(d,i) { 
		var partidoindex = partidos.indexOf(d.comite_parlamentario);
		var lealtad = Math.max(0, (d.lealtad_rec - lealtadajuste)/(1 - lealtadajuste))
		var mov = partidosplacing[partidoindex]*(Math.random(0,1))*(360/8)/4;
		var rotate = "rotate(" + ((360/8)/2 - 90 + mov + 360*partidoindex/8) + ", " + width/2 + "," + height/2 + ")";
		var translate = "translate(0,-" + (radiocircentro + (1-lealtad)*(radionivelbajo - radiocircentro)) + ")"
		partidosplacing[partidoindex] = partidosplacing[partidoindex]*-1
		return rotate + " " + translate; 
	});
}

function mostrarLealtadPrimerTramite() {
	display = 'primertramite';
	
	diputadoscirculos.transition().duration(750).attr("transform",function(d,i) { 
		var partidoindex = partidos.indexOf(d.comite_parlamentario);
		var lealtad = Math.max(0, (d.lealtad_tr01 - lealtadajuste)/(1 - lealtadajuste))
		var mov = partidosplacing[partidoindex]*(Math.random(0,1))*(360/8)/4;
		var rotate = "rotate(" + ((360/8)/2 - 90 + mov + 360*partidoindex/8) + ", " + width/2 + "," + height/2 + ")";
		var translate = "translate(0,-" + (radiocircentro + (1-lealtad)*(radionivelbajo - radiocircentro)) + ")"
		partidosplacing[partidoindex] = partidosplacing[partidoindex]*-1
		return rotate + " " + translate; 
	});
}

function cambiarTipo(n) {
	var btn = contents[n-1];
	var ths = $('#btn_' + n)
	
	btn.action();
	
	
	$('#pos').animate({
		left: (n-1)*25 + '%',
	}, {
		duration: 500,
		complete: function() {
			$('#expl-container h1').text(btn.title);
			$('#expl-container p').text(btn.body);	
			$('#buttons-container a.nav-link').removeClass('active');
			ths.addClass('active');					
		}
	});
}

var contents = [
	{
		n: 1,
		button: "General",
		title: "Índice de cercanía legislativa - Todos",
		body: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum",
		action: mostrarLealtadSinAsistencia
	},
	{
		n: 2,
		button: "Sólo Asistentes",
		title: "Tomando en cuenta sólo las sesiones en la que asistieron",
		body: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum",
		action: mostrarLealtadConAsistencia
	},
	{
		n: 3,
		button: "Primer Trámite",
		title: "Tomando en cuenta sólo Primer Trámite - Primer Informe",
		body: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum",
		action: mostrarLealtadPrimerTramite
	},
	{
		n: 4,
		button: "Rechazados",
		title: "Tomando en cuenta sólo los proyectos finalmente rechazados",
		body: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum",
		action: mostrarLealtadSoloReprobados
	}
];

for (var i = 0; i < contents.length; i++) {
	btn = contents[i];
	$('#buttons-container').append('<li class="nav-item"><a id="btn_' + btn.n + '" data-n="' + btn.n + '" class="nav-link ' + (i==0 ? 'active' : '') + '" href="javascript:">' + btn.button + '</a></li>');
}
$('#expl-container h1').text(contents[0].title);
$('#expl-container p').text(contents[0].body);

var automatico = setInterval(cambiarAuto, 5000);
var counter = 1;
function cambiarAuto() {
    if (counter == 4) {
    	counter = 1;
    }
	else {
		counter ++;
	}
	cambiarTipo(counter);
}

$('#buttons-container a.nav-link').click(function() {
	clearInterval(automatico);
	
	var n = $(this).data('n');
	cambiarTipo(n);
});